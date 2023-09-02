# Utility Functions
import re
import os
from datetime import datetime

import yaml


# File Name Friendly Timestamp
def get_timestamp():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    return timestamp
# File Name Friendly UserName
def get_safe_username(username: str) -> str:
    # Remove leading '@' and any other special characters you want to exclude
    return re.sub(r'[^\w\s]', '', username.lstrip('@'))

# Basic open text file function
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Read the YAML configuration file
def read_config(file_path):
    with open(file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config
    
# Read a plain text .prmpt file
def fetch_prompt(file_path):
    with open(file_path, 'r') as prompt_file:
        prompt = prompt_file.read()
    return prompt

# Generate a Chat Session Log filename
def generate_filename(bot_uid: str, user_uid: str) -> str:
    timestamp = get_timestamp()
    return f'{bot_uid}_{user_uid}_{timestamp}.log'

# ToDo: Add a function to log error messages to a file including an error type and timestamp
def log_error(error: Exception or str, error_type: str, error_filename: str) -> None:
    """

    :rtype: object
    """
    timestamp = get_timestamp()
    with open(error_filename, 'a') as error_file:
        error_file.write(f'{timestamp} {error_type}: {error}\n')
        # Also print the error to the console
        print(f'{timestamp} {error_type}: {error}')

# Checks for TeLLMgramBot directories and creates them as necessary
def ensure_directories():
    app_base_path = os.environ.get('TELLMGRAMBOT_APP_PATH', os.getcwd())

    # Update the environment variable with the cleaned-up path
    os.environ['TELLMGRAMBOT_APP_PATH'] = app_base_path

    # Create necessary directories
    directories = [
        os.path.join(app_base_path, 'sessionlogs'),
        os.path.join(app_base_path, 'errorlogs'),
        os.path.join(app_base_path, 'prompts'),
        # Add more as needed
    ]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

# Investigates three key files needed for the TeLLMgramBot
def ensure_keys():
    # List the key file and the URL if it does not exist for more information
    key_files = {
        'openai.key'     : 'https://platform.openai.com/account/api-keys',
        'telegram.key'   : 'https://core.telegram.org/api',
        'virustotal.key' : 'https://developers.virustotal.com/reference/overview'
    }

    # Create key files and environment variables for other libraries
    for key_file, url in key_files.items():
        path    = os.path.join(os.environ['TELLMGRAMBOT_APP_PATH'], key_file)
        key     = re.sub("\..+", "", key_file).upper() # Uppercase with .key removed
        env_var = f"TELLMGRAMBOT_{key}_API_KEY"

        # Ensures the specified key file is created and populated by user
        if not os.path.exists(path):
            # Create a basic ~.key file
            with open(path, 'w') as f:
                f.write(f"YOUR {key} API KEY HERE - {url}\n")

        # Set environment variable for each key by destination
        if os.environ.get(env_var) is None:
            try:
                with open(path, 'r') as f:
                    os.environ[env_var] = f.read().strip()
                    print(f"Loaded secret for {env_var}")
            except FileNotFoundError:
                print(f"Key file not found for {env_var}")
            except Exception as e:
                print(f"An error occurred while loading {env_var}: {e}")