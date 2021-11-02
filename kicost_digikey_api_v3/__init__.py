import logging
from kicost_digikey_api_v3.v3.api import (keyword_search, product_details, digi_reel_pricing, suggested_parts,
                                          manufacturer_product_details)
from .utils import by_manf_pn, by_digikey_pn, by_keyword, DK_API
from .exceptions import DigikeyError

logger = logging.getLogger(__name__)


def setup_logger(logger_ref):
    logger_ref.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)20.20s - %(levelname)8s: %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger_ref.addHandler(handler)


setup_logger(logger)

name = 'digikey'
