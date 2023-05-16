import json
import logging
import os
import ssl
import typing as t
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from json.decoder import JSONDecodeError
from pathlib import Path
from urllib.parse import urlencode, urlparse, parse_qs
from webbrowser import open_new

import requests
from certauth.certauth import CertificateAuthority

from digikey.constants import USER_AGENT
from digikey.exceptions import DigikeyOauthException

CA_CERT = 'digikey-api.pem'
TOKEN_STORAGE = 'token_storage.json'

AUTH_URL_V3_PROD = 'https://api.digikey.com/v1/oauth2/authorize'
TOKEN_URL_V3_PROD = 'https://api.digikey.com/v1/oauth2/token'

AUTH_URL_V3_SB = 'https://sandbox-api.digikey.com/v1/oauth2/authorize'
TOKEN_URL_V3_SB = 'https://sandbox-api.digikey.com/v1/oauth2/token'

REDIRECT_URI = 'https://localhost:8139/digikey_callback'
PORT = 8139

logger = logging.getLogger(__name__)


class Oauth2Token:
    def __init__(self, token):
        self._token = token

    @property
    def access_token(self):
        return self._token.get('access_token')

    @property
    def refresh_token(self):
        return self._token.get('refresh_token')

    @property
    def expires(self):
        return datetime.fromtimestamp(self._token.get('expires'), timezone.utc)

    @property
    def type(self):
        return self._token.get('token_type')

    def expired(self) -> bool:
        return datetime.now(timezone.utc) >= self.expires

    def get_authorization(self) -> str:
        return self.type + ' ' + self.access_token

    def __repr__(self):
        return '<Token: expires={}>'.format(self.expires.astimezone().isoformat())


class HTTPServerHandler(BaseHTTPRequestHandler):
    """
    HTTP Server callbacks to handle Digikey OAuth redirects
    """
    def __init__(self, request, address, server, a_id, a_secret):
        self.app_id = a_id
        self.app_secret = a_secret
        self.auth_code = None
        super().__init__(request, address, server)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        get_params = parse_qs(urlparse(self.path).query)
        if 'code' in get_params:
            self.auth_code = get_params['code'][0]
            self.wfile.write(bytes('<html>' +
                                   '<body>'
                                   '<h1>You may now close this window.</h1>' +
                                   '<p>Auth code retreived: ' + self.auth_code + '</p>'
                                   '</body>'
                                   '</html>', 'utf-8'))
            self.server.auth_code = self.auth_code
            self.server.stop = 1
        else:
            raise DigikeyOauthException('Digikey did not return authorization token in request: {}'.format(self.path))

    # Disable logging from the HTTP Server
    def log_message(self, format, *args):
        return


class TokenHandler:
    """
    Functions used to handle Digikey oAuth
    """
    def __init__(self,
                 a_id: t.Optional[str] = None,
                 a_secret: t.Optional[str] = None,
                 a_token_storage_path: t.Optional[str] = None,
                 version: int = 2,
                 sandbox: bool = False):

        if version == 3:
            if sandbox:
                self.auth_url = AUTH_URL_V3_SB
                self.token_url = TOKEN_URL_V3_SB
            else:
                self.auth_url = AUTH_URL_V3_PROD
                self.token_url = TOKEN_URL_V3_PROD
        else:
            raise ValueError('Please specify the correct Digikey API version')

        logger.debug(f'Using API V{version}')

        a_id = a_id or os.getenv('DIGIKEY_CLIENT_ID')
        a_secret = a_secret or os.getenv('DIGIKEY_CLIENT_SECRET')
        if not a_id or not a_secret:
            raise ValueError(
                'CLIENT ID and SECRET must be set. '
                'Set "DIGIKEY_CLIENT_ID" and "DIGIKEY_CLIENT_SECRET" '
                'as an environment variable, or pass your keys directly to the client.'
            )

        a_token_storage_path = a_token_storage_path or os.getenv('DIGIKEY_STORAGE_PATH')
        if not a_token_storage_path or not Path(a_token_storage_path).exists():
            raise ValueError(
                'STORAGE PATH must be set and must exist.'
                'Set "DIGIKEY_STORAGE_PATH" as an environment variable, '
                'or pass your keys directly to the client.'
            )

        self._id = a_id
        self._secret = a_secret
        self._storage_path = Path(a_token_storage_path)
        self._token_storage_path = self._storage_path.joinpath(TOKEN_STORAGE)
        self._ca_cert = self._storage_path.joinpath(CA_CERT)

    def __generate_certificate(self):
        ca = CertificateAuthority('Python digikey-api CA', str(self._ca_cert), cert_cache=str(self._storage_path))
        return ca.cert_for_host('localhost')

    def __build_authorization_url(self) -> str:
        params = {'client_id': self._id,
                  'response_type': 'code',
                  'redirect_uri': REDIRECT_URI
                  }
        url = self.auth_url + '?' + urlencode(params)
        logger.debug(f'AUTH - Authenticating with endpoint {self.auth_url} using ID: {self._id[:-5]}...')
        logger.debug(f'AUTH - Redirect URL: {REDIRECT_URI}')
        return url

    def __exchange_for_token(self, code):
        headers = {'user-agent': USER_AGENT,
                   'Content-type': 'application/x-www-form-urlencoded'
                   }
        post_data = {'grant_type': 'authorization_code',
                     'code': code,
                     'client_id': self._id,
                     'client_secret': self._secret,
                     'redirect_uri': REDIRECT_URI
                     }

        try:
            logger.debug(f'TOKEN - Exchanging {code} auth code for token at endpoint: {self.token_url}')
            logger.debug(f'TOKEN - Using client id: {self._id[:-5]}...')
            logger.debug(f'TOKEN - Using client secret: {self._secret[:-5]}...')
            r = requests.post(self.token_url, headers=headers, data=post_data)
            r.raise_for_status()
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
            raise DigikeyOauthException('TOKEN - Cannot request new token with auth code: {}'.format(e))
        else:
            token_json = r.json()
            logger.debug(f'TOKEN - Got access token with value: {token_json["access_token"][:-5]}...')
            logger.info('TOKEN - Successfully retrieved access token.')

        # Create epoch timestamp from expires in, with 1 minute margin
        token_json['expires'] = int(token_json['expires_in']) + datetime.now(timezone.utc).timestamp() - 60
        return token_json

    def __refresh_token(self, refresh_token: str):
        headers = {'user-agent': USER_AGENT,
                   'Content-type': 'application/x-www-form-urlencoded'
                   }
        post_data = {'grant_type': 'refresh_token',
                     'refresh_token': refresh_token,
                     'client_id': self._id,
                     'client_secret': self._secret
                     }
        error_message = None

        try:
            r = requests.post(self.token_url, headers=headers, data=post_data)
            error_message = r.json().get('error_description', None)
            r.raise_for_status()
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
            raise DigikeyOauthException('REFRESH - Cannot request new token with refresh token: {}.'.format(error_message))
        else:
            token_json = r.json()
            logger.debug(f'REFRESH - Got access token with value: {token_json["access_token"]}')
            logger.info('REFRESH - Successfully retrieved access token.')

        # Create epoch timestamp from expires in, with 1 minute margin
        token_json['expires'] = int(token_json['expires_in']) + datetime.now(timezone.utc).timestamp() - 60
        return token_json

    def save(self, json_data):
        with open(self._token_storage_path, 'w') as f:
            json.dump(json_data, f)
            logger.debug('Saved token to: {}'.format(self._token_storage_path))

    def get_access_token(self) -> Oauth2Token:
        """
         Fetches the access key using an HTTP server to handle oAuth
         requests
            Args:
                appId:      The assigned App ID
                appSecret:  The assigned App Secret
        """

        # Check if a token already exists on the storage
        token_json = None
        try:
            with open(self._token_storage_path, 'r') as f:
                token_json = json.load(f)
        except (EnvironmentError, JSONDecodeError):
            logger.warning('Oauth2 token storage does not exist or malformed, creating new.')

        token = None
        if token_json is not None:
            token = Oauth2Token(token_json)

        # Try to refresh the credentials with the stores refresh token
        if token is not None and token.expired():
            try:
                logger.debug(f'REFRESH - Current token is stale, refresh using: {token.refresh_token}')
                token_json = self.__refresh_token(token.refresh_token)
                self.save(token_json)
            except DigikeyOauthException:
                logger.error('REFRESH - Failed to use refresh token, starting new authorization flow.')
                token_json = None

        # Obtain new credentials using the Oauth flow if no token stored or refresh fails
        if token_json is None:
            open_new(self.__build_authorization_url())
            filename = self.__generate_certificate()
            httpd = HTTPServer(
                    ('localhost', PORT),
                    lambda request, address, server: HTTPServerHandler(
                        request, address, server, self._id, self._secret))
            httpd.socket = ssl.wrap_socket(httpd.socket, certfile=str(Path(filename)), server_side=True)
            httpd.stop = 0

            # This function will block until it receives a request
            while httpd.stop == 0:
                httpd.handle_request()
            httpd.server_close()

            # Remove generated certificate
            try:
                os.remove(Path(filename))
                os.remove(self._ca_cert)
            except OSError as e:
                logger.error('Cannot remove temporary certificates: {}'.format(e))

            # Get the acccess token from the auth code
            token_json = self.__exchange_for_token(httpd.auth_code)

            # Save the newly obtained credentials to the filesystem
            self.save(token_json)

        return Oauth2Token(token_json)
