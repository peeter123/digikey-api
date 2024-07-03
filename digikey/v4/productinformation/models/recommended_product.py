# coding: utf-8

"""
    ProductSearch Api

    ProductSearch Api  # noqa: E501

    OpenAPI spec version: v4
    Contact: dl_Agile_Team_B2B_API@digikey.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class RecommendedProduct(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'digi_key_product_number': 'str',
        'manufacturer_product_number': 'str',
        'manufacturer_name': 'str',
        'primary_photo': 'str',
        'product_description': 'str',
        'quantity_available': 'int',
        'unit_price': 'float',
        'product_url': 'str'
    }

    attribute_map = {
        'digi_key_product_number': 'DigiKeyProductNumber',
        'manufacturer_product_number': 'ManufacturerProductNumber',
        'manufacturer_name': 'ManufacturerName',
        'primary_photo': 'PrimaryPhoto',
        'product_description': 'ProductDescription',
        'quantity_available': 'QuantityAvailable',
        'unit_price': 'UnitPrice',
        'product_url': 'ProductUrl'
    }

    def __init__(self, digi_key_product_number=None, manufacturer_product_number=None, manufacturer_name=None, primary_photo=None, product_description=None, quantity_available=None, unit_price=None, product_url=None):  # noqa: E501
        """RecommendedProduct - a model defined in Swagger"""  # noqa: E501
        self._digi_key_product_number = None
        self._manufacturer_product_number = None
        self._manufacturer_name = None
        self._primary_photo = None
        self._product_description = None
        self._quantity_available = None
        self._unit_price = None
        self._product_url = None
        self.discriminator = None
        if digi_key_product_number is not None:
            self.digi_key_product_number = digi_key_product_number
        if manufacturer_product_number is not None:
            self.manufacturer_product_number = manufacturer_product_number
        if manufacturer_name is not None:
            self.manufacturer_name = manufacturer_name
        if primary_photo is not None:
            self.primary_photo = primary_photo
        if product_description is not None:
            self.product_description = product_description
        if quantity_available is not None:
            self.quantity_available = quantity_available
        if unit_price is not None:
            self.unit_price = unit_price
        if product_url is not None:
            self.product_url = product_url

    @property
    def digi_key_product_number(self):
        """Gets the digi_key_product_number of this RecommendedProduct.  # noqa: E501

        The Digi-Key part number.  # noqa: E501

        :return: The digi_key_product_number of this RecommendedProduct.  # noqa: E501
        :rtype: str
        """
        return self._digi_key_product_number

    @digi_key_product_number.setter
    def digi_key_product_number(self, digi_key_product_number):
        """Sets the digi_key_product_number of this RecommendedProduct.

        The Digi-Key part number.  # noqa: E501

        :param digi_key_product_number: The digi_key_product_number of this RecommendedProduct.  # noqa: E501
        :type: str
        """

        self._digi_key_product_number = digi_key_product_number

    @property
    def manufacturer_product_number(self):
        """Gets the manufacturer_product_number of this RecommendedProduct.  # noqa: E501

        The manufacturer part number.  # noqa: E501

        :return: The manufacturer_product_number of this RecommendedProduct.  # noqa: E501
        :rtype: str
        """
        return self._manufacturer_product_number

    @manufacturer_product_number.setter
    def manufacturer_product_number(self, manufacturer_product_number):
        """Sets the manufacturer_product_number of this RecommendedProduct.

        The manufacturer part number.  # noqa: E501

        :param manufacturer_product_number: The manufacturer_product_number of this RecommendedProduct.  # noqa: E501
        :type: str
        """

        self._manufacturer_product_number = manufacturer_product_number

    @property
    def manufacturer_name(self):
        """Gets the manufacturer_name of this RecommendedProduct.  # noqa: E501

        The name of the manufacturer.  # noqa: E501

        :return: The manufacturer_name of this RecommendedProduct.  # noqa: E501
        :rtype: str
        """
        return self._manufacturer_name

    @manufacturer_name.setter
    def manufacturer_name(self, manufacturer_name):
        """Sets the manufacturer_name of this RecommendedProduct.

        The name of the manufacturer.  # noqa: E501

        :param manufacturer_name: The manufacturer_name of this RecommendedProduct.  # noqa: E501
        :type: str
        """

        self._manufacturer_name = manufacturer_name

    @property
    def primary_photo(self):
        """Gets the primary_photo of this RecommendedProduct.  # noqa: E501

        The URL to the product’s image.  # noqa: E501

        :return: The primary_photo of this RecommendedProduct.  # noqa: E501
        :rtype: str
        """
        return self._primary_photo

    @primary_photo.setter
    def primary_photo(self, primary_photo):
        """Sets the primary_photo of this RecommendedProduct.

        The URL to the product’s image.  # noqa: E501

        :param primary_photo: The primary_photo of this RecommendedProduct.  # noqa: E501
        :type: str
        """

        self._primary_photo = primary_photo

    @property
    def product_description(self):
        """Gets the product_description of this RecommendedProduct.  # noqa: E501

        Catalog description of the product.  # noqa: E501

        :return: The product_description of this RecommendedProduct.  # noqa: E501
        :rtype: str
        """
        return self._product_description

    @product_description.setter
    def product_description(self, product_description):
        """Sets the product_description of this RecommendedProduct.

        Catalog description of the product.  # noqa: E501

        :param product_description: The product_description of this RecommendedProduct.  # noqa: E501
        :type: str
        """

        self._product_description = product_description

    @property
    def quantity_available(self):
        """Gets the quantity_available of this RecommendedProduct.  # noqa: E501

        Quantity of the product available for immediate sale.  # noqa: E501

        :return: The quantity_available of this RecommendedProduct.  # noqa: E501
        :rtype: int
        """
        return self._quantity_available

    @quantity_available.setter
    def quantity_available(self, quantity_available):
        """Sets the quantity_available of this RecommendedProduct.

        Quantity of the product available for immediate sale.  # noqa: E501

        :param quantity_available: The quantity_available of this RecommendedProduct.  # noqa: E501
        :type: int
        """

        self._quantity_available = quantity_available

    @property
    def unit_price(self):
        """Gets the unit_price of this RecommendedProduct.  # noqa: E501

        The catalog price for a single unit of this product.  # noqa: E501

        :return: The unit_price of this RecommendedProduct.  # noqa: E501
        :rtype: float
        """
        return self._unit_price

    @unit_price.setter
    def unit_price(self, unit_price):
        """Sets the unit_price of this RecommendedProduct.

        The catalog price for a single unit of this product.  # noqa: E501

        :param unit_price: The unit_price of this RecommendedProduct.  # noqa: E501
        :type: float
        """

        self._unit_price = unit_price

    @property
    def product_url(self):
        """Gets the product_url of this RecommendedProduct.  # noqa: E501

        URL of the Digi-Key catalog page to purchase the product. This is based on your provided header Locale values.  # noqa: E501

        :return: The product_url of this RecommendedProduct.  # noqa: E501
        :rtype: str
        """
        return self._product_url

    @product_url.setter
    def product_url(self, product_url):
        """Sets the product_url of this RecommendedProduct.

        URL of the Digi-Key catalog page to purchase the product. This is based on your provided header Locale values.  # noqa: E501

        :param product_url: The product_url of this RecommendedProduct.  # noqa: E501
        :type: str
        """

        self._product_url = product_url

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(RecommendedProduct, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RecommendedProduct):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
