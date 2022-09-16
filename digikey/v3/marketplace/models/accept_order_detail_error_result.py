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


class AcceptOrderDetailErrorResult(object):
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
        'error_message': 'str',
        'item': 'AcceptOrderDetailModel'
    }

    attribute_map = {
        'error_message': 'errorMessage',
        'item': 'item'
    }

    def __init__(self, error_message=None, item=None):  # noqa: E501
        """AcceptOrderDetailErrorResult - a model defined in Swagger"""  # noqa: E501

        self._error_message = None
        self._item = None
        self.discriminator = None

        if error_message is not None:
            self.error_message = error_message
        if item is not None:
            self.item = item

    @property
    def error_message(self):
        """Gets the error_message of this AcceptOrderDetailErrorResult.  # noqa: E501


        :return: The error_message of this AcceptOrderDetailErrorResult.  # noqa: E501
        :rtype: str
        """
        return self._error_message

    @error_message.setter
    def error_message(self, error_message):
        """Sets the error_message of this AcceptOrderDetailErrorResult.


        :param error_message: The error_message of this AcceptOrderDetailErrorResult.  # noqa: E501
        :type: str
        """

        self._error_message = error_message

    @property
    def item(self):
        """Gets the item of this AcceptOrderDetailErrorResult.  # noqa: E501


        :return: The item of this AcceptOrderDetailErrorResult.  # noqa: E501
        :rtype: AcceptOrderDetailModel
        """
        return self._item

    @item.setter
    def item(self, item):
        """Sets the item of this AcceptOrderDetailErrorResult.


        :param item: The item of this AcceptOrderDetailErrorResult.  # noqa: E501
        :type: AcceptOrderDetailModel
        """

        self._item = item

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
        if issubclass(AcceptOrderDetailErrorResult, dict):
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
        if not isinstance(other, AcceptOrderDetailErrorResult):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other