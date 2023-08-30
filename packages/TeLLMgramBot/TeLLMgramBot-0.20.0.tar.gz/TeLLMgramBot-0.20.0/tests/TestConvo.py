import unittest

from conversation import Conversation  # Assuming the class is defined in a file named conversation.py


class TestConversation(unittest.TestCase):

    def setUp(self):
        self.max_tokens = 4000
        self.threshold = 0.75
        self.convo = Conversation('System Context', 'SessionLogs/ConvoTest.log')

    def test_add_user_message(self):
        initial_len = len(self.convo.messages)
        self.convo.add_user_message('Test user message')
        self.assertEqual(len(self.convo.messages), initial_len + 1)

    def test_add_assistant_message(self):
        initial_len = len(self.convo.messages)
        self.convo.add_assistant_message('Test assistant message')
        self.assertEqual(len(self.convo.messages), initial_len + 1)

    def test_prune_conversation(self):
        # Add messages until you exceed the pruning threshold
        while sum(len(message["content"].encode('utf-8')) for message in
                  self.convo.messages) < self.max_tokens * 4 * self.threshold:
            self.convo.add_user_message('Adding a message to exceed the limit.')
            self.convo.add_assistant_message('Adding another message to exceed the limit.')

        initial_len = len(self.convo.messages)
        self.convo.prune_conversation(self.max_tokens, self.threshold)

        # Check if conversation was pruned
        self.assertTrue(len(self.convo.messages) < initial_len)


if __name__ == '__main__':
    unittest.main()
