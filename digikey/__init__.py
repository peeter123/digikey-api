import logging
from digikey.v2.api import (search, part)
from digikey.v3.api import (keyword_search, product_details, digi_reel_pricing, suggested_parts,
                            manufacturer_product_details)

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
