# coding: utf-8

"""
    Orders

    API operations for managing orders as well as refunds and incidents as they relate to the order  # noqa: E501

    OpenAPI spec version: suppliers-v1
    Contact: MarketplaceAPISupport@digikey.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class OrderCancellation(object):
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
        'amount': 'float',
        'currency_iso_code': 'str',
        'quantity': 'int',
        'reason_code': 'str',
        'reason_label': 'str',
        'create_date_utc': 'datetime'
    }

    attribute_map = {
        'amount': 'amount',
        'currency_iso_code': 'currencyISOCode',
        'quantity': 'quantity',
        'reason_code': 'reasonCode',
        'reason_label': 'reasonLabel',
        'create_date_utc': 'createDateUtc'
    }

    def __init__(self, amount=None, currency_iso_code=None, quantity=None, reason_code=None, reason_label=None, create_date_utc=None):  # noqa: E501
        """OrderCancellation - a model defined in Swagger"""  # noqa: E501

        self._amount = None
        self._currency_iso_code = None
        self._quantity = None
        self._reason_code = None
        self._reason_label = None
        self._create_date_utc = None
        self.discriminator = None

        if amount is not None:
            self.amount = amount
        if currency_iso_code is not None:
            self.currency_iso_code = currency_iso_code
        if quantity is not None:
            self.quantity = quantity
        if reason_code is not None:
            self.reason_code = reason_code
        if reason_label is not None:
            self.reason_label = reason_label
        if create_date_utc is not None:
            self.create_date_utc = create_date_utc

    @property
    def amount(self):
        """Gets the amount of this OrderCancellation.  # noqa: E501


        :return: The amount of this OrderCancellation.  # noqa: E501
        :rtype: float
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this OrderCancellation.


        :param amount: The amount of this OrderCancellation.  # noqa: E501
        :type: float
        """

        self._amount = amount

    @property
    def currency_iso_code(self):
        """Gets the currency_iso_code of this OrderCancellation.  # noqa: E501


        :return: The currency_iso_code of this OrderCancellation.  # noqa: E501
        :rtype: str
        """
        return self._currency_iso_code

    @currency_iso_code.setter
    def currency_iso_code(self, currency_iso_code):
        """Sets the currency_iso_code of this OrderCancellation.


        :param currency_iso_code: The currency_iso_code of this OrderCancellation.  # noqa: E501
        :type: str
        """

        self._currency_iso_code = currency_iso_code

    @property
    def quantity(self):
        """Gets the quantity of this OrderCancellation.  # noqa: E501


        :return: The quantity of this OrderCancellation.  # noqa: E501
        :rtype: int
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this OrderCancellation.


        :param quantity: The quantity of this OrderCancellation.  # noqa: E501
        :type: int
        """

        self._quantity = quantity

    @property
    def reason_code(self):
        """Gets the reason_code of this OrderCancellation.  # noqa: E501


        :return: The reason_code of this OrderCancellation.  # noqa: E501
        :rtype: str
        """
        return self._reason_code

    @reason_code.setter
    def reason_code(self, reason_code):
        """Sets the reason_code of this OrderCancellation.


        :param reason_code: The reason_code of this OrderCancellation.  # noqa: E501
        :type: str
        """

        self._reason_code = reason_code

    @property
    def reason_label(self):
        """Gets the reason_label of this OrderCancellation.  # noqa: E501


        :return: The reason_label of this OrderCancellation.  # noqa: E501
        :rtype: str
        """
        return self._reason_label

    @reason_label.setter
    def reason_label(self, reason_label):
        """Sets the reason_label of this OrderCancellation.


        :param reason_label: The reason_label of this OrderCancellation.  # noqa: E501
        :type: str
        """

        self._reason_label = reason_label

    @property
    def create_date_utc(self):
        """Gets the create_date_utc of this OrderCancellation.  # noqa: E501


        :return: The create_date_utc of this OrderCancellation.  # noqa: E501
        :rtype: datetime
        """
        return self._create_date_utc

    @create_date_utc.setter
    def create_date_utc(self, create_date_utc):
        """Sets the create_date_utc of this OrderCancellation.


        :param create_date_utc: The create_date_utc of this OrderCancellation.  # noqa: E501
        :type: datetime
        """

        self._create_date_utc = create_date_utc

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
        if issubclass(OrderCancellation, dict):
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
        if not isinstance(other, OrderCancellation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other