import os
import re
from unittest import TestCase
from pathlib import Path

import responses

from digikey import oauth2
from . import fixtures


class Oauth2Tests(TestCase):
    def setUp(self):
        self.old_token_storage_path = os.getenv('DIGIKEY_STORAGE_PATH', "")
        self.old_client_id = os.getenv('DIGIKEY_CLIENT_ID', "")
        self.old_client_secret = os.getenv('DIGIKEY_CLIENT_SECRET', "")

    def tearDown(self):
        os.environ['DIGIKEY_STORAGE_PATH'] = self.old_token_storage_path
        os.environ['DIGIKEY_CLIENT_ID'] = self.old_client_id
        os.environ['DIGIKEY_CLIENT_SECRET'] = self.old_client_secret

    @responses.activate
    def test_authentication(self):
        """Tests that `match` returns part matches"""
        # Mock out all calls to match endpoint.
        url_auth = re.compile(r'https://sso.digikey.com/as/authorization.oauth2.*')
        responses.add(
            responses.GET,
            url_auth,
            status=200,
            content_type='application/json'
        )

        url_regex_token = 'https://sso.digikey.com/as/token.oauth2'

        token = oauth2.TokenHandler()
