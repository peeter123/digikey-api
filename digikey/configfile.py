import os
import json


class DigikeyBaseConfig:
    """
        Base class for a configuration handler which saves info related to Digikey's API like the client-ID
        This class must not be directly used, instead another class that inherits this class. The class that inherits
        this class must override save(), get(), and set() with the same parameters and returns.
        Check out DigikeyJsonConfig for more details as to how to do this.
    """
    def __init__(self):
        pass

    def save(self):
        pass

    def get(self, key: str):
        pass

    def set(self, key: str, val: str):
        pass


class DigikeyJsonConfig(DigikeyBaseConfig):
    def __init__(self, file_name):
        super().__init__()
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

    def get(self, key: str):
        if key in self.config:
            return self.config[key]
        return None

    def set(self, key: str, val: str):
        self.config[key] = val
