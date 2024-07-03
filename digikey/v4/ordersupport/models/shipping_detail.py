# coding: utf-8

"""
    Order Details

    Retrieve information about current and past orders.  # noqa: E501

    OpenAPI spec version: v3
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class ShippingDetail(object):
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
        'carrier': 'str',
        'carrier_package_id': 'str',
        'date_transaction': 'str',
        'shipping_method': 'str',
        'tracking_url': 'str',
        'invoice_id': 'int',
        'canceled_or_voided': 'bool',
        'delivery_date': 'str'
    }

    attribute_map = {
        'carrier': 'Carrier',
        'carrier_package_id': 'CarrierPackageId',
        'date_transaction': 'DateTransaction',
        'shipping_method': 'ShippingMethod',
        'tracking_url': 'TrackingUrl',
        'invoice_id': 'InvoiceId',
        'canceled_or_voided': 'CanceledOrVoided',
        'delivery_date': 'DeliveryDate'
    }

    def __init__(self, carrier=None, carrier_package_id=None, date_transaction=None, shipping_method=None, tracking_url=None, invoice_id=None, canceled_or_voided=None, delivery_date=None):  # noqa: E501
        """ShippingDetail - a model defined in Swagger"""  # noqa: E501

        self._carrier = None
        self._carrier_package_id = None
        self._date_transaction = None
        self._shipping_method = None
        self._tracking_url = None
        self._invoice_id = None
        self._canceled_or_voided = None
        self._delivery_date = None
        self.discriminator = None

        if carrier is not None:
            self.carrier = carrier
        if carrier_package_id is not None:
            self.carrier_package_id = carrier_package_id
        if date_transaction is not None:
            self.date_transaction = date_transaction
        if shipping_method is not None:
            self.shipping_method = shipping_method
        if tracking_url is not None:
            self.tracking_url = tracking_url
        if invoice_id is not None:
            self.invoice_id = invoice_id
        if canceled_or_voided is not None:
            self.canceled_or_voided = canceled_or_voided
        if delivery_date is not None:
            self.delivery_date = delivery_date

    @property
    def carrier(self):
        """Gets the carrier of this ShippingDetail.  # noqa: E501

        Name of the carrier  # noqa: E501

        :return: The carrier of this ShippingDetail.  # noqa: E501
        :rtype: str
        """
        return self._carrier

    @carrier.setter
    def carrier(self, carrier):
        """Sets the carrier of this ShippingDetail.

        Name of the carrier  # noqa: E501

        :param carrier: The carrier of this ShippingDetail.  # noqa: E501
        :type: str
        """

        self._carrier = carrier

    @property
    def carrier_package_id(self):
        """Gets the carrier_package_id of this ShippingDetail.  # noqa: E501

        Id assigned by the carrier  # noqa: E501

        :return: The carrier_package_id of this ShippingDetail.  # noqa: E501
        :rtype: str
        """
        return self._carrier_package_id

    @carrier_package_id.setter
    def carrier_package_id(self, carrier_package_id):
        """Sets the carrier_package_id of this ShippingDetail.

        Id assigned by the carrier  # noqa: E501

        :param carrier_package_id: The carrier_package_id of this ShippingDetail.  # noqa: E501
        :type: str
        """

        self._carrier_package_id = carrier_package_id

    @property
    def date_transaction(self):
        """Gets the date_transaction of this ShippingDetail.  # noqa: E501

        Date that tracking number was generated in ISO 8601 format  # noqa: E501

        :return: The date_transaction of this ShippingDetail.  # noqa: E501
        :rtype: str
        """
        return self._date_transaction

    @date_transaction.setter
    def date_transaction(self, date_transaction):
        """Sets the date_transaction of this ShippingDetail.

        Date that tracking number was generated in ISO 8601 format  # noqa: E501

        :param date_transaction: The date_transaction of this ShippingDetail.  # noqa: E501
        :type: str
        """

        self._date_transaction = date_transaction

    @property
    def shipping_method(self):
        """Gets the shipping_method of this ShippingDetail.  # noqa: E501

        Shipping method used by this shipment  # noqa: E501

        :return: The shipping_method of this ShippingDetail.  # noqa: E501
        :rtype: str
        """
        return self._shipping_method

    @shipping_method.setter
    def shipping_method(self, shipping_method):
        """Sets the shipping_method of this ShippingDetail.

        Shipping method used by this shipment  # noqa: E501

        :param shipping_method: The shipping_method of this ShippingDetail.  # noqa: E501
        :type: str
        """

        self._shipping_method = shipping_method

    @property
    def tracking_url(self):
        """Gets the tracking_url of this ShippingDetail.  # noqa: E501


        :return: The tracking_url of this ShippingDetail.  # noqa: E501
        :rtype: str
        """
        return self._tracking_url

    @tracking_url.setter
    def tracking_url(self, tracking_url):
        """Sets the tracking_url of this ShippingDetail.


        :param tracking_url: The tracking_url of this ShippingDetail.  # noqa: E501
        :type: str
        """

        self._tracking_url = tracking_url

    @property
    def invoice_id(self):
        """Gets the invoice_id of this ShippingDetail.  # noqa: E501

        The Invoice Id for this shipment  # noqa: E501

        :return: The invoice_id of this ShippingDetail.  # noqa: E501
        :rtype: int
        """
        return self._invoice_id

    @invoice_id.setter
    def invoice_id(self, invoice_id):
        """Sets the invoice_id of this ShippingDetail.

        The Invoice Id for this shipment  # noqa: E501

        :param invoice_id: The invoice_id of this ShippingDetail.  # noqa: E501
        :type: int
        """

        self._invoice_id = invoice_id

    @property
    def canceled_or_voided(self):
        """Gets the canceled_or_voided of this ShippingDetail.  # noqa: E501

        Whether this individual detail has been canceled or voided.  # noqa: E501

        :return: The canceled_or_voided of this ShippingDetail.  # noqa: E501
        :rtype: bool
        """
        return self._canceled_or_voided

    @canceled_or_voided.setter
    def canceled_or_voided(self, canceled_or_voided):
        """Sets the canceled_or_voided of this ShippingDetail.

        Whether this individual detail has been canceled or voided.  # noqa: E501

        :param canceled_or_voided: The canceled_or_voided of this ShippingDetail.  # noqa: E501
        :type: bool
        """

        self._canceled_or_voided = canceled_or_voided

    @property
    def delivery_date(self):
        """Gets the delivery_date of this ShippingDetail.  # noqa: E501

        Date that the tracking number reports of delivery. If Tracking Number is not initiated by carrier or if  tracking number is expired the value of DeliveryDate will be empty  \"\"  # noqa: E501

        :return: The delivery_date of this ShippingDetail.  # noqa: E501
        :rtype: str
        """
        return self._delivery_date

    @delivery_date.setter
    def delivery_date(self, delivery_date):
        """Sets the delivery_date of this ShippingDetail.

        Date that the tracking number reports of delivery. If Tracking Number is not initiated by carrier or if  tracking number is expired the value of DeliveryDate will be empty  \"\"  # noqa: E501

        :param delivery_date: The delivery_date of this ShippingDetail.  # noqa: E501
        :type: str
        """

        self._delivery_date = delivery_date

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
        if issubclass(ShippingDetail, dict):
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
        if not isinstance(other, ShippingDetail):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
