from __future__ import annotations

import pytest

from digikey import DigikeyApiError, DigikeyClient
from digikey.v4 import productsearch

pytestmark = pytest.mark.vcr

PART = "296-6501-1-ND"  # TI LM358 cut tape: has pricing, media, substitutions and DigiReel


def test_keyword_search(prod: DigikeyClient) -> None:
    result = prod.keyword_search(productsearch.KeywordRequest(keywords="LM358", limit=5))
    assert result.products_count and result.products_count > 0
    assert 0 < len(result.products or []) <= 5
    assert all(p.manufacturer_product_number for p in result.products or [])


def test_product_details(prod: DigikeyClient) -> None:
    result = prod.product_details(PART)
    product = result.product
    assert product is not None
    assert product.manufacturer is not None and product.manufacturer.name
    assert any(v.digi_key_product_number == PART for v in product.product_variations or [])


def test_product_details_not_found(prod: DigikeyClient) -> None:
    with pytest.raises(DigikeyApiError) as error:
        prod.product_details("THIS-PART-DOES-NOT-EXIST-ND")
    assert error.value.status == 404


def test_product_pricing(prod: DigikeyClient) -> None:
    assert prod.product_pricing(PART, limit=1).product_pricings is not None


def test_pricing_options_by_quantity(prod: DigikeyClient) -> None:
    assert prod.pricing_options_by_quantity(PART, 100) is not None


def test_digi_reel_pricing(prod: DigikeyClient) -> None:
    assert prod.digi_reel_pricing(PART, 500) is not None


def test_substitutions(prod: DigikeyClient) -> None:
    assert prod.substitutions(PART) is not None


def test_recommended_products(prod: DigikeyClient) -> None:
    assert prod.recommended_products(PART, limit=3) is not None


def test_associations(prod: DigikeyClient) -> None:
    assert prod.associations(PART) is not None


def test_alternate_packaging(prod: DigikeyClient) -> None:
    assert prod.alternate_packaging(PART) is not None


def test_media(prod: DigikeyClient) -> None:
    assert prod.media(PART).media_links


def test_manufacturers(prod: DigikeyClient) -> None:
    assert len(prod.manufacturers().manufacturers or []) > 100


def test_categories(prod: DigikeyClient) -> None:
    categories = prod.categories().categories or []
    assert categories
    assert prod.categories_by_id(categories[0].category_id).category is not None
