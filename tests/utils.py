""" Utility functions for testing, _not_ tests for utilities"""
from contextlib import contextmanager
import json
import re

import responses


@contextmanager
def digikey_api_mock_response(data=None):
    """Boilerplate for mocking all Dgikey API URLs with an empty response"""
    if data is None:
        data = {"results": []}

    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            re.compile(r'https://api.digikey\.com/services/.*'),
            body=json.dumps(data),
            status=200,
            content_type='application/json'
        )

        yield rsps

@contextmanager
def digikey_sso_mock_response(data=None):
    """Boilerplate for mocking all Dgikey SSO URLs with an empty response"""
    if data is None:
        data = {"results": []}

    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            re.compile(r'https://sso.digikey\.com/as/.*'),
            body=json.dumps(data),
            status=200,
            content_type='application/json'
        )

        yield rsps



def request_url_from_request_mock(reqmock):
    """Given responses.RequestsMock, get URL of first recorded request
    Utility method for asserting that the correct URL was generated. Fails
    if more than one request was made against the RequestMock.
    """
    assert len(reqmock.calls) == 1
    request, _ = reqmock.calls[0]
    return request.url
