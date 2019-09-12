import functools
import logging

import retrying
from requests.exceptions import RequestException

from digikey.exceptions import DigikeyError

logger = logging.getLogger(__name__)


def wrap_exception_in(exc_type, catch=Exception):
    """
    Wraps raised exception in another exception type, and only includes
    the original exception type name in the new exception message.
    Args:
        exc_type: Exception type
        catch: optional, Exception type to catch
    """

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except catch as exc:
                logger.error('Wrapped error: %s', str(exc))
                message = type(exc).__name__
                # Add HTTP status code, if one is attached to 'exc'.
                try:
                    message += f' {exc.response.status_code}'
                except AttributeError:
                    pass
                raise exc_type(message) from exc

        return inner

    return wrapper


# Retry when RequestException is raised.
# wait 2^x * 100 milliseconds between each retry,
# wait up to 10 seconds between each retry,
# and stop retrying after 20 total seconds.
exponential_backoff = retrying.retry(
    retry_on_exception=lambda exc: isinstance(exc, RequestException),
    wait_exponential_multiplier=100,
    wait_exponential_max=10000,
    stop_max_delay=20000)


def retry(func):
    """
    Applies exponential backoff and exception wrapper decorators to expose
    a single decorator, to wrap functions that make HTTP requests.
    """

    @functools.wraps(func)
    @wrap_exception_in(DigikeyError)
    @exponential_backoff
    def inner(*args, **kwargs):
        return func(*args, **kwargs)

    return inner