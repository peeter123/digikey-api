import logging
import os
import re
import ssl
import json
import sys
import urllib.request
import urllib.parse as urlparse
from json.decoder import JSONDecodeError
from unittest import TestCase
import unittest.mock as mock
from pathlib import Path
from datetime import datetime, timezone
import threading

import responses

from digikey.oauth import oauth2
from . import fixtures

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG


def mock_open_new(url):
    parsed = urlparse.parse_qs(urlparse.urlparse(url).query)
    assert parsed['client_id'][0] == 'MOCK_CLIENT_ID'
    assert parsed['redirect_uri'][0] == 'https://localhost:8139/digikey_callback'

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

        self.stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(self.stream_handler)

    def tearDown(self):
        os.environ['DIGIKEY_STORAGE_PATH'] = self.old_token_storage_path
        os.environ['DIGIKEY_CLIENT_ID'] = self.old_client_id
        os.environ['DIGIKEY_CLIENT_SECRET'] = self.old_client_secret

        logger.removeHandler(self.stream_handler)

    @responses.activate
    @mock.patch('digikey.oauth.oauth2.open_new', side_effect=mock_open_new)
    def test_authentication(self, mock_on):
        """Tests that token is retrieved correctly from authorization"""

        urls = {2: oauth2.TOKEN_URL_V2 + r'.*',
                3: oauth2.TOKEN_URL_V3_PROD + r'.*'}

        for version in [2, 3]:
            logger.info(f'Tests that token is retrieved correctly from authorization [API V{version}]')

            # Mock out all calls to token endpoint.
            url_auth = re.compile(urls[version])
            responses.add(
                responses.POST,
                url_auth,
                status=200,
                content_type='application/json',
                json=fixtures.oauth2_response
            )

            token = oauth2.TokenHandler(version=version).get_access_token()
            assert token.access_token == 'MOCK_ACCESS'
            assert token.refresh_token == 'MOCK_REFRESH'
            expires_in = (token.expires - datetime.now(timezone.utc)).seconds
            assert 86200 <= expires_in <= 86340

            token_file = Path(os.getenv('DIGIKEY_STORAGE_PATH', "")).joinpath(oauth2.TOKEN_STORAGE)
            cacert = Path(os.getenv('DIGIKEY_STORAGE_PATH', "")).joinpath(oauth2.CA_CERT)
            pemfile = Path(os.getenv('DIGIKEY_STORAGE_PATH', "")).joinpath('localhost.pem')

            # Test if temporary files have been cleaned up
            assert not cacert.is_file()
            assert not pemfile.is_file()

            # Test if token has been saved
            assert token_file.is_file()

            # Test for correct storage
            token_json = None
            try:
                with open(token_file, 'r') as f:
                    token_json = json.load(f)
            except (EnvironmentError, JSONDecodeError):
                print('Token storage does not exist or malformed')
                assert False

            os.remove(token_file)

            assert token_json['access_token'] == 'MOCK_ACCESS'
            assert token_json['refresh_token'] == 'MOCK_REFRESH'
