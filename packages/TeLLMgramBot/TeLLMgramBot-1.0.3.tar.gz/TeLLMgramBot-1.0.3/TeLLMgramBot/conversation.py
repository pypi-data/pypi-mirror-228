import os


class Conversation:
    def __init__(self, system_content, interaction_log_path):

        # Orient to the base app path for TellMgramBot no matter what sub folder I'm coming from
        if not os.environ.get('TELLMGRAMBOT_APP_PATH'):
            current_path = os.environ['TELLMGRAMBOT_APP_PATH'] = os.getcwd()
            # Find the index of the app name in the path
            app_index = current_path.find("TeLLMgramBot")
            base_path = current_path[:app_index + len("TeLLMgramBot")]
            os.environ['TELLMGRAMBOT_APP_PATH'] = base_path

        self.system_content = system_content
        self.interaction_log: str = os.path.join(os.environ['TELLMGRAMBOT_APP_PATH'],
                                                 'sessionlogs', interaction_log_path)
        self.messages = [{"role": "system", "content": system_content}]

    def change_system_content(self, new_content):
        self.system_content = new_content
        self.messages[0] = {"role": "system", "content": new_content}

    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})
        self.write_interaction(role="user", content=content)

    def add_assistant_message(self, content):
        self.messages.append({"role": "assistant", "content": content})
        self.write_interaction(role="assistant", content=content)

    def get_openai_messages(self):
        return self.messages

    # This also fixes UTF-8 and accounts for other symbols available
    def write_interaction(self, role, content):
        mode = 'w' if not os.path.exists(self.interaction_log) else 'a'
        with open(self.interaction_log, mode, encoding='utf-8') as file:
            file.write(f'{role}: {content}\n')

    def prune_conversation(self, max_tokens, threshold):
        # Todo: This should really be evaluating Tokens but bytes will work for now. 1 token = 4 bytes
        byte_size_ceiling = max_tokens * 4 * threshold
        current_convo_size = sum(len(message["content"].encode('utf-8')) for message in self.messages)
        # Keeep popping messages off the stack until our size is below the threshold
        while current_convo_size > byte_size_ceiling:
            popped_message = self.messages.pop(1)
            popped_message_len = len(popped_message["content"].encode('utf-8'))
            current_convo_size -= popped_message_len
