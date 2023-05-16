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


class ShippingTrackingInfo(object):
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
        'shipping_carrier_id': 'str',
        'shipping_tracking_number': 'str',
        'shipping_tracking_url': 'str',
        'shipping_carrier_name': 'str'
    }

    attribute_map = {
        'shipping_carrier_id': 'shippingCarrierId',
        'shipping_tracking_number': 'shippingTrackingNumber',
        'shipping_tracking_url': 'shippingTrackingURL',
        'shipping_carrier_name': 'shippingCarrierName'
    }

    def __init__(self, shipping_carrier_id=None, shipping_tracking_number=None, shipping_tracking_url=None, shipping_carrier_name=None):  # noqa: E501
        """ShippingTrackingInfo - a model defined in Swagger"""  # noqa: E501

        self._shipping_carrier_id = None
        self._shipping_tracking_number = None
        self._shipping_tracking_url = None
        self._shipping_carrier_name = None
        self.discriminator = None

        if shipping_carrier_id is not None:
            self.shipping_carrier_id = shipping_carrier_id
        if shipping_tracking_number is not None:
            self.shipping_tracking_number = shipping_tracking_number
        if shipping_tracking_url is not None:
            self.shipping_tracking_url = shipping_tracking_url
        if shipping_carrier_name is not None:
            self.shipping_carrier_name = shipping_carrier_name

    @property
    def shipping_carrier_id(self):
        """Gets the shipping_carrier_id of this ShippingTrackingInfo.  # noqa: E501


        :return: The shipping_carrier_id of this ShippingTrackingInfo.  # noqa: E501
        :rtype: str
        """
        return self._shipping_carrier_id

    @shipping_carrier_id.setter
    def shipping_carrier_id(self, shipping_carrier_id):
        """Sets the shipping_carrier_id of this ShippingTrackingInfo.


        :param shipping_carrier_id: The shipping_carrier_id of this ShippingTrackingInfo.  # noqa: E501
        :type: str
        """

        self._shipping_carrier_id = shipping_carrier_id

    @property
    def shipping_tracking_number(self):
        """Gets the shipping_tracking_number of this ShippingTrackingInfo.  # noqa: E501


        :return: The shipping_tracking_number of this ShippingTrackingInfo.  # noqa: E501
        :rtype: str
        """
        return self._shipping_tracking_number

    @shipping_tracking_number.setter
    def shipping_tracking_number(self, shipping_tracking_number):
        """Sets the shipping_tracking_number of this ShippingTrackingInfo.


        :param shipping_tracking_number: The shipping_tracking_number of this ShippingTrackingInfo.  # noqa: E501
        :type: str
        """

        self._shipping_tracking_number = shipping_tracking_number

    @property
    def shipping_tracking_url(self):
        """Gets the shipping_tracking_url of this ShippingTrackingInfo.  # noqa: E501


        :return: The shipping_tracking_url of this ShippingTrackingInfo.  # noqa: E501
        :rtype: str
        """
        return self._shipping_tracking_url

    @shipping_tracking_url.setter
    def shipping_tracking_url(self, shipping_tracking_url):
        """Sets the shipping_tracking_url of this ShippingTrackingInfo.


        :param shipping_tracking_url: The shipping_tracking_url of this ShippingTrackingInfo.  # noqa: E501
        :type: str
        """

        self._shipping_tracking_url = shipping_tracking_url

    @property
    def shipping_carrier_name(self):
        """Gets the shipping_carrier_name of this ShippingTrackingInfo.  # noqa: E501


        :return: The shipping_carrier_name of this ShippingTrackingInfo.  # noqa: E501
        :rtype: str
        """
        return self._shipping_carrier_name

    @shipping_carrier_name.setter
    def shipping_carrier_name(self, shipping_carrier_name):
        """Sets the shipping_carrier_name of this ShippingTrackingInfo.


        :param shipping_carrier_name: The shipping_carrier_name of this ShippingTrackingInfo.  # noqa: E501
        :type: str
        """

        self._shipping_carrier_name = shipping_carrier_name

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
        if issubclass(ShippingTrackingInfo, dict):
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
        if not isinstance(other, ShippingTrackingInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
