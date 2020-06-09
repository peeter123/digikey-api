import logging
from digikey.v2.api import (search, part)
from digikey.v3.api import (keyword_search, part_number)

logger = logging.getLogger(__name__)


def setup_logger(logger_ref):
    logger_ref.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)6s: %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger_ref.addHandler(handler)


setup_logger(logger)

name = 'digikey'
