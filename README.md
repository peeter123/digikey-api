Python Client for Digikey API
=================================
Search for parts in the Digi-Key catalog by keyword using KeywordSearch. Then make a PartDetails call to retrieve all 
real time information about the part including pricing. PartDetails works best with Digi-Key part numbers as some 
manufacturers overlap other manufacturer part numbers.

[![Pypi](https://img.shields.io/pypi/v/digikey-api.svg?color=brightgreen)](https://pypi.org/project/digikey-api/) 
[![Donate](https://img.shields.io/badge/Donate-PayPal-gold.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=53HWHHVCJ3D4J&currency_code=EUR&source=url)

# What does it do
`digikey-api` is an [Digkey Part Search API](https://api-portal.digikey.com/node/8517) client for Python 3.6+. API response data is returned as Python objects that attempt to make it easy to get the data you want. Not all endpoints have been implemented.

# Quickstart

## Install
```sh
pip install digikey-api
```

# API V3
## Register
Register an app on the Digikey API portal: [Digi-Key API V3](https://developer.digikey.com/get_started). You will need 
the client ID and the client secret to use the API. You will also need a Digi-Key account to authenticate, using the 
Oauth2 process.

When registering an app the OAuth Callback needs to be set to `https://localhost:8139/digikey_callback`.

## Use [API V3]
Python will automatically spawn a browser to allow you to authenticate using the Oauth2 process. After obtaining a token
the library will cache the access token and use the refresh token to automatically refresh your credentials.

You can test your application using the sandbox API, the data returned from a Sandbox API may not be complete, but the 
structure of the Sandbox API response will be a representation of what to expect in Production.

For valid responses make sure you use the client ID and secret for a [Production App](https://developer.digikey.com/documentation/organization)

```python
import digikey
from digikey.v3.productinformation import KeywordSearchRequest

dk_config = digikey.DigikeyJsonConfig(file_name='dk_conf.json')
dk_api = digikey.DigikeyAPI(dk_config, is_sandbox=False)
dk_api.set_client_info(client_id='ENTER_CLIENT_ID', client_secret='ENTER_CLIENT_SECRET')

# Query product number
dkpn = '296-6501-1-ND'
part = dk_api.product_details(dkpn)

# Search for parts 
search_request = KeywordSearchRequest(keywords='CRCW080510K0FKEA', record_count=10)
result = dk_api.keyword_search(body=search_request)
```

## API Configuration Storage
`DigikeyAPI` requires a configuration class that will handle getting, storing, and saving key-value pairs. Currently
only `DigikeyJsonConfig` is implemented for storing settings in a JSON file, but a custom configuration can be created.
See [docs/DigikeyBaseConfig.md](docs/DigikeyBaseConfig.md) for more details on that.

## Top-level APIs

#### Configuration Related Functions
* `set_client_info()`
    * Arguments are `client_id` and `client_secret`
* `DigikeyAPI.needs_client_id()`
    * Returns `True` if a client ID is needed/missing
* `DigikeyAPI.needs_client_secret()`
    * Returns `True` if a client secret is needed/missing

#### Product Information
All functions from the [PartSearch](https://developer.digikey.com/products/product-information/partsearch/) API have been implemented.
* `DigikeyAPI.keyword_search()`
* `DigikeyAPI.product_details()`
* `DigikeyAPI.digi_reel_pricing()`
* `DigikeyAPI.suggested_parts()`
* `DigikeyAPI.manufacturer_product_details()`

#### Batch Product Details
The one function from the [BatchProductDetailsAPI](https://developer.digikey.com/products/batch-productdetails/batchproductdetailsapi) API has been implemented.
* `DigikeyAPI.batch_product_details()`

#### Order Support
All functions from the [OrderDetails](https://developer.digikey.com/products/order-support/orderdetails/) API have been implemented.
* `DigikeyAPI.salesorder_history()`
* `DigikeyAPI.status_salesorder_id()`

#### Barcode
TODO

## API Limits
The API has a limited amount of requests you can make per time interval [Digikey Rate Limits](https://developer.digikey.com/documentation/shared-concepts#rate-limits). 

It is possible to retrieve the number of max requests and current requests by passing an optional api_limits kwarg to an API function:
```python
api_limit = {}
search_request = KeywordSearchRequest(keywords='CRCW080510K0FKEA', record_count=10)
result = dk_api.keyword_search(body=search_request, api_limits=api_limit)
```
 
The dict will be filled with the information returned from the API:
```python
{ 
    'api_requests_limit': 1000, 
    'api_requests_remaining': 139
}
```
Sometimes the API does not return any rate limit data, the values will then be set to None.

