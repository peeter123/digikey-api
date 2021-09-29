# -*- coding: utf-8 -*-
# GPL license
#
# Copyright (C) 2021 by Salvador E. Tropea / Instituto Nacional de Tecnologia Industrial
#
import os
import re
import logging
import pickle

import kicost_digikey_api_v3
from kicost_digikey_api_v3.v3.productinformation import ManufacturerProductDetailsRequest, KeywordSearchRequest
from .exceptions import DigikeyError

logger = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/22.0"
includes = ["DigiKeyPartNumber","ProductUrl","QuantityAvailable","MinimumOrderQuantity","PrimaryDatasheet","ProductStatus",
            "SearchLocaleUsed","StandardPricing","Parameters","RoHsStatus","AdditionalValueFee"]
includes = ','.join(includes)
# Store the results to reproduce them during debug
do_save_results = False
# Read the results from disk for debugging
do_fake_results = False


def get_name(prefix, name):
    return os.path.join(os.environ['DIGIKEY_STORAGE_PATH'], prefix + '_' + name.replace('/', '_') + ".dat")


def save_results(prefix, name, results):
    if do_save_results:
        file = get_name(prefix, name)
        if do_fake_results and os.path.isfile(file):
            # Don't refresh the data we loaded
            return
        with open(file, "wb") as fh:
            pickle.dump(results, fh)


def fake_results(prefix, name):
    if do_fake_results:
        file = get_name(prefix, name)
        if os.path.isfile(file):
            with open(file, "rb") as fh:
                return pickle.loads(fh.read())


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


class by_manf_pn(object):
    def __init__(self, manf_pn):
        self.manf_pn = manf_pn

    def search(self):
        search_request = ManufacturerProductDetailsRequest(manufacturer_product=self.manf_pn, record_count=10)
        self.api_limit = {}
        results = fake_results('mpn', self.manf_pn)
        if results is None:
            results = kicost_digikey_api_v3.manufacturer_product_details(body=search_request, api_limits=self.api_limit)
        save_results('mpn', self.manf_pn, results)
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
                # print('* ' + self.manf_pn + ':')
                # for rs in tmp_results:
                #    r = rs.data
                #    print('- {} {} {} {} {}'.format(r.digi_key_part_number, r.minimum_order_quantity, r.manufacturer.value, rs.min_price, r.additional_value_fee))
            # print(result)
        else:
            result = results.product_details
        return result


class by_digikey_pn(object):
    def __init__(self, dk_pn):
        self.dk_pn = dk_pn

    def search(self):
        self.api_limit = {}
        result = fake_results('dpn', self.dk_pn)
        if result is None:
            result = kicost_digikey_api_v3.product_details(self.dk_pn, api_limits=self.api_limit, includes=includes)
        save_results('dpn', self.dk_pn, result)
        return result


class by_keyword(object):
    def __init__(self, keyword):
        self.keyword = keyword

    def search(self):
        search_request = KeywordSearchRequest(keywords=self.keyword, record_count=10)
        self.api_limit = {}
        result = fake_results('key', self.keyword)
        if result is None:
            result = kicost_digikey_api_v3.keyword_search(body=search_request, api_limits=self.api_limit) #, includes=includes)
        save_results('key', self.keyword, result)
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


def environ_add(var, value):
    """ Adds variable var to the environment, but only if not already defined """
    if os.getenv(var) is None:
        os.environ[var] = value


def configure(file=None, a_logger=None):
    """ Load the configuration file and check we have the needed stuff """
    if a_logger:
        global logger
        logger = a_logger
        kicost_digikey_api_v3.v3.api.set_logger(a_logger)
    if not file:
        data_path = os.getenv('DIGIKEY_STORAGE_PATH')
        if data_path:
            fn = os.path.join(data_path, 'config.txt')
            if os.path.isfile(fn):
                file = fn
        # Default config file
        if not file:
            file = os.path.join(os.environ['HOME'], '.config', 'kicost_digikey_api_v3', 'config.txt')
    if os.path.isfile(file):
        # Load options from the configuration file
        reg = re.compile(r'(\w+)\s*=\s*(.*)')
        with open(file, 'rt') as fh:
            for line in fh:
                if line[0] != '#':
                    res = reg.match(line)
                    if res:
                        (var, val) = res.groups()
                        environ_add(var, val)
    # Ensure we have a place to store the token
    environ_add('DIGIKEY_STORAGE_PATH', os.path.dirname(file))
    dir = os.environ['DIGIKEY_STORAGE_PATH']
    if not os.path.isdir(dir):
        raise DigikeyError("No directory to store tokens, please create `{}`".format(dir))
    # Ensure we have the credentials
    id = os.getenv('DIGIKEY_CLIENT_ID')
    secret = os.getenv('DIGIKEY_CLIENT_SECRET')
    if not id or not secret:
        raise DigikeyError("No Digi-Key credentials defined, store them in `{}`".format(file))
    # Default to no sandbox
    environ_add('DIGIKEY_CLIENT_SANDBOX', 'False')
    # Debug configuration
    if os.getenv('DIGIKEY_SAVE_RESULTS'):
        global do_save_results
        do_save_results = True
    if os.getenv('DIGIKEY_FAKE_RESULTS'):
        global do_fake_results
        do_fake_results = True
    logger.debug('Digi-Key API plug-in options:')
    logger.debug(str([k + '=' + v for k, v in os.environ.items() if k.startswith('DIGIKEY_')]))
