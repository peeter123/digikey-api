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

export DIGIKEY_CLIENT_ID="client_id"
export DIGIKEY_CLIENT_SECRET="client_secret"
export DIGIKEY_STORAGE_PATH="cache_dir"
```

# API V3
## Register
Register an app on the Digikey API portal: [Digi-Key API V3](https://developer.digikey.com/get_started). You will need 
the client ID and the client secret to use the API. You will also need a Digi-Key account to authenticate, using the 
Oauth2 process.

## Use [API V3]
Python will automatically spawn a browser to allow you to authenticate using the Oauth2 process. After obtaining a token
the library will cache the access token and use the refresh token to automatically refresh your credentials.

You can test your application using the sandbox API, the data returned from a Sandbox API may not be complete, but the 
structure of the Sandbox API response will be a representation of what to expect in Production.

For valid responses make sure you use the client ID and secret for a [Production App](https://developer.digikey.com/documentation/organization)

```python
import os
import digikey
from digikey.v3.productinformation import KeywordSearchRequest

os.environ['DIGIKEY_CLIENT_ID'] = 'client_id'
os.environ['DIGIKEY_CLIENT_SECRET'] = 'client_secret'
os.environ['DIGIKEY_CLIENT_SANDBOX'] = 'False'
os.environ['DIGIKEY_STORAGE_PATH'] = 'cache_dir'

# Query product number
dkpn = '296-6501-1-ND'
part = digikey.product_details(dkpn)

# Search for parts 
search_request = KeywordSearchRequest(keywords='CRCW080510K0FKEA', record_count=10)
result = digikey.keyword_search(body=search_request)
```

## Top-level API

#### Product Information
Currently all functions from the [PartSearch](https://developer.digikey.com/products/product-information/partsearch/) API have been implemented.
* `digikey.keyword_search()`
* `digikey.product_details()`
* `digikey.digi_reel_pricing()`
* `digikey.suggested_parts()`
* `digikey.manufacturer_product_details()`

#### Order Support
TODO

#### Barcode
TODO

# API V2 [Deprecated]
**NOTE: API V2 is not supported anymore by Digi-Key and you cannot register new applications**

See API V3 above to use the new API.

## Register
Register an app on the Digikey API portal: [Digi-Key API V2](https://api-portal.digikey.com/start). You will need the client
ID and the client secret to use the API. You will also need a Digi-Key account to authenticate, using the Oauth2 process.

## Use
Python will automatically spawn a browser to allow you to authenticate using the Oauth2 process. After obtaining a token
the library will cache the access token and use the refresh token to automatically refresh your credentials.

```python
import os
import digikey

os.environ['DIGIKEY_CLIENT_ID'] = 'client_id'
os.environ['DIGIKEY_CLIENT_SECRET'] = 'client_secret'
os.environ['DIGIKEY_STORAGE_PATH'] = 'cache_dir'

dkpn = '296-6501-1-ND'
part = digikey.part(dkpn)
print(part)
# <Part mpn=NE555DR>

print(part.manufacturer)
# 'Texas Instruments'
```

## Test
```sh
python -m pytest --cov=digikey --doctest-modules --ignore=setup.py
python -m mypy digikey --ignore-missing-imports
```

## Top-level API
* `digikey.search()`
* `digikey.part()`

## Data models
* `digikey.models.KeywordSearchResult`
* `digikey.models.Part`