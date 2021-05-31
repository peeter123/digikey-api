import os
import json


class DigikeyApiConfig:
    def __init__(self, file_name):
        self.file_name = file_name
        # Get config from file if it exists
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {}

    def save(self):
        with open(self.file_name, 'w') as f:
            json.dump(self.config, f)

    def get(self, what: str):
        if what in self.config:
            return self.config[what]
        return None

    def set(self, what: str, to):
        self.config[what] = to
