import os

def ensure_config_files():

    if not os.path.exists('config.yaml'):
        # Create a basic config.yaml file
        with open('config.yaml', 'w') as config_file:
            config_file.write('bot_uname: \n')
            config_file.write('bot_uid_owner: \n')
            config_file.write('bot_creator: \n')
            config_file.write('bot_name: Friendly Bot\n')
            config_file.write('bot_nickname: Botty\n')
            config_file.write('bot_initials: FB\n')
            config_file.write('model: gpt-3.5-turbo\n')

    if not os.path.exists('openai.key'):
        # Create a basic openai.key file
        with open('openai.key', 'w') as openai_key_file:
            openai_key_file.write('YOUR_OPENAI_KEY_HERE - https://platform.openai.com/account/api-keys\n')

    if not os.path.exists('telegram.key'):
        # Create a basic telegram.key file
        with open('telegram.key', 'w') as telegram_key_file:
            telegram_key_file.write('YOUR_TELEGRAM_KEY_HERE - https://core.telegram.org/api\n')

    if not os.path.exists('virustotal.key'):
        # Create a basic openai.key file
        with open('virustotal.key', 'w') as openai_key_file:
            openai_key_file.write('YOUR_VIRUSTOTAL_KEY_HERE - https://www.virustotal.com/gui/user/RoninATX/apikey\n')


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

def load_secrets():
    secrets = {
        'TELLMGRAMBOT_TELEGRAM_API_KEY': 'telegram.key',
        'TELLMGRAMBOT_OPENAI_API_KEY': 'openai.key',
        'TELLMGRAMBOT_VIRUSTOTAL_API_KEY': 'virustotal.key'
    }

    for env_var, key_file in secrets.items():
        if os.environ.get(env_var) is None:
            try:
                with open(os.path.join(os.environ['TELLMGRAMBOT_APP_PATH'], key_file), 'r') as f:
                    os.environ[env_var] = f.read().strip()
                    print(f"Loaded secret for {env_var}")
            except FileNotFoundError:
                print(f"Key file not found for {env_var}")
            except Exception as e:
                print(f"An error occurred while loading {env_var}: {e}")

if __name__ == '__main__':
    ensure_directories()
    ensure_config_files()
    load_secrets()
