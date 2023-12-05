from kicost_digikey_api_v3 import by_digikey_pn, by_keyword, by_manf_pn
from tools.test_config import configure

# Configuration file
cfg_file = None
# Default is ~/.config/kicost_digikey_api_v3/config.txt
# Must contain:
# DIGIKEY_CLIENT_ID = Digi-Key_registered_production_app_Client_ID
# DIGIKEY_CLIENT_SECRET = Digi-Key_registered_production_app_Client_Secret
# They can be defined in the OS environment. Environment vars have more priority than the config file.

# The "DIGIKEY_CLIENT_SANDBOX = True" can bne used to avoid consuming real queries
# The DIGIKEY_STORAGE_PATH option can be used to control where the tokens are stored

# Locale setup:
#         :param str x_digikey_locale_site: Two letter code for Digi-Key product website to search on. Different countries sites have different part restrictions, supported languages, and currencies. Acceptable values include: US, CA, JP, UK, DE, AT, BE, DK, FI, GR, IE, IT, LU, NL, NO, PT, ES, KR, HK, SG, CN, TW, AU, FR, IN, NZ, SE, MX, CH, IL, PL, SK, SI, LV, LT, EE, CZ, HU, BG, MY, ZA, RO, TH, PH.
#         :param str x_digikey_locale_language: Two letter code for language to search on. Langauge must be supported by the selected site. If searching on keyword, this language is used to find matches. Acceptable values include: en, ja, de, fr, ko, zhs, zht, it, es, he, nl, sv, pl, fi, da, no.
#         :param str x_digikey_locale_currency: Three letter code for Currency to return part pricing for. Currency must be supported by the selected site. Acceptable values include: USD, CAD, JPY, GBP, EUR, HKD, SGD, TWD, KRW, AUD, NZD, INR, DKK, NOK, SEK, ILS, CNY, PLN, CHF, CZK, HUF, RON, ZAR, MYR, THB, PHP.
#         :param str x_digikey_locale_ship_to_country: ISO code for country to ship to.
# It must be coherent, i.e.
# , x_digikey_locale_currency = 'EUR', x_digikey_locale_site = 'ES', x_digikey_locale_ship_to_country = 'ES'
# If you ask for EUR to the US site you'll get USD, they won't charge you in EUR

configure(cfg_file)

# Query product number
dkpn = '296-6501-6-ND'
o = by_digikey_pn(dkpn)
part = o.search()
api_limit = o.api_limit

print(part)
print('part_num: ' + part.digi_key_part_number)
print('url: ' + part.product_url)
print('qty_avail: ' + str(part.quantity_available))
print('moq/qty_increment: ' +  str(part.minimum_order_quantity))
print('datasheet: ' + part.primary_datasheet)
# Active, Obsolete, Discontinued at Digi-Key, Last Time Buy, Not For New  Designs, Preliminary.
print('lifecycle: ' + part.product_status.lower())
print('currency: ' + part.search_locale_used.currency)
price_tiers = {p.break_quantity: p.unit_price for p in part.standard_pricing}
print('price_tiers: ' + str(price_tiers))
specs = {sp.parameter: (sp.parameter, sp.value) for sp in part.parameters}
specs['RoHS'] = ('RoHS', part.ro_hs_status)
print('specs: ' + str(specs))
print('-----')
print('price_offset: ' + str(part.additional_value_fee))
print(api_limit)
exit(0)


# Batch search
# This isn't a free API
# products = ['296-6501-6-ND', 'CRCW080510K0FKEA']
# request = BatchProductDetailsRequest(products=products)
# api_limit = {}
# result = kicost_digikey_api_v3.batch_product_details(body=request, api_limits=api_limit)
# print(result)
# print(api_limit)
# exit(0)

# Search for manufacturer parts
# Search for a manufacturer part
# Returns one record for each available match and for each digikey code (i.e. one for the reel, another for the cut tape, etc.)
# Only exact matches are returned
#manf_pn = 'CRCW080510K0FKEA'
manf_pn = 'C0805C104K5RACTU'
o = by_manf_pn(manf_pn)
result = o.search()
api_limit = o.api_limit

print(len(result))
for part in result:
    # print(part)
    print('part_num: ' + part.digi_key_part_number)
    print('url: ' + part.product_url)
    print('qty_avail: ' + str(part.quantity_available))
    print('moq/qty_increment: ' +  str(part.minimum_order_quantity))
    print('datasheet: ' + part.primary_datasheet)
    # Active, Obsolete, Discontinued at Digi-Key, Last Time Buy, Not For New  Designs, Preliminary.
    print('lifecycle: ' + part.product_status.lower())
    print('currency: ' + part.search_locale_used.currency)
    price_tiers = {p.break_quantity: p.unit_price for p in part.standard_pricing}
    print('price_tiers: ' + str(price_tiers))
    specs = {sp.parameter: (sp.parameter, sp.value) for sp in part.parameters}
    specs['RoHS'] = ('RoHS', part.ro_hs_status)
    print('specs: ' + str(specs))
    print('* price_offset: ' + str(part.additional_value_fee))
    print('-----')
print(api_limit)
exit(0)

# Search for parts by keyword
o = by_keyword('CRCW080510K0FKEA')
result = o.search()
print(result)
print(o.api_limit)
exit(0)

