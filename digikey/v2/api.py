"""
Top-level API, provides access to the Digikey API
without directly instantiating a client object.
Also wraps the response JSON in types that provide easier access
to various fields.
"""
from digikey.v2 import models
from digikey.v2.client import DigikeyClient


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


def part(partnr: str,
         include_associated: bool = False,
         include_for_use_with: bool = False,
         ) -> models.Part:
    """
    Query part by unique ID
    Args:
        partnr (str): Part number. Works best with Digi-Key part numbers.
        include_associated (bool): The option to include all Associated products
        include_for_use_with (bool): The option to include all For Use With product
    Kwargs:
    Returns:
        dict. See `models.Part` for exact fields.
    """
    client = DigikeyClient()
    response = client.part(
        partnr,
        include_associated=include_associated,
        include_for_use_with=include_for_use_with,
    )
    return models.Part(response['PartDetails'])
