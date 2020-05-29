"""
Top-level API, provides access to the Digikey API for product_information
without directly instantiating a client object.
Also wraps the response JSON in types that provide easier access
to various fields.
"""

import os, logging
import digikey.oauth.oauth2
import digikey.v3.productinformation as dpi
from digikey.v3.productinformation.rest import ApiException


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

    def product_details(self, digi_key_part_number, **kwargs):
        authorization = self._digikeyApiTokenObject.get_authorization()
        x_digikey_client_id = os.getenv('DIGIKEY_CLIENT_ID')
        try:
            api_response = self._api_instance.products_digi_key_part_number_get(
                digi_key_part_number,
                authorization,
                x_digikey_client_id,
                **kwargs)

            return api_response
        except ApiException as e:
            print("Exception when calling digikey_productinformation->product_details: %s\n" % e)
            return {}

    def keyword_search(self, query: str, st: int = 0, lim: int = 10, **kwargs):
        authorization = self._digikeyApiTokenObject.get_authorization()
        x_digikey_client_id = os.getenv('DIGIKEY_CLIENT_ID')

        search_request = dpi.KeywordSearchRequest(keywords=query, record_start_position=st, record_count=lim, **kwargs)

        try:
            api_response = self._api_instance.products_keyword_post(
                authorization,
                x_digikey_client_id,
                body=search_request
            )

            return api_response
        except ApiException as e:
            print("Exception when calling digikey_productinformation->keyword_search: %s\n" % e)
            return {}