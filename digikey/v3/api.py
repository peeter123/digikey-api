import digikey.v3.product_information_client as pic
from digikey.v3.productinformation import KeywordSearchRequest, KeywordSearchResponse, ProductDetails


def searchv3(search_request: KeywordSearchRequest) -> KeywordSearchResponse:
    """
    Search Digikey for a general keyword (and optional filters).
    Args:
        query (str): Free-form keyword query
        start: Ordinal position of first result
        limit: Maximum number of results to return
    Returns:
        list of `models.KeywordSearchResult` objects.
    """
    client = pic.ProductInformation()
    response = client.keyword_search(search_request)
    return response


def partv3(partnr: str) -> ProductDetails:
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
    client = pic.ProductInformation()
    response = client.product_details(partnr)
    return response
