import os
import ssl
import json
import requests
import logging
import typing as t
from datetime import datetime
from certauth.certauth import CertificateAuthority
from pathlib import Path
from json.decoder import JSONDecodeError
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlencode
from webbrowser import open_new
from digikey.exceptions import DigykeyOauthException

CA_CERT = 'digikey-api.pem'
TOKEN_STORAGE = 'token_storage.json'
AUTH_URL = 'https://sso.digikey.com/as/authorization.oauth2'
TOKEN_URL = 'https://sso.digikey.com/as/token.oauth2'
REDIRECT_URI = 'https://localhost:8080/digikey_callback'
PORT = 8080

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
        return datetime.fromtimestamp(self._token.get('expires'))

    @property
    def type(self):
        return self._token.get('token_type')

    def expired(self) -> bool:
        if datetime.now().timestamp() >= self.expires.timestamp():
            return True
        else:
            return False

    def get_authorization(self) -> str:
        return self.type + ' ' + self.access_token

    def __repr__(self):
        return '<Token: expires={}>'.format(self.expires.strftime('%c'))


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
        if 'code' in self.path:
            self.auth_code = self.path.split('=')[1]
            self.wfile.write(bytes('<html>' +
                                   '<body>'
                                   '<h1>You may now close this window.</h1>' +
                                   '<p>Auth code retreived: ' + self.auth_code + '</p>'
                                   '</body>'
                                   '</html>', 'utf-8'))
            self.server.auth_code = self.auth_code
            self.server.stop = 1

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
                 a_token_storage_path: t.Optional[str] = None):

        a_id = a_id or os.getenv('DIGIKEY_CLIENT_ID')
        a_secret = a_secret or os.getenv('DIGIKEY_CLIENT_SECRET')
        if not a_id or not a_secret:
            raise ValueError(
                "CLIENT ID and SECRET must be set. "
                "Set 'DIGIKEY_CLIENT_ID' and 'DIGIKEY_CLIENT_SECRET' "
                "as an environment variable, or pass your keys directly to the client."
            )

        a_token_storage_path = a_token_storage_path or os.getenv('DIGIKEY_STORAGE_PATH')
        if not a_token_storage_path or not Path(a_token_storage_path).exists():
            raise ValueError(
                "STORAGE PATH must be set and must exist."
                "Set 'DIGIKEY_STORAGE_PATH' as an environment variable, "
                "or pass your keys directly to the client."
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
        params = {"client_id": self._id,
                  "response_type": "code",
                  "redirect_uri": REDIRECT_URI
                  }
        url = AUTH_URL + '?' + urlencode(params)
        return url

    def __exchange_for_token(self, code):
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        post_data = {"grant_type": "authorization_code",
                     "code": code,
                     "client_id": self._id,
                     "client_secret": self._secret,
                     "redirect_uri": REDIRECT_URI
                     }
        try:
            r = requests.post(TOKEN_URL, headers=headers, data=post_data)
            r.raise_for_status()
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
            raise DigykeyOauthException('Cannot request new token with auth code: {}'.format(e))
        token_json = r.json()
        token_json['expires'] = int(token_json['expires_in']) + datetime.now().timestamp()
        return token_json

    def __refresh_token(self, refresh_token):
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        post_data = {"grant_type": "refresh_token",
                     "refresh_token": refresh_token,
                     "client_id": self._id,
                     "client_secret": self._secret
                     }
        try:
            r = requests.post(TOKEN_URL, headers=headers, data=post_data)
            r.raise_for_status()
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
            raise DigykeyOauthException('Cannot request new token with refresh token: {}'.format(e))
        token_json = r.json()
        token_json['expires'] = int(token_json['expires_in']) + datetime.now().timestamp()
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
            logger.warning('Token storage does not exist or malformed, creating new')

        token = None
        if token_json is not None:
            token = Oauth2Token(token_json)

        if token is not None:
            if not token.expired():
                return token
            else:
                return Oauth2Token(self.__refresh_token(token.refresh_token))
        else:
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

            # Save the credentials to the filesystem
            self.save(token_json)

            return Oauth2Token(token_json)
