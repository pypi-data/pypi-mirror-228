# Utility Functions
import re
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