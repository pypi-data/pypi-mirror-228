#!/usr/bin/env python
import json
import os
import re

import openai
from openai import error as openai_error
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from .conversation import Conversation
from .load_config import load_secrets, ensure_directories, ensure_config_files
from .message_handlers import handle_greetings, handle_common_queries, handle_url_ask
from .utils import generate_filename, read_config, fetch_prompt, log_error, ensure_directories, ensure_keys


class TelegramBot:
    # Commands
    async def tele_start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        current_uname = update.message.chat.username.lstrip("@")
        if current_uname == self.telegram['owner']:
            greeting_text = f'Oh, hello {update.message.from_user.first_name}! Let me get to work!'
            bot_info = await context.bot.get_me()
            self.telegram['bot_id'] = bot_info.id
            await update.message.reply_text(greeting_text)
            self.started = True
            self.GPTOnline = True
        else:
            await update.message.reply_text(f'Sorry {current_uname}, but I\'m off the clock at the moment.')

    async def tele_nick_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        human_uid: str = str(update.message.from_user.id)
        new_nickname = update.message.text.strip()
        prompt = f'Please refer to me by my nickname, {new_nickname}, rather than my user name.'
        await self.tele_handle_response(human_uid, prompt)

    # Responses
    async def tele_handle_response(self, uname: str, text: str) -> str:

        # Before we handle messages, ensure a user has /started us
        # Starting ensures we get some kind of user account details for logging
        if not self.started:
            return 'I\'d love to chat, but please wait as I haven\'t started up yet!'

        processed: str = text.lower().strip()

        # First, we add the user's message to our conversation
        self.conversations[uname].add_user_message(text)

        # Let's check if the user is asking about a [URL]
        url_match = re.search(r'\[http(s)?://\S+]', text)

        # Then we form the assistant's message, add it to our conversation, and return it
        reply = 'Unhandled response.'
        # Then we process some low level easy stuff, or send it to GPT
        if handle_greetings(text=processed):
            reply = handle_greetings(text=processed)
        elif handle_common_queries(text=processed):
            reply = handle_common_queries(text=processed)
        elif url_match:
            reply = await handle_url_ask(text=processed)
        elif self.GPTOnline:
            # This is essentially the transition point between quick Telegram replies and GPT
            gptresponse = self.gpt_completion(uname)
            token_count = gptresponse['usage']['total_tokens']
            reply = gptresponse['choices'][0]['message']['content'].strip()

            # We need to check some rolling thresholds to ensure we don't overload our token limit:
            if token_count > (self.chatgpt['token_limit'] * self.chatgpt['prune_threshold']):
                # Start pruning if we hit our upper threshold, but don't worry, we warn well below it.
                self.conversations[uname].prune_conversation(self.chatgpt['token_limit'],
                                                             self.chatgpt['prune_back_to'])
            elif token_count > (self.chatgpt['token_limit'] * self.chatgpt['prune_back_to']) \
                    and not self.users[uname].summary_warning:
                # Check to see if we're getting close to the conversation limit, and add a warning.
                reply += ("\n\nBy the way, we're starting to get close to my current conversation length "
                          "limits, so I may start forgetting some of our older exchanges, would you like me to "
                          "summarize our conversation so far, to keep the main points alive?")
                self.users[uname].summary_warning = True
        else:
            reply = "Sorry, I'm not on the clock right now, please wait for my owner to start me up."
        self.conversations[uname].add_assistant_message(reply)
        return reply

    # Handles the Telegram side of the message, discerning between Private and Group conversation
    async def tele_handle_message(self, update: Update, context=ContextTypes.DEFAULT_TYPE):
        human_uid: str = str(update.message.from_user.id)
        human_name: str = str(update.message.from_user.first_name)

        # See if this is a new conversation we need to track
        if human_uid not in self.conversations:
            interactionlogfile = generate_filename(str(self.telegram['bot_id']), human_uid).lower()
            self.conversations[human_uid] = Conversation(self.chatgpt['personaprompt'], interactionlogfile)

        # PM or Group Chat
        message_type: str = update.message.chat.type
        message_text: str = update.message.text
        message_usr = update.message.from_user.username
        print(f'User ({update.message.chat.id}) {message_usr} in {message_type}')

        # If it's a group text, only reply if the bot is named. The real magic of how the bot behaves isn't here,
        # it's in tele_handle_response()
        if message_type == 'supergroup' or message_type == 'group':
            if self.telegram['username'] in message_text:
                new_text: str = message_text.replace(self.telegram['username'], '').strip()
                response: str = await self.tele_handle_response(human_uid, new_text)
            elif self.telegram['nickname'].lower() in message_text.lower() or self.telegram['initials'] in message_text:
                response: str = await self.tele_handle_response(human_uid, message_text)
            else:
                return
        elif message_type == 'private':
            response: str = await self.tele_handle_response(human_uid, message_text)
        else:
            return
        await update.message.reply_text(response)

    # Formally closes out the polling loop and "clears" the bot back to a generic state
    async def tele_stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.chat.username.lstrip("@") == self.telegram['owner']:
            self.GPTOnline = False
            await update.message.reply_text("Sure things boss, cutting out!")
        else:
            await update.message.reply_text("Sorry, I can't do that for you.")

    # Handle errors caused on the Telegram side
    async def tele_error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        log_error(context.error, 'Telegram', self.ErrorLog)

    # Read the GPT Conversation so far
    @staticmethod
    def gpt_read_interactions(filepath):
        with open(filepath, 'r') as interaction_log:
            lines = interaction_log.readlines()
        formatted_messages = [json.loads(line) for line in lines]
        return formatted_messages

    def gpt_completion(self, uname):
        try:
            response = openai.ChatCompletion.create(
                model=self.chatgpt['model'],
                messages=self.conversations[uname].messages,
                temperature=self.chatgpt['temp'],
                top_p=self.chatgpt['top_p']
            )
            return response
        except openai_error.AuthenticationError as e:
            # Handle authentication error
            log_error(e, error_type='OpenAI-Authentication', error_filename=self.ErrorLog)
        except openai_error.InvalidRequestError as e:
            # Handle invalid request error
            log_error(e, error_type='OpenAI-InvalidRequest', error_filename=self.ErrorLog)
        except openai_error.APIConnectionError as e:
            # Handle API connection error
            log_error(e, error_type='OpenAI-APIConnection', error_filename=self.ErrorLog)
        except openai_error.OpenAIError as e:
            # Handle other OpenAI-related errors
            log_error(e, error_type='OpenAI-Other', error_filename=self.ErrorLog)
        except Exception as e:
            # Catch any other unexpected exceptions
            log_error(e, error_type='Other', error_filename=self.ErrorLog)

    # The main polling "loop" the user interacts with via Telegram
    def start_polling(self):
        self.telegram['app'].run_polling(poll_interval=self.telegram['pollinterval'])

    # Initialization
    def __init__(self, bot_username=None, bot_nickname=None,
                 bot_initials=None, bot_owner=None, bot_owner_uid=None, chatmodel=None, persona_name=None,
                 persona_prompt=None, persona_temp=1.0):

        # First check if directories and keys are available to start
        ensure_directories()
        ensure_keys()

        # Set up our variables
        self.ErrorLog = os.path.join(os.environ['TELLMGRAMBOT_APP_PATH'], 'errorlogs', 'error.log')
        self.started = False
        self.GPTOnline = False
        self.users = {}
        self.conversations = {}

        # Get Telegram Spun Up
        self.telegram = {
            'bot_id': None,
            'owner': bot_owner,
            'owner_id': bot_owner_uid,
            'username': bot_username,
            'nickname': bot_nickname,
            'initials': bot_initials,
            'pollinterval': 3
        }
        self.telegram['app'] = Application.builder().token(os.environ.get('TELLMGRAMBOT_TELEGRAM_API_KEY')).build()

        # Add our handlers for Commands, Messages, and Errors
        self.telegram['app'].add_handler(CommandHandler('start', self.tele_start_command))
        self.telegram['app'].add_handler(CommandHandler('stop', self.tele_stop_command))
        self.telegram['app'].add_handler(CommandHandler('nick', self.tele_nick_command))
        self.telegram['app'].add_handler(MessageHandler(filters.TEXT, self.tele_handle_message))
        self.telegram['app'].add_error_handler(self.tele_error)

        # Get our LLM Spun Up
        self.chatgpt = {
            'personaname': persona_name,
            'personaprompt': persona_prompt,
            'model': chatmodel or 'gpt-3.5-turbo',
            'temp': persona_temp or 1.0,
            'top_p': 0.9,
            'token_limit': 4096,  # 4096 for gpt-3.5-turbo
            'prune_threshold': 0.9,
            'prune_back_to': 0.75
        }
        openai.api_key = os.environ.get('TELLMGRAMBOT_OPENAI_API_KEY')

    # Sets the TelegramBot object based on the YAML configuration and prompt files
    def set(config_file='config.yaml', prompt_file='prompts/starter.prmpt'):
        
        # First check if directories and keys are available to start
        ensure_directories()
        ensure_keys()
        
        # Set YAML configuration file to apply to bot, unless invalid
        try:
            config = read_config(config_file)
        except:
            print(f"Could not read the configuration file '{config_file}'. Creating a new template...")
            with open(config_file, 'w') as f:
                f.write('bot_uname:       test_bot\n')
                f.write('bot_uname_owner: <YOUR BOT USERNAME>\n')
                f.write('bot_uid_owner:   <YOUR BOT UID FROM BOTFATHER>\n')
                f.write('bot_name:        Test Bot\n')
                f.write('bot_nickname:    Testy\n')
                f.write('bot_initials:    TB\n')
                f.write('model:           gpt-3.5-turbo\n')
            config = read_config(config_file)

        # Set text prompt that defines bot's characteristics unless undefined
        try:
            prompt = fetch_prompt(prompt_file)
        except:
            print(f"Could not read the prompt file '{prompt_file}'. Creating a new template...")
            with open(prompt_file, 'w') as f:
                f.write('You are a test harness bot')
            prompt = fetch_prompt(prompt_file)

        # Apply parameters to bot:
        return TelegramBot(
            bot_username   = config['bot_uname'],
            bot_nickname   = config['bot_nickname'],
            bot_initials   = config['bot_initials'],
            bot_owner      = config['bot_uname_owner'],
            bot_owner_uid  = config['bot_uid_owner'],
            chatmodel      = config['model'],
            persona_name   = config['bot_name'],
            persona_prompt = prompt
        )