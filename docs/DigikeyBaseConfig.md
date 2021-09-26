# Digikey-API Settings Storage Configuration

The `DigikeyAPI` class of the V3 API must be given a configuration class as one of it's arguments. 
The purpose of this configuration class is to determine how the API will store some settings like the client-id, client-secret, and other stuff. 

As of right now, there is only 1 available configuration class which is `DigikeyJsonConfig`. Of course you can create your own configurator class and input that into `DigikeyAPI`, for example if you want the API to store it's configuration in a database.

## DigikeyJsonConfig

This configuration classes stores the API settings in a JSON file. When initializing this class, a file name/path must be given.

Example:
```python
dk_config = digikey.DigikeyJsonConfig(file_name='test_conf.json')
dk_config.set('client-id', 'ENTER_CLIENT_ID')
dk_config.set('client-secret', 'ENTER_CLIENT_SECRET')
```

## Create your own storage configuration

You can create your own storage configurator as mentioned to define how to store the API's settings. The `DigikeyBaseConfig` class can be inherited to create it. You must override and define 3 functions:

- save(self): This function gets called when the API wants to save the settings.
- get(self, key: str): This function gets called when the API wants to retrieve a value for a given key. Return `None` if it doesn't exist
- set(self, key: str, val: str): This function gets called when the API wants to store a value for a given key.

As an example, this is how `DigikeyJsonConfig` is implemented:
```python
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
```
