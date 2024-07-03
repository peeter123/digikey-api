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

class ProductPricingResponse(object):
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
        'product_pricings': 'list[ProductPricing]',
        'products_count': 'int',
        'settings_used': 'SettingsUsed'
    }

    attribute_map = {
        'product_pricings': 'ProductPricings',
        'products_count': 'ProductsCount',
        'settings_used': 'SettingsUsed'
    }

    def __init__(self, product_pricings=None, products_count=None, settings_used=None):  # noqa: E501
        """ProductPricingResponse - a model defined in Swagger"""  # noqa: E501
        self._product_pricings = None
        self._products_count = None
        self._settings_used = None
        self.discriminator = None
        if product_pricings is not None:
            self.product_pricings = product_pricings
        if products_count is not None:
            self.products_count = products_count
        if settings_used is not None:
            self.settings_used = settings_used

    @property
    def product_pricings(self):
        """Gets the product_pricings of this ProductPricingResponse.  # noqa: E501

        List of Products  # noqa: E501

        :return: The product_pricings of this ProductPricingResponse.  # noqa: E501
        :rtype: list[ProductPricing]
        """
        return self._product_pricings

    @product_pricings.setter
    def product_pricings(self, product_pricings):
        """Sets the product_pricings of this ProductPricingResponse.

        List of Products  # noqa: E501

        :param product_pricings: The product_pricings of this ProductPricingResponse.  # noqa: E501
        :type: list[ProductPricing]
        """

        self._product_pricings = product_pricings

    @property
    def products_count(self):
        """Gets the products_count of this ProductPricingResponse.  # noqa: E501

        Total number of matching products found.  # noqa: E501

        :return: The products_count of this ProductPricingResponse.  # noqa: E501
        :rtype: int
        """
        return self._products_count

    @products_count.setter
    def products_count(self, products_count):
        """Sets the products_count of this ProductPricingResponse.

        Total number of matching products found.  # noqa: E501

        :param products_count: The products_count of this ProductPricingResponse.  # noqa: E501
        :type: int
        """

        self._products_count = products_count

    @property
    def settings_used(self):
        """Gets the settings_used of this ProductPricingResponse.  # noqa: E501


        :return: The settings_used of this ProductPricingResponse.  # noqa: E501
        :rtype: SettingsUsed
        """
        return self._settings_used

    @settings_used.setter
    def settings_used(self, settings_used):
        """Sets the settings_used of this ProductPricingResponse.


        :param settings_used: The settings_used of this ProductPricingResponse.  # noqa: E501
        :type: SettingsUsed
        """

        self._settings_used = settings_used

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
        if issubclass(ProductPricingResponse, dict):
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
        if not isinstance(other, ProductPricingResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
