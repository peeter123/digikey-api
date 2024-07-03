# coding: utf-8

"""
    Order Details

    Retrieve information about current and past orders.  # noqa: E501

    OpenAPI spec version: v3
    Contact: api.contact@digikey.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class SalesorderHistoryItem(object):
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
        'salesorder_id': 'int',
        'customer_id': 'int',
        'date_entered': 'str',
        'purchase_order': 'str'
    }

    attribute_map = {
        'salesorder_id': 'SalesorderId',
        'customer_id': 'CustomerId',
        'date_entered': 'DateEntered',
        'purchase_order': 'PurchaseOrder'
    }

    def __init__(self, salesorder_id=None, customer_id=None, date_entered=None, purchase_order=None):  # noqa: E501
        """SalesorderHistoryItem - a model defined in Swagger"""  # noqa: E501

        self._salesorder_id = None
        self._customer_id = None
        self._date_entered = None
        self._purchase_order = None
        self.discriminator = None

        if salesorder_id is not None:
            self.salesorder_id = salesorder_id
        if customer_id is not None:
            self.customer_id = customer_id
        if date_entered is not None:
            self.date_entered = date_entered
        if purchase_order is not None:
            self.purchase_order = purchase_order

    @property
    def salesorder_id(self):
        """Gets the salesorder_id of this SalesorderHistoryItem.  # noqa: E501

        The Salesorder Id. You can use this Id to look up details on the order.  # noqa: E501

        :return: The salesorder_id of this SalesorderHistoryItem.  # noqa: E501
        :rtype: int
        """
        return self._salesorder_id

    @salesorder_id.setter
    def salesorder_id(self, salesorder_id):
        """Sets the salesorder_id of this SalesorderHistoryItem.

        The Salesorder Id. You can use this Id to look up details on the order.  # noqa: E501

        :param salesorder_id: The salesorder_id of this SalesorderHistoryItem.  # noqa: E501
        :type: int
        """

        self._salesorder_id = salesorder_id

    @property
    def customer_id(self):
        """Gets the customer_id of this SalesorderHistoryItem.  # noqa: E501

        The CustomerId associated with the Salesorder  # noqa: E501

        :return: The customer_id of this SalesorderHistoryItem.  # noqa: E501
        :rtype: int
        """
        return self._customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        """Sets the customer_id of this SalesorderHistoryItem.

        The CustomerId associated with the Salesorder  # noqa: E501

        :param customer_id: The customer_id of this SalesorderHistoryItem.  # noqa: E501
        :type: int
        """

        self._customer_id = customer_id

    @property
    def date_entered(self):
        """Gets the date_entered of this SalesorderHistoryItem.  # noqa: E501

        Date in which the order was entered in ISO 8601 format.  # noqa: E501

        :return: The date_entered of this SalesorderHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._date_entered

    @date_entered.setter
    def date_entered(self, date_entered):
        """Sets the date_entered of this SalesorderHistoryItem.

        Date in which the order was entered in ISO 8601 format.  # noqa: E501

        :param date_entered: The date_entered of this SalesorderHistoryItem.  # noqa: E501
        :type: str
        """

        self._date_entered = date_entered

    @property
    def purchase_order(self):
        """Gets the purchase_order of this SalesorderHistoryItem.  # noqa: E501

        Purchase order if available  # noqa: E501

        :return: The purchase_order of this SalesorderHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._purchase_order

    @purchase_order.setter
    def purchase_order(self, purchase_order):
        """Sets the purchase_order of this SalesorderHistoryItem.

        Purchase order if available  # noqa: E501

        :param purchase_order: The purchase_order of this SalesorderHistoryItem.  # noqa: E501
        :type: str
        """

        self._purchase_order = purchase_order

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
        if issubclass(SalesorderHistoryItem, dict):
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
        if not isinstance(other, SalesorderHistoryItem):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
