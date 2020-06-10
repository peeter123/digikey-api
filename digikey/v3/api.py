import os
import types
import wrapt
import logging
import digikey.oauth.oauth2
import digikey.v3.productinformation as dpi
from digikey.v3.productinformation import KeywordSearchRequest, KeywordSearchResponse, ProductDetails, PartSearchApi
from digikey.v3.productinformation.rest import ApiException

logger = logging.getLogger(__name__)


class ProductApiWrapper(object):
    def __init__(self, wrapped_function):
        # Configure API key authorization: apiKeySecurity
        configuration = dpi.Configuration()
        configuration.api_key['X-DIGIKEY-Client-Id'] = os.getenv('DIGIKEY_CLIENT_ID')
        # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
        # configuration.api_key_prefix['X-DIGIKEY-Client-Id'] = 'Bearer'

        # Configure OAuth2 access token for authorization: oauth2AccessCodeSecurity
        configuration = dpi.Configuration()
        self._digikeyApiTokenObject = digikey.oauth.oauth2.TokenHandler(version=3).get_access_token()
        configuration.access_token = self._digikeyApiTokenObject.access_token

        # create an instance of the API class
        self._api_instance = dpi.PartSearchApi(dpi.ApiClient(configuration))

        # Populate reused ids
        self.authorization = self._digikeyApiTokenObject.get_authorization()
        self.x_digikey_client_id = os.getenv('DIGIKEY_CLIENT_ID')

        self.wrapped_function = wrapped_function

    @staticmethod
    def _print_remaining_requests(header):
        try:
            rate_limit = header['X-RateLimit-Limit']
            rate_limit_rem = header['X-RateLimit-Remaining']
            logger.debug('Requests remaining: [{}/{}]'.format(rate_limit_rem, rate_limit))
        except KeyError:
            pass

    @wrapt.decorator
    def __call__(self, wrapped, instance, args, kwargs):
        try:
            func = getattr(self._api_instance, self.wrapped_function)
            wrapped(*args, **kwargs)
            api_response = func(*args, self.authorization, self.x_digikey_client_id, **kwargs)
            self._print_remaining_requests(api_response[2])
            return api_response[0]
        except ApiException as e:
            logger.error(f'Exception when calling {self.wrapped_function}: {e}')


@ProductApiWrapper('products_keyword_post_with_http_info')
def keyword_search(**kwargs) -> KeywordSearchResponse:
    if 'body' in kwargs:
        logger.debug('CALL -> keyword_search')
        logger.info(f'Search for: {kwargs["body"].keywords}')


@ProductApiWrapper('products_digi_key_part_number_get_with_http_info')
def part_number(*args, **kwargs) -> ProductDetails:
    if len(args):
        logger.debug('CALL -> part_number')
        logger.info(f'Get product details for: {args[0]}')

