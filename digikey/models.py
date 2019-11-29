"""
Types that wrap responses from the Octopart API
and make various attributes easier to access.
"""

import inflection

from schematics.exceptions import ConversionError, DataError, ValidationError
from schematics.models import Model
from schematics.types import BooleanType, IntType, StringType
from schematics.types.compound import ListType, ModelType


class BaseModel(Model):
    @classmethod
    def errors(cls, dict_):
        """
        Wraps `schematics` validate method to return an error list instead of
        having to catch an exception in the caller.
        Returns:
            list of validation errors, or None.
        """
        try:
            cls(dict_).validate()
            return None
        except (DataError, ValidationError) as err:
            return err.messages

    @classmethod
    def errors_list(cls, list_):
        """
        Return any validation errors in list of dicts.
        Args:
            list_ (list): dicts to be validated.
        Returns:
            list of errors, if any, otherwise None.
        """
        try:
            errors = [cls(dict_).errors for dict_ in list_]
            if any(errors):
                return [_f for _f in errors if _f]
            return None
        except (ConversionError, DataError) as err:
            return err.messages

    @classmethod
    def is_valid(cls, dict_):
        return not cls.errors(dict_)

    @classmethod
    def is_valid_list(cls, list_):
        try:
            return all([cls(dict_).is_valid for dict_ in list_])
        except (ConversionError, DataError):
            return False

    @classmethod
    def camelize(cls, dict_):
        return {inflection.camelize(k): v for k, v in dict_.items()}


class Filters(BaseModel):
    """Query format sent to the search endpoint
    https://api-portal.digikey.com/node/8517
    """


class Sort(BaseModel):
    """Query format sent to the search endpoint
    https://api-portal.digikey.com/node/8517
    """


class KeywordSearchRequest(BaseModel):
    """Query format sent to the search endpoint
    https://api-portal.digikey.com/node/8517
    """
    # Keywords to search on
    keywords = StringType(required=True)
    # Filters the search results by the included SearchOptions
    search_options = ListType(StringType)
    # Maximum number of items to return
    record_count = IntType(default=10, min_value=1, max_value=50, required=True)
    # Ordinal position of first returned item
    record_start_pos = IntType(default=0)
    # Set Filters to narrow down search response
    filters = ModelType(Filters)
    # Sort Parameters
    sort = ModelType(Sort)
    # The RequestedQuantity is used with the SortByUnitPrice Sort Option to sort by unit price at the RequestedQuantity
    requested_quantity = IntType(default=1)


class PartDetailPostRequest(BaseModel):
    """Query format sent to the partdetails endpoint
    https://api-portal.digikey.com/node/8517
    """
    # Part number. Works best with Digi-Key part numbers.
    part = StringType(required=True)
    # The option to include all Associated products
    include_all_associated_products = BooleanType()
    # The option to include all For Use With products
    include_all_for_use_with_products = BooleanType()


class KeywordSearchResult:
    def __init__(self, result):
        self._result = result

    @property
    def parts(self):
        return [
            Part(result)
            for result in self._result.get('Parts', [])
        ]

    def __repr__(self):
        return '<KeywordSearchResult: hits=%s>' % self._result['Results']

    def pretty_print(self):
        print(self)
        for part in self.parts:
            print('\t%s' % part)


''' 
Helper classes for responses
'''


class PriceBreak:
    def __init__(self, pricebreak: dict):
        self._pricebreak = pricebreak

    @property
    def breakquantity(self) -> int:
        return self._pricebreak.get('BreakQuantity', 0)

    @property
    def unitprice(self) -> float:
        return self._pricebreak.get('UnitPrice', 0.0)

    @property
    def totalprice(self) -> float:
        return self._pricebreak.get('TotalPrice', 0.0)


class IdTextPair:
    def __init__(self, idtextpair: dict):
        self._idtextpair = idtextpair

    @property
    def id(self) -> str:
        return self._idtextpair.get('Id', '')

    @property
    def text(self) -> str:
        return self._idtextpair.get('Text', '')


class PidVid:
    def __init__(self, pidvid: dict):
        self._pidvid = pidvid

    @property
    def parameter_id(self) -> int:
        return self._pidvid.get('ParameterId', 0)

    @property
    def value_id(self) -> int:
        return self._pidvid.get('ValueId', 0)

    @property
    def parameter(self) -> str:
        return self._pidvid.get('Parameter', '')

    @property
    def value(self) -> str:
        return self._pidvid.get('Value', '')

    def __repr__(self):
        return '<PidVid param={} val={}>'.format(self.parameter, self.value)


class Family:
    def __init__(self, family: dict):
        self._family = family

    @property
    def id(self) -> str:
        return self._family.get('Id', '')

    @property
    def name(self) -> str:
        return self._family.get('Name', '')

    @property
    def part_count(self) -> int:
        return self._family.get('PartCount', 0)


class Part:
    def __init__(self, part: dict):
        self._part = part

    @property
    def standard_pricing(self) -> list:
        return [
            PriceBreak(part)
            for part in self._part.get('StandardPricing', [])
        ]

    @property
    def category(self) -> IdTextPair:
        return IdTextPair(self._part.get('Category', {}))

    @property
    def family(self) -> IdTextPair:
        return IdTextPair(self._part.get('Family', {}))

    @property
    def manufacturer(self) -> str:
        return IdTextPair(self._part.get('ManufacturerName', {})).text

    @property
    def mpn(self) -> str:
        return self._part.get('ManufacturerPartNumber', None)

    @property
    def part_status(self) -> str:
        return self._part.get('PartStatus', None)

    @property
    def digikey_pn(self) -> str:
        return self._part.get('DigiKeyPartNumber', None)

    @property
    def digikey_url(self) -> str:
        return 'https://www.digikey.com' + self._part.get('PartUrl', '')

    @property
    def in_stock(self) -> int:
        return self._part.get('QuantityOnHand', None)

    @property
    def moq(self) -> int:
        return self._part.get('MinimumOrderQuantity', None)

    @property
    def parameters(self) -> dict:
        _params = [PidVid(param) for param in self._part.get('Parameters', [])]
        return {p.parameter: p.value for p in _params}

    @property
    def description_product(self) -> str:
        return self._part.get('ProductDescription', None)

    @property
    def description_detailed(self) -> str:
        return self._part.get('DetailedDescription', None)

    @property
    def datasheet(self) -> str:
        return self._part.get('PrimaryDatasheet', None)

    def __repr__(self):
        return '<Part mpn=%s>' % self.mpn
