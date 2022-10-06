# -*- coding: utf-8 -*-
# GPL license
#
# Copyright (C) 2021 by Salvador E. Tropea / Instituto Nacional de Tecnologia Industrial
#
import os
import re
import logging

import kicost_digikey_api_v3
from kicost_digikey_api_v3.v3.productinformation import ManufacturerProductDetailsRequest, KeywordSearchRequest
from .exceptions import DigikeyError

USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/22.0"
includes = ["DigiKeyPartNumber","ProductUrl","QuantityAvailable","MinimumOrderQuantity","PrimaryDatasheet","ProductStatus",
            "SearchLocaleUsed","StandardPricing","Parameters","RoHsStatus","AdditionalValueFee","ProductDescription"]
includes = ','.join(includes)


class PartSortWrapper(object):
    """ This class is used to sort the results giving more priority to entries with less MOQ, less price,
        more availability, etc. """
    def __init__(self, data):
        self.data = data
        self.min_price = data.standard_pricing[0].unit_price if len(data.standard_pricing) > 0 else -1
        if not hasattr(data, 'additional_value_fee'):
            data.additional_value_fee = 0

    def __eq__(self, other):
        return (self.data.minimum_order_quantity == other.data.minimum_order_quantity and
                self.data.quantity_available == other.data.quantity_available and
                self.data.additional_value_fee == other.data.additional_value_fee and
                self.min_price == other.min_price and
                self.data.product_status == other.data.product_status)

    def __lt__(self, other):
        if self.data.quantity_available and not other.data.quantity_available:
            return True
        if not self.data.minimum_order_quantity:
            return False
        if self.data.minimum_order_quantity < other.data.minimum_order_quantity:
            return True
        if self.min_price == -1:
            return False
        dif = self.data.additional_value_fee + self.min_price - (other.data.additional_value_fee + other.min_price)
        if dif < 0:
            return True
        if dif == 0 and self.data.product_status == 'Active' and other.data.product_status != 'Active':
            return True
        return False


class DK_API(object):
    ''' Configuration class, KiCost must extend it and provide an object with the desired options '''
    # Provided by KiCost
    id = secret = None
    sandbox = False
    api_ops = {}
    exclude_market_place_products = False
    # Configured here
    cache = None
    logger = logging.getLogger(__name__)
    extra_ops = {}  # Extra options for the API

    @staticmethod
    def _create_cache_name_suffix():
        suf = '_' + DK_API.extra_ops.get('x_digikey_locale_site', 'US')
        suf += '_' + DK_API.extra_ops.get('x_digikey_locale_language', 'en')
        suf += '_' + DK_API.extra_ops.get('x_digikey_locale_currency', 'USD')
        suf += '_' + DK_API.extra_ops.get('x_digikey_locale_ship_to_country', 'US')
        return suf

    @staticmethod
    def configure(cache, a_logger=None):
        ''' Configures the plug-in '''
        if a_logger:
            DK_API.logger = a_logger
            kicost_digikey_api_v3.v3.api.set_logger(a_logger)
            kicost_digikey_api_v3.oauth.oauth2.set_logger(a_logger)
        # Ensure we have a place to store the token
        DK_API.cache = cache
        cache_path = cache.path
        if not os.path.isdir(cache_path):
            raise DigikeyError("No directory to store tokens, please create `{}`".format(cache_path))
        os.environ['DIGIKEY_STORAGE_PATH'] = cache_path
        # Ensure we have the credentials
        if not DK_API.id or not DK_API.secret:
            raise DigikeyError("No Digi-Key credentials defined")
        os.environ['DIGIKEY_CLIENT_ID'] = DK_API.id
        os.environ['DIGIKEY_CLIENT_SECRET'] = DK_API.secret
        # Default to no sandbox
        os.environ['DIGIKEY_CLIENT_SANDBOX'] = str(DK_API.sandbox)
        # API options
        DK_API.extra_ops = {'x_digikey_'+op: val for op, val in DK_API.api_ops.items()}
        # Cache suffix (uses extra_ops)
        cache.suffix = DK_API._create_cache_name_suffix()
        # Debug information about what we got
        DK_API.logger.debug('Digi-Key API plug-in options:')
        DK_API.logger.debug(str([k + '=' + v for k, v in os.environ.items() if k.startswith('DIGIKEY_')]))
        DK_API.logger.debug(str(DK_API.extra_ops))


class by_manf_pn(object):
    def __init__(self, manf_pn):
        self.manf_pn = manf_pn

    def search(self):
        search_request = ManufacturerProductDetailsRequest(manufacturer_product=self.manf_pn, record_count=10)
        self.api_limit = {}
        results, loaded = DK_API.cache.load_results('mpn', self.manf_pn)
        if not loaded:
            results = kicost_digikey_api_v3.manufacturer_product_details(body=search_request, api_limits=self.api_limit, **DK_API.extra_ops)
            if results is not None:
                DK_API.cache.save_results('mpn', self.manf_pn, results)
        # print('************************')
        # print(results)
        # print('************************')
        if results is None:
            return None
        if not isinstance(results, list):
            results = results.product_details
        if isinstance(results, list):
            if len(results) == 1:
                result = results[0]
            elif len(results) == 0:
                result = None
            else:
                tmp_results = [PartSortWrapper(r) for r in results]
                tmp_results.sort()
                result = tmp_results[0].data
                # print('* ' + self.manf_pn + ':')
                # for rs in tmp_results:
                #    r = rs.data
                #    print('- {} {} {} {} {}'.format(r.digi_key_part_number, r.minimum_order_quantity, r.manufacturer.value, rs.min_price, r.additional_value_fee))
            # print(result)
        return result


class by_digikey_pn(object):
    def __init__(self, dk_pn):
        self.dk_pn = dk_pn

    def search(self):
        self.api_limit = {}
        result, loaded = DK_API.cache.load_results('dpn', self.dk_pn)
        if not loaded:
            result = kicost_digikey_api_v3.product_details(self.dk_pn, api_limits=self.api_limit, includes=includes, **DK_API.extra_ops)
            DK_API.cache.save_results('dpn', self.dk_pn, result)
        return result


class by_keyword(object):
    def __init__(self, keyword):
        self.keyword = keyword

    def search(self):
        search_request = KeywordSearchRequest(keywords=self.keyword, record_count=10,
                                              exclude_market_place_products=DK_API.exclude_market_place_products)
        self.api_limit = {}
        result, loaded = DK_API.cache.load_results('key', self.keyword)
        if not loaded:
            result = kicost_digikey_api_v3.keyword_search(body=search_request, api_limits=self.api_limit, **DK_API.extra_ops) #, includes=includes)
            DK_API.cache.save_results('key', self.keyword, result)
        results = result.products
        # print(results)
        if isinstance(results, list):
            if len(results) == 1:
                result = results[0]
            elif len(results) == 0:
                result = None
            else:
                tmp_results = [PartSortWrapper(r) for r in results]
                tmp_results.sort()
                result = tmp_results[0].data
                # print('* ' + self.keyword + ':')
                # for rs in tmp_results:
                #    r = rs.data
                #    print('- {} {} {} {} {}'.format(r.digi_key_part_number, r.minimum_order_quantity, r.manufacturer.value, rs.min_price, r.additional_value_fee))
            if result is not None:
                # The keyword search returns incomplete data, do a query using the Digi-Key code
                o = by_digikey_pn(result.digi_key_part_number)
                result = o.search()
            # print(result)
        return result
