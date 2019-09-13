import os
import re
import ssl
import urllib.request
import urllib.parse as urlparse
from webbrowser import open_new
from unittest import TestCase
import unittest.mock as mock
from pathlib import Path
import threading

import requests
import responses

from digikey import oauth2
from . import fixtures


def mock_open_new(url):
    parsed = urlparse.parse_qs(urlparse.urlparse(url).query)
    assert parsed['client_id'][0] == 'MOCK_CLIENT_ID'
    assert parsed['redirect_uri'][0] == 'https://localhost:8080/digikey_callback'

    # Call the redirect URI
    values = {'code': 'MOCK_AUTH_CODE'}
    data = urllib.parse.urlencode(values)
    req = parsed['redirect_uri'][0] + '?' + data
    threading.Thread(target=lambda: urllib.request.urlopen(req, context=ssl._create_unverified_context())).start()
    pass


class Oauth2Tests(TestCase):
    def setUp(self):
        self.old_token_storage_path = os.getenv('DIGIKEY_STORAGE_PATH', "")
        self.old_client_id = os.getenv('DIGIKEY_CLIENT_ID', "")
        self.old_client_secret = os.getenv('DIGIKEY_CLIENT_SECRET', "")

        os.environ['DIGIKEY_STORAGE_PATH'] = str(Path(__file__).parent)
        os.environ['DIGIKEY_CLIENT_ID'] = 'MOCK_CLIENT_ID'
        os.environ['DIGIKEY_CLIENT_SECRET'] = 'MOCK_CLIENT_SECRET'

    def tearDown(self):
        os.environ['DIGIKEY_STORAGE_PATH'] = self.old_token_storage_path
        os.environ['DIGIKEY_CLIENT_ID'] = self.old_client_id
        os.environ['DIGIKEY_CLIENT_SECRET'] = self.old_client_secret

    @responses.activate
    @mock.patch('digikey.oauth2.open_new', side_effect=mock_open_new)
    def test_authentication(self, mock_on):
        """Tests that token is retrieved correctly from authorization"""
        print('Tests that token is retrieved correctly from authorization')

        # Mock out all calls to token endpoint.
        url_auth = re.compile(r'https://sso.digikey.com/as/token.oauth2.*')
        responses.add(
            responses.POST,
            url_auth,
            status=200,
            content_type='application/json',
            json=fixtures.oauth2_response
        )

        token = oauth2.TokenHandler().get_access_token()
        assert token.access_token == 'MOCK_ACCESS'
        assert token.refresh_token == 'MOCK_REFRESH'

        tokenfile = Path(os.getenv('DIGIKEY_STORAGE_PATH', "")).joinpath(oauth2.TOKEN_STORAGE)
        cacert = Path(os.getenv('DIGIKEY_STORAGE_PATH', "")).joinpath(oauth2.CA_CERT)
        pemfile = Path(os.getenv('DIGIKEY_STORAGE_PATH', "")).joinpath('localhost.pem')

        # Test if temporary files have been cleaned up
        assert not cacert.is_file()
        assert not pemfile.is_file()

        # Test if token has been saved
        assert tokenfile.is_file()
        os.remove(tokenfile)
