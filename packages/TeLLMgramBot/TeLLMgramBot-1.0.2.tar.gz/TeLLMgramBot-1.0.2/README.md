# TeLLMgramBot

Telegram BOT + LLM Encapsulation

The basic goal of this project is to create a bridge between a Telegram Bot and a Large Langage Model, like ChatGPT.

> The telegram interface handles special commands, and even some basic "chatty" prompts and reponses that don't require a LLM to interpret, like saying "Hello".
> The more dynamic conversation gets handed off to the LLM to manage prompts and responses, and Telegram acts as the interaction broker.
> The bot can also handle URLs. If you want the bot to interpret a URL, pass it a url [in brackets] and mention what you want the bot to do with it. (e.g. - What do  you think of this article? [https://some_site/article])

Using Telegram as the interface not only solves "exposing" the interface, but gives you boadloads of interactivity over a standard Command Line interface, or trying to create a website with input boxes and submit buttons to try to handle everything:
1. Telegram already lets you paste in verbose, multiline messages.
2. Telegram already lets you paste in pictures, videos, links, etc.
3. Telegram already lets you react with emojis, stickers, etc.

To function, the bot requires 3 API keys:
> OpenAI - To drive the actual GPT AI
> Tellegram Bot - Get via chatting with BotFather
> VirusTotal - To perform safety checks on URLs

To initialize the bot, install via pip (pip install TeLLMgramBot) and then import into your project.

Instantiate the bot passing in the various necessary configuration pieces:

telegram_bot = TeLLMgramBot.TelegramBot(
    bot_username=bot_uname,
    bot_nickname=bot_nick,
    bot_initials=bot_initials,
    bot_owner=bot_owner_uname,
    bot_owner_uid=bot_owner_uid,
    chatmodel=model,
    persona_name=bot_name,
    persona_prompt=starter_prompt
)

And then run by calling:
telegram_bot.start_polling()

Once you see "Polling..." the bot is online - switch to Tellegram and initiate a conversation with your bot there, and pass it the /start command.

The bot will only respond to the /start command coming from the bot_owner_uid of the owner specified. 
