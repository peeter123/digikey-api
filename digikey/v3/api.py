import digikey.v3.product_information_client as pic

def searchv3(query: str,
           start: int = 0,
           limit: int = 10,
           ):
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
    response = client.keyword_search(
        query,
        start,
        limit,
    )
    return response

def partv3(partnr: str,
         include_associated: bool = False,
         include_for_use_with: bool = False,
         ):
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
    response = client.product_details(
        partnr
    )
    return response
