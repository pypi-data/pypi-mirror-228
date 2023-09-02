# message_handlers.py
import os
import re
from typing import Optional

import openai
import validators

from .web_utils import fetch_url, strip_html_markup, InvalidURLException, InsecureURLException, SusURLException


def handle_greetings(text: str) -> Optional[str]:
    # Make TeLLMgramBot respond from single word greetings
    # Example: User says 'hello...?' -> Bot responds 'Hello!'
    greetings = {'Hello', 'Hi', 'Heya', 'Sup', 'Yo'}
    word = re.sub(r'[^\w\s]', '', text.title())
    if word in greetings:
        return f'{word}!'
    return None


def handle_common_queries(text: str) -> Optional[str]:
    if text.startswith('how you doin'):
        return 'How YOU doin?'
    elif text.startswith("I'm not your friend, buddy"):
        return "I'm not your buddy, guy."
    elif text.startswith("I'm not your guy, pal"):
        return "I'm not your pal, friend."
    return None


async def handle_url_ask(text: str) -> Optional[str]:
    # Check if the message contains a URL, but only if the url is wrapped in square brackets []
    url_match = re.search(r'\[http(s)?://\S+]', text)

    if url_match:
        # Extract the URL from the message, but not the square brackets
        url = url_match.group()[1:-1]

        # Fetch the URL content
        try:
            # Fetch the URL content, stripping the HTML markup. The function handles ensuring the URL is valid and safe
            url_content = strip_html_markup(await fetch_url(url))

            # Check if the URL is valid real quick
            if not validators.url(url):
                raise InvalidURLException(f'Invalid URL Parsed by message_handlers.handle_url_ask(): {url}')

            # We have a budget of 8k tokens with the GPT4 model we want to use, so lets see how big the content is
            # by encoding it to UTF-8 and getting the length in bytes
            content_size = len(url_content.encode('utf-8'))

            # If the content is too big, we need to prune it down to a reasonable size. Each token is 4 bytes, so we
            # need to divide the max token count by 4 to get the max byte count. Let's reserve 2000 bytes (500 tokens)
            # for the prompt and the rest for the content
            lenghty_url = False
            pruned_tail = None
            if content_size > 30000:
                # Prune the content
                url_content = url_content[:30000]
                pruned_tail = url_content[-50:]
                lenghty_url = True

            # Load our prompt template for URL analysis
            with open(os.path.join(os.environ['TELLMGRAMBOT_APP_PATH'], 'prompts', 'url_analysis.prmpt'), 'r') as f:
                template = f.read()

            # Substitute variables into the template
            formatted_prompt = template.format(url_content=url_content)

            # Let's build a messages list to pass to the OpenAI API, starting with the system message
            system_message = {"role": "system", "content": formatted_prompt}

            # Then adding the user message
            user_message = {"role": "user", "content": text}

            # Call the OpenAI API, using GPT-4, so we can get a larger token count to work with
            openai.api_key = os.environ['TELLMGRAMBOT_OPENAI_API_KEY']
            try:
                ask_results = openai.ChatCompletion.create(
                    model="gpt-4",
                    temperature=0.9,
                    messages=[system_message, user_message],
                )
                response = ask_results['choices'][0]['message']['content'].strip()
            except Exception as e:
                print(f"Error in calling OpenAI API: {e}")
                return "Something went wrong while fetching the URL. Please try again later."

            # If the URL content was too long, let the user know
            if lenghty_url:
                response += ('\n\n**Please note that URL content was too long, so I had to prune it down to a '
                             f'reasonable size. If the content after "{pruned_tail}" is crucial, you may need to let '
                             'me know and paste it here. **')
            return response

        except InvalidURLException:
            return "The URL you provided appears to be invalid. Could you please check it and try again?"
        except InsecureURLException:
            return ("The URL you provided is not secure. For safety reasons, I can't fetch its content. Could you "
                    "please try another URL, or just pasting the relevant content here?")
        except SusURLException:
            return ("The URL you provided is potentially unsafe, based on my internal scans.  I would be careful about "
                    "opening it. You can check the safety of URLS using this site: "
                    "https://www.virustotal.com/gui/home/url")
        except Exception as e:
            return f"Something went wrong while fetching the URL: {e}"

    return None
