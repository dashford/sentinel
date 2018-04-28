class Message:
    def __init__(self):
        self._message = {}

    def get_message(self):
        return self._message

    def add_key_value(self, key, value):
        self._message[key] = value
