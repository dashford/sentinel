import json


class JsonFormatter:
    def __init__(self):
        pass

    def format(self, message):
        return json.dumps(message)
