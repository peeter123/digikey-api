import json
from json import JSONDecodeError
from pathlib import Path

oauth2_response = None
try:
    with open(Path(__file__).resolve().parent.joinpath('responses/oauth2_response.json'), 'r') as f:
        oauth2_response = json.load(f)
except (EnvironmentError, JSONDecodeError):
    print('Token response does not exist or malformed')
