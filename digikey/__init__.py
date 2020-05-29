import logging
from digikey.v2.api import (search, part)

logger = logging.getLogger(__name__)


def setup_logger(logger_ref):
    logger_ref.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s: %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger_ref.addHandler(handler)


setup_logger(logger)

name = 'digikey'
