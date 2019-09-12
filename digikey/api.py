"""
Top-level API, provides access to the Digikey API
without directly instantiating a client object.
Also wraps the response JSON in types that provide easier access
to various fields.
"""
from digikey.client import DigikeyClient
from digikey import models


def search(query: str,
           start: int = 0,
           limit: int = 10,
           ) -> models.KeywordSearchResult:
    """
    Search Digikey for a general keyword (and optional filters).
    Args:
        query (str): Free-form keyword query
        start: Ordinal position of first result
        limit: Maximum number of results to return
    Returns:
        list of `models.KeywordSearchResult` objects.
    """

    client = DigikeyClient()
    response = client.search(
        query,
        start=start,
        limit=limit,
    )
    return models.KeywordSearchResult(response)
