"""
Top-level API, provides access to the Digikey API for product_information
without directly instantiating a client object.
Also wraps the response JSON in types that provide easier access
to various fields.
"""

import re
import os
import logging
import digikey.oauth.oauth2
import digikey.v3.productinformation as dpi
from digikey.v3.productinformation import KeywordSearchRequest, KeywordSearchResponse, ProductDetails
from digikey.v3.productinformation.rest import ApiException

logger = logging.getLogger(__name__)


def _print_remaining_requests(header):
    try:
        rate_limit = header['X-RateLimit-Limit']
        rate_limit_rem = header['X-RateLimit-Remaining']
        logger.debug('Requests remaining: [{}/{}]'.format(rate_limit_rem, rate_limit))
    except KeyError:
        pass


class ProductInformation:
    def __init__(self):
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
        self._api_instance = dpi.PartSearchApi(
            dpi.ApiClient(configuration))

        # Populate reused ids
        self.authorization = self._digikeyApiTokenObject.get_authorization()
        self.x_digikey_client_id = os.getenv('DIGIKEY_CLIENT_ID')

    def product_details(self, digi_key_part_number: str, **kwargs) -> ProductDetails:
        logger.debug(f'Get product details for: {digi_key_part_number}')

        try:
            api_response = self._api_instance.products_digi_key_part_number_get_with_http_info(
                digi_key_part_number,
                self.authorization,
                self.x_digikey_client_id,
                **kwargs)

            _print_remaining_requests(api_response[2])

            return api_response[0]
        except ApiException as e:
            logger.error(f'Exception when calling digikey_productinformation->product_details: {e}')
            return ProductDetails()

    def keyword_search(self, search_request: KeywordSearchRequest, **kwargs) -> KeywordSearchResponse:
        logger.debug(f'Search for: {search_request.keywords}')

        if search_request.record_count is None:
            search_request.record_count = 10

        try:
            api_response = self._api_instance.products_keyword_post_with_http_info(
                self.authorization,
                self.x_digikey_client_id,
                body=search_request,
                **kwargs
            )

            _print_remaining_requests(api_response[2])

            return api_response[0]
        except ApiException as e:
            logger.error(f'Exception when calling digikey_productinformation->keyword_search: {e}')
            return KeywordSearchResponse()