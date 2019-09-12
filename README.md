Python Client for Digikey PartSearch API v2
=================================
# Quickstart

## Install

```sh
pip install digikey-api

export DIGIKEY_CLIENT_ID="client_id"
export DIGIKEY_CLIENT_SECRET'="client_secret"
export DIGIKEY_STORAGE_PATH'="cache_dir"
```

## Use

```python
import digikey

os.environ['DIGIKEY_CLIENT_ID'] = client_id
os.environ['DIGIKEY_CLIENT_SECRET'] = client_secret
os.environ['DIGIKEY_STORAGE_PATH'] = cache_dir

dkpn = '296-6501-1-ND'
part = digikey.part(dkpn)
print(part)
# <Part mpn=NE555DR>

print(part.manufacturer)
# 'Texas Instruments'
```

## Test

```sh
python -m pytest --cov=octopart --doctest-modules --ignore=setup.py
python -m mypy digikey --ignore-missing-imports
```

# What does it do

`digkey-api` is an [Digkey Part Search API](https://api-portal.digikey.com/node/8517) client for Python 3.6+. API response data is returned as Python objects that attempt to make it easy to get the data you want. Not all endpoints have been implemented.

## Top-level API
* `digikey.search()`
* `digikey.part()`

## Data models
* `digikey.models.KeywordSearchResult`
* `digikey.models.Part`
