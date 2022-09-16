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


class OrderExpanded(object):
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
        'supplier_name': 'str',
        'shipping_method_label': 'str',
        'shipping_region_label': 'str',
        'id': 'str',
        'business_id': 'str',
        'accounting_document_id': 'str',
        'accounting_document_number': 'str',
        'payment_status': 'str',
        'create_date_utc': 'datetime',
        'last_update_date_utc': 'datetime',
        'customer_debited_date_utc': 'datetime',
        'acceptance_rejection_date_utc': 'datetime',
        'received_date_utc': 'datetime',
        'shipped_date_utc': 'datetime',
        'cancellation_date_utc': 'datetime',
        'shipping_deadline_utc': 'datetime',
        'lead_time_to_ship': 'int',
        'order_state': 'str',
        'customer': 'Customer',
        'supplier_id': 'str',
        'supplier_legacy_id': 'int',
        'supplier_business_id': 'str',
        'order_details': 'list[OrderDetail]',
        'additional_fields': 'list[AdditionalField]',
        'subtotal_price': 'float',
        'total_price': 'float',
        'total_discount_fee': 'float',
        'adjusted_subtotal_price': 'float',
        'adjusted_total_price': 'float',
        'adjusted_total_discount_fee': 'float',
        'shipping_price': 'float',
        'adjusted_shipping_price': 'float',
        'shipping_tracking_info_list': 'list[ShippingTrackingInfo]',
        'shipping_method_code': 'str',
        'shipping_region_code': 'str',
        'tracking_required': 'bool',
        'refunds': 'list[OrderRefund]',
        'supplier_invoice_number': 'str'
    }

    attribute_map = {
        'supplier_name': 'supplierName',
        'shipping_method_label': 'shippingMethodLabel',
        'shipping_region_label': 'shippingRegionLabel',
        'id': 'id',
        'business_id': 'businessId',
        'accounting_document_id': 'accountingDocumentId',
        'accounting_document_number': 'accountingDocumentNumber',
        'payment_status': 'paymentStatus',
        'create_date_utc': 'createDateUtc',
        'last_update_date_utc': 'lastUpdateDateUtc',
        'customer_debited_date_utc': 'customerDebitedDateUtc',
        'acceptance_rejection_date_utc': 'acceptanceRejectionDateUtc',
        'received_date_utc': 'receivedDateUtc',
        'shipped_date_utc': 'shippedDateUtc',
        'cancellation_date_utc': 'cancellationDateUtc',
        'shipping_deadline_utc': 'shippingDeadlineUtc',
        'lead_time_to_ship': 'leadTimeToShip',
        'order_state': 'orderState',
        'customer': 'customer',
        'supplier_id': 'supplierId',
        'supplier_legacy_id': 'supplierLegacyId',
        'supplier_business_id': 'supplierBusinessId',
        'order_details': 'orderDetails',
        'additional_fields': 'additionalFields',
        'subtotal_price': 'subtotalPrice',
        'total_price': 'totalPrice',
        'total_discount_fee': 'totalDiscountFee',
        'adjusted_subtotal_price': 'adjustedSubtotalPrice',
        'adjusted_total_price': 'adjustedTotalPrice',
        'adjusted_total_discount_fee': 'adjustedTotalDiscountFee',
        'shipping_price': 'shippingPrice',
        'adjusted_shipping_price': 'adjustedShippingPrice',
        'shipping_tracking_info_list': 'shippingTrackingInfoList',
        'shipping_method_code': 'shippingMethodCode',
        'shipping_region_code': 'shippingRegionCode',
        'tracking_required': 'trackingRequired',
        'refunds': 'refunds',
        'supplier_invoice_number': 'supplierInvoiceNumber'
    }

    def __init__(self, supplier_name=None, shipping_method_label=None, shipping_region_label=None, id=None, business_id=None, accounting_document_id=None, accounting_document_number=None, payment_status=None, create_date_utc=None, last_update_date_utc=None, customer_debited_date_utc=None, acceptance_rejection_date_utc=None, received_date_utc=None, shipped_date_utc=None, cancellation_date_utc=None, shipping_deadline_utc=None, lead_time_to_ship=None, order_state=None, customer=None, supplier_id=None, supplier_legacy_id=None, supplier_business_id=None, order_details=None, additional_fields=None, subtotal_price=None, total_price=None, total_discount_fee=None, adjusted_subtotal_price=None, adjusted_total_price=None, adjusted_total_discount_fee=None, shipping_price=None, adjusted_shipping_price=None, shipping_tracking_info_list=None, shipping_method_code=None, shipping_region_code=None, tracking_required=None, refunds=None, supplier_invoice_number=None):  # noqa: E501
        """OrderExpanded - a model defined in Swagger"""  # noqa: E501

        self._supplier_name = None
        self._shipping_method_label = None
        self._shipping_region_label = None
        self._id = None
        self._business_id = None
        self._accounting_document_id = None
        self._accounting_document_number = None
        self._payment_status = None
        self._create_date_utc = None
        self._last_update_date_utc = None
        self._customer_debited_date_utc = None
        self._acceptance_rejection_date_utc = None
        self._received_date_utc = None
        self._shipped_date_utc = None
        self._cancellation_date_utc = None
        self._shipping_deadline_utc = None
        self._lead_time_to_ship = None
        self._order_state = None
        self._customer = None
        self._supplier_id = None
        self._supplier_legacy_id = None
        self._supplier_business_id = None
        self._order_details = None
        self._additional_fields = None
        self._subtotal_price = None
        self._total_price = None
        self._total_discount_fee = None
        self._adjusted_subtotal_price = None
        self._adjusted_total_price = None
        self._adjusted_total_discount_fee = None
        self._shipping_price = None
        self._adjusted_shipping_price = None
        self._shipping_tracking_info_list = None
        self._shipping_method_code = None
        self._shipping_region_code = None
        self._tracking_required = None
        self._refunds = None
        self._supplier_invoice_number = None
        self.discriminator = None

        if supplier_name is not None:
            self.supplier_name = supplier_name
        if shipping_method_label is not None:
            self.shipping_method_label = shipping_method_label
        if shipping_region_label is not None:
            self.shipping_region_label = shipping_region_label
        if id is not None:
            self.id = id
        if business_id is not None:
            self.business_id = business_id
        if accounting_document_id is not None:
            self.accounting_document_id = accounting_document_id
        if accounting_document_number is not None:
            self.accounting_document_number = accounting_document_number
        if payment_status is not None:
            self.payment_status = payment_status
        if create_date_utc is not None:
            self.create_date_utc = create_date_utc
        if last_update_date_utc is not None:
            self.last_update_date_utc = last_update_date_utc
        if customer_debited_date_utc is not None:
            self.customer_debited_date_utc = customer_debited_date_utc
        if acceptance_rejection_date_utc is not None:
            self.acceptance_rejection_date_utc = acceptance_rejection_date_utc
        if received_date_utc is not None:
            self.received_date_utc = received_date_utc
        if shipped_date_utc is not None:
            self.shipped_date_utc = shipped_date_utc
        if cancellation_date_utc is not None:
            self.cancellation_date_utc = cancellation_date_utc
        if shipping_deadline_utc is not None:
            self.shipping_deadline_utc = shipping_deadline_utc
        if lead_time_to_ship is not None:
            self.lead_time_to_ship = lead_time_to_ship
        if order_state is not None:
            self.order_state = order_state
        if customer is not None:
            self.customer = customer
        if supplier_id is not None:
            self.supplier_id = supplier_id
        if supplier_legacy_id is not None:
            self.supplier_legacy_id = supplier_legacy_id
        if supplier_business_id is not None:
            self.supplier_business_id = supplier_business_id
        if order_details is not None:
            self.order_details = order_details
        if additional_fields is not None:
            self.additional_fields = additional_fields
        if subtotal_price is not None:
            self.subtotal_price = subtotal_price
        if total_price is not None:
            self.total_price = total_price
        if total_discount_fee is not None:
            self.total_discount_fee = total_discount_fee
        if adjusted_subtotal_price is not None:
            self.adjusted_subtotal_price = adjusted_subtotal_price
        if adjusted_total_price is not None:
            self.adjusted_total_price = adjusted_total_price
        if adjusted_total_discount_fee is not None:
            self.adjusted_total_discount_fee = adjusted_total_discount_fee
        if shipping_price is not None:
            self.shipping_price = shipping_price
        if adjusted_shipping_price is not None:
            self.adjusted_shipping_price = adjusted_shipping_price
        if shipping_tracking_info_list is not None:
            self.shipping_tracking_info_list = shipping_tracking_info_list
        if shipping_method_code is not None:
            self.shipping_method_code = shipping_method_code
        if shipping_region_code is not None:
            self.shipping_region_code = shipping_region_code
        if tracking_required is not None:
            self.tracking_required = tracking_required
        if refunds is not None:
            self.refunds = refunds
        if supplier_invoice_number is not None:
            self.supplier_invoice_number = supplier_invoice_number

    @property
    def supplier_name(self):
        """Gets the supplier_name of this OrderExpanded.  # noqa: E501


        :return: The supplier_name of this OrderExpanded.  # noqa: E501
        :rtype: str
        """
        return self._supplier_name

    @supplier_name.setter
    def supplier_name(self, supplier_name):
        """Sets the supplier_name of this OrderExpanded.


        :param supplier_name: The supplier_name of this OrderExpanded.  # noqa: E501
        :type: str
        """

        self._supplier_name = supplier_name

    @property
    def shipping_method_label(self):
        """Gets the shipping_method_label of this OrderExpanded.  # noqa: E501


        :return: The shipping_method_label of this OrderExpanded.  # noqa: E501
        :rtype: str
        """
        return self._shipping_method_label

    @shipping_method_label.setter
    def shipping_method_label(self, shipping_method_label):
        """Sets the shipping_method_label of this OrderExpanded.


        :param shipping_method_label: The shipping_method_label of this OrderExpanded.  # noqa: E501
        :type: str
        """

        self._shipping_method_label = shipping_method_label

    @property
    def shipping_region_label(self):
        """Gets the shipping_region_label of this OrderExpanded.  # noqa: E501


        :return: The shipping_region_label of this OrderExpanded.  # noqa: E501
        :rtype: str
        """
        return self._shipping_region_label

    @shipping_region_label.setter
    def shipping_region_label(self, shipping_region_label):
        """Sets the shipping_region_label of this OrderExpanded.


        :param shipping_region_label: The shipping_region_label of this OrderExpanded.  # noqa: E501
        :type: str
        """

        self._shipping_region_label = shipping_region_label

    @property
    def id(self):
        """Gets the id of this OrderExpanded.  # noqa: E501


        :return: The id of this OrderExpanded.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this OrderExpanded.


        :param id: The id of this OrderExpanded.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def business_id(self):
        """Gets the business_id of this OrderExpanded.  # noqa: E501


        :return: The business_id of this OrderExpanded.  # noqa: E501
        :rtype: str
        """
        return self._business_id

    @business_id.setter
    def business_id(self, business_id):
        """Sets the business_id of this OrderExpanded.


        :param business_id: The business_id of this OrderExpanded.  # noqa: E501
        :type: str
        """

        self._business_id = business_id

    @property
    def accounting_document_id(self):
        """Gets the accounting_document_id of this OrderExpanded.  # noqa: E501


        :return: The accounting_document_id of this OrderExpanded.  # noqa: E501
        :rtype: str
        """
        return self._accounting_document_id

    @accounting_document_id.setter
    def accounting_document_id(self, accounting_document_id):
        """Sets the accounting_document_id of this OrderExpanded.


        :param accounting_document_id: The accounting_document_id of this OrderExpanded.  # noqa: E501
        :type: str
        """

        self._accounting_document_id = accounting_document_id

    @property
    def accounting_document_number(self):
        """Gets the accounting_document_number of this OrderExpanded.  # noqa: E501


        :return: The accounting_document_number of this OrderExpanded.  # noqa: E501
        :rtype: str
        """
        return self._accounting_document_number

    @accounting_document_number.setter
    def accounting_document_number(self, accounting_document_number):
        """Sets the accounting_document_number of this OrderExpanded.


        :param accounting_document_number: The accounting_document_number of this OrderExpanded.  # noqa: E501
        :type: str
        """

        self._accounting_document_number = accounting_document_number

    @property
    def payment_status(self):
        """Gets the payment_status of this OrderExpanded.  # noqa: E501


        :return: The payment_status of this OrderExpanded.  # noqa: E501
        :rtype: str
        """
        return self._payment_status

    @payment_status.setter
    def payment_status(self, payment_status):
        """Sets the payment_status of this OrderExpanded.


        :param payment_status: The payment_status of this OrderExpanded.  # noqa: E501
        :type: str
        """
        allowed_values = ["Pending", "Payable", "Paid", "Invoiced"]  # noqa: E501
        if payment_status not in allowed_values:
            raise ValueError(
                "Invalid value for `payment_status` ({0}), must be one of {1}"  # noqa: E501
                .format(payment_status, allowed_values)
            )

        self._payment_status = payment_status

    @property
    def create_date_utc(self):
        """Gets the create_date_utc of this OrderExpanded.  # noqa: E501


        :return: The create_date_utc of this OrderExpanded.  # noqa: E501
        :rtype: datetime
        """
        return self._create_date_utc

    @create_date_utc.setter
    def create_date_utc(self, create_date_utc):
        """Sets the create_date_utc of this OrderExpanded.


        :param create_date_utc: The create_date_utc of this OrderExpanded.  # noqa: E501
        :type: datetime
        """

        self._create_date_utc = create_date_utc

    @property
    def last_update_date_utc(self):
        """Gets the last_update_date_utc of this OrderExpanded.  # noqa: E501


        :return: The last_update_date_utc of this OrderExpanded.  # noqa: E501
        :rtype: datetime
        """
        return self._last_update_date_utc

    @last_update_date_utc.setter
    def last_update_date_utc(self, last_update_date_utc):
        """Sets the last_update_date_utc of this OrderExpanded.


        :param last_update_date_utc: The last_update_date_utc of this OrderExpanded.  # noqa: E501
        :type: datetime
        """

        self._last_update_date_utc = last_update_date_utc

    @property
    def customer_debited_date_utc(self):
        """Gets the customer_debited_date_utc of this OrderExpanded.  # noqa: E501


        :return: The customer_debited_date_utc of this OrderExpanded.  # noqa: E501
        :rtype: datetime
        """
        return self._customer_debited_date_utc

    @customer_debited_date_utc.setter
    def customer_debited_date_utc(self, customer_debited_date_utc):
        """Sets the customer_debited_date_utc of this OrderExpanded.


        :param customer_debited_date_utc: The customer_debited_date_utc of this OrderExpanded.  # noqa: E501
        :type: datetime
        """

        self._customer_debited_date_utc = customer_debited_date_utc

    @property
    def acceptance_rejection_date_utc(self):
        """Gets the acceptance_rejection_date_utc of this OrderExpanded.  # noqa: E501


        :return: The acceptance_rejection_date_utc of this OrderExpanded.  # noqa: E501
        :rtype: datetime
        """
        return self._acceptance_rejection_date_utc

    @acceptance_rejection_date_utc.setter
    def acceptance_rejection_date_utc(self, acceptance_rejection_date_utc):
        """Sets the acceptance_rejection_date_utc of this OrderExpanded.


        :param acceptance_rejection_date_utc: The acceptance_rejection_date_utc of this OrderExpanded.  # noqa: E501
        :type: datetime
        """

        self._acceptance_rejection_date_utc = acceptance_rejection_date_utc

    @property
    def received_date_utc(self):
        """Gets the received_date_utc of this OrderExpanded.  # noqa: E501


        :return: The received_date_utc of this OrderExpanded.  # noqa: E501
        :rtype: datetime
        """
        return self._received_date_utc

    @received_date_utc.setter
    def received_date_utc(self, received_date_utc):
        """Sets the received_date_utc of this OrderExpanded.


        :param received_date_utc: The received_date_utc of this OrderExpanded.  # noqa: E501
        :type: datetime
        """

        self._received_date_utc = received_date_utc

    @property
    def shipped_date_utc(self):
        """Gets the shipped_date_utc of this OrderExpanded.  # noqa: E501


        :return: The shipped_date_utc of this OrderExpanded.  # noqa: E501
        :rtype: datetime
        """
        return self._shipped_date_utc

    @shipped_date_utc.setter
    def shipped_date_utc(self, shipped_date_utc):
        """Sets the shipped_date_utc of this OrderExpanded.


        :param shipped_date_utc: The shipped_date_utc of this OrderExpanded.  # noqa: E501
        :type: datetime
        """

        self._shipped_date_utc = shipped_date_utc

    @property
    def cancellation_date_utc(self):
        """Gets the cancellation_date_utc of this OrderExpanded.  # noqa: E501


        :return: The cancellation_date_utc of this OrderExpanded.  # noqa: E501
        :rtype: datetime
        """
        return self._cancellation_date_utc

    @cancellation_date_utc.setter
    def cancellation_date_utc(self, cancellation_date_utc):
        """Sets the cancellation_date_utc of this OrderExpanded.


        :param cancellation_date_utc: The cancellation_date_utc of this OrderExpanded.  # noqa: E501
        :type: datetime
        """

        self._cancellation_date_utc = cancellation_date_utc

    @property
    def shipping_deadline_utc(self):
        """Gets the shipping_deadline_utc of this OrderExpanded.  # noqa: E501


        :return: The shipping_deadline_utc of this OrderExpanded.  # noqa: E501
        :rtype: datetime
        """
        return self._shipping_deadline_utc

    @shipping_deadline_utc.setter
    def shipping_deadline_utc(self, shipping_deadline_utc):
        """Sets the shipping_deadline_utc of this OrderExpanded.


        :param shipping_deadline_utc: The shipping_deadline_utc of this OrderExpanded.  # noqa: E501
        :type: datetime
        """

        self._shipping_deadline_utc = shipping_deadline_utc

    @property
    def lead_time_to_ship(self):
        """Gets the lead_time_to_ship of this OrderExpanded.  # noqa: E501


        :return: The lead_time_to_ship of this OrderExpanded.  # noqa: E501
        :rtype: int
        """
        return self._lead_time_to_ship

    @lead_time_to_ship.setter
    def lead_time_to_ship(self, lead_time_to_ship):
        """Sets the lead_time_to_ship of this OrderExpanded.


        :param lead_time_to_ship: The lead_time_to_ship of this OrderExpanded.  # noqa: E501
        :type: int
        """

        self._lead_time_to_ship = lead_time_to_ship

    @property
    def order_state(self):
        """Gets the order_state of this OrderExpanded.  # noqa: E501


        :return: The order_state of this OrderExpanded.  # noqa: E501
        :rtype: str
        """
        return self._order_state

    @order_state.setter
    def order_state(self, order_state):
        """Sets the order_state of this OrderExpanded.


        :param order_state: The order_state of this OrderExpanded.  # noqa: E501
        :type: str
        """
        allowed_values = ["WaitingAcceptance", "Accepted", "ShippingInProgress", "Shipped", "Received", "IncidentOpen", "Refunded", "Closed", "Cancelled", "Rejected"]  # noqa: E501
        if order_state not in allowed_values:
            raise ValueError(
                "Invalid value for `order_state` ({0}), must be one of {1}"  # noqa: E501
                .format(order_state, allowed_values)
            )

        self._order_state = order_state

    @property
    def customer(self):
        """Gets the customer of this OrderExpanded.  # noqa: E501


        :return: The customer of this OrderExpanded.  # noqa: E501
        :rtype: Customer
        """
        return self._customer

    @customer.setter
    def customer(self, customer):
        """Sets the customer of this OrderExpanded.


        :param customer: The customer of this OrderExpanded.  # noqa: E501
        :type: Customer
        """

        self._customer = customer

    @property
    def supplier_id(self):
        """Gets the supplier_id of this OrderExpanded.  # noqa: E501


        :return: The supplier_id of this OrderExpanded.  # noqa: E501
        :rtype: str
        """
        return self._supplier_id

    @supplier_id.setter
    def supplier_id(self, supplier_id):
        """Sets the supplier_id of this OrderExpanded.


        :param supplier_id: The supplier_id of this OrderExpanded.  # noqa: E501
        :type: str
        """

        self._supplier_id = supplier_id

    @property
    def supplier_legacy_id(self):
        """Gets the supplier_legacy_id of this OrderExpanded.  # noqa: E501


        :return: The supplier_legacy_id of this OrderExpanded.  # noqa: E501
        :rtype: int
        """
        return self._supplier_legacy_id

    @supplier_legacy_id.setter
    def supplier_legacy_id(self, supplier_legacy_id):
        """Sets the supplier_legacy_id of this OrderExpanded.


        :param supplier_legacy_id: The supplier_legacy_id of this OrderExpanded.  # noqa: E501
        :type: int
        """

        self._supplier_legacy_id = supplier_legacy_id

    @property
    def supplier_business_id(self):
        """Gets the supplier_business_id of this OrderExpanded.  # noqa: E501


        :return: The supplier_business_id of this OrderExpanded.  # noqa: E501
        :rtype: str
        """
        return self._supplier_business_id

    @supplier_business_id.setter
    def supplier_business_id(self, supplier_business_id):
        """Sets the supplier_business_id of this OrderExpanded.


        :param supplier_business_id: The supplier_business_id of this OrderExpanded.  # noqa: E501
        :type: str
        """

        self._supplier_business_id = supplier_business_id

    @property
    def order_details(self):
        """Gets the order_details of this OrderExpanded.  # noqa: E501


        :return: The order_details of this OrderExpanded.  # noqa: E501
        :rtype: list[OrderDetail]
        """
        return self._order_details

    @order_details.setter
    def order_details(self, order_details):
        """Sets the order_details of this OrderExpanded.


        :param order_details: The order_details of this OrderExpanded.  # noqa: E501
        :type: list[OrderDetail]
        """

        self._order_details = order_details

    @property
    def additional_fields(self):
        """Gets the additional_fields of this OrderExpanded.  # noqa: E501


        :return: The additional_fields of this OrderExpanded.  # noqa: E501
        :rtype: list[AdditionalField]
        """
        return self._additional_fields

    @additional_fields.setter
    def additional_fields(self, additional_fields):
        """Sets the additional_fields of this OrderExpanded.


        :param additional_fields: The additional_fields of this OrderExpanded.  # noqa: E501
        :type: list[AdditionalField]
        """

        self._additional_fields = additional_fields

    @property
    def subtotal_price(self):
        """Gets the subtotal_price of this OrderExpanded.  # noqa: E501


        :return: The subtotal_price of this OrderExpanded.  # noqa: E501
        :rtype: float
        """
        return self._subtotal_price

    @subtotal_price.setter
    def subtotal_price(self, subtotal_price):
        """Sets the subtotal_price of this OrderExpanded.


        :param subtotal_price: The subtotal_price of this OrderExpanded.  # noqa: E501
        :type: float
        """

        self._subtotal_price = subtotal_price

    @property
    def total_price(self):
        """Gets the total_price of this OrderExpanded.  # noqa: E501


        :return: The total_price of this OrderExpanded.  # noqa: E501
        :rtype: float
        """
        return self._total_price

    @total_price.setter
    def total_price(self, total_price):
        """Sets the total_price of this OrderExpanded.


        :param total_price: The total_price of this OrderExpanded.  # noqa: E501
        :type: float
        """

        self._total_price = total_price

    @property
    def total_discount_fee(self):
        """Gets the total_discount_fee of this OrderExpanded.  # noqa: E501


        :return: The total_discount_fee of this OrderExpanded.  # noqa: E501
        :rtype: float
        """
        return self._total_discount_fee

    @total_discount_fee.setter
    def total_discount_fee(self, total_discount_fee):
        """Sets the total_discount_fee of this OrderExpanded.


        :param total_discount_fee: The total_discount_fee of this OrderExpanded.  # noqa: E501
        :type: float
        """

        self._total_discount_fee = total_discount_fee

    @property
    def adjusted_subtotal_price(self):
        """Gets the adjusted_subtotal_price of this OrderExpanded.  # noqa: E501


        :return: The adjusted_subtotal_price of this OrderExpanded.  # noqa: E501
        :rtype: float
        """
        return self._adjusted_subtotal_price

    @adjusted_subtotal_price.setter
    def adjusted_subtotal_price(self, adjusted_subtotal_price):
        """Sets the adjusted_subtotal_price of this OrderExpanded.


        :param adjusted_subtotal_price: The adjusted_subtotal_price of this OrderExpanded.  # noqa: E501
        :type: float
        """

        self._adjusted_subtotal_price = adjusted_subtotal_price

    @property
    def adjusted_total_price(self):
        """Gets the adjusted_total_price of this OrderExpanded.  # noqa: E501


        :return: The adjusted_total_price of this OrderExpanded.  # noqa: E501
        :rtype: float
        """
        return self._adjusted_total_price

    @adjusted_total_price.setter
    def adjusted_total_price(self, adjusted_total_price):
        """Sets the adjusted_total_price of this OrderExpanded.


        :param adjusted_total_price: The adjusted_total_price of this OrderExpanded.  # noqa: E501
        :type: float
        """

        self._adjusted_total_price = adjusted_total_price

    @property
    def adjusted_total_discount_fee(self):
        """Gets the adjusted_total_discount_fee of this OrderExpanded.  # noqa: E501


        :return: The adjusted_total_discount_fee of this OrderExpanded.  # noqa: E501
        :rtype: float
        """
        return self._adjusted_total_discount_fee

    @adjusted_total_discount_fee.setter
    def adjusted_total_discount_fee(self, adjusted_total_discount_fee):
        """Sets the adjusted_total_discount_fee of this OrderExpanded.


        :param adjusted_total_discount_fee: The adjusted_total_discount_fee of this OrderExpanded.  # noqa: E501
        :type: float
        """

        self._adjusted_total_discount_fee = adjusted_total_discount_fee

    @property
    def shipping_price(self):
        """Gets the shipping_price of this OrderExpanded.  # noqa: E501


        :return: The shipping_price of this OrderExpanded.  # noqa: E501
        :rtype: float
        """
        return self._shipping_price

    @shipping_price.setter
    def shipping_price(self, shipping_price):
        """Sets the shipping_price of this OrderExpanded.


        :param shipping_price: The shipping_price of this OrderExpanded.  # noqa: E501
        :type: float
        """

        self._shipping_price = shipping_price

    @property
    def adjusted_shipping_price(self):
        """Gets the adjusted_shipping_price of this OrderExpanded.  # noqa: E501


        :return: The adjusted_shipping_price of this OrderExpanded.  # noqa: E501
        :rtype: float
        """
        return self._adjusted_shipping_price

    @adjusted_shipping_price.setter
    def adjusted_shipping_price(self, adjusted_shipping_price):
        """Sets the adjusted_shipping_price of this OrderExpanded.


        :param adjusted_shipping_price: The adjusted_shipping_price of this OrderExpanded.  # noqa: E501
        :type: float
        """

        self._adjusted_shipping_price = adjusted_shipping_price

    @property
    def shipping_tracking_info_list(self):
        """Gets the shipping_tracking_info_list of this OrderExpanded.  # noqa: E501


        :return: The shipping_tracking_info_list of this OrderExpanded.  # noqa: E501
        :rtype: list[ShippingTrackingInfo]
        """
        return self._shipping_tracking_info_list

    @shipping_tracking_info_list.setter
    def shipping_tracking_info_list(self, shipping_tracking_info_list):
        """Sets the shipping_tracking_info_list of this OrderExpanded.


        :param shipping_tracking_info_list: The shipping_tracking_info_list of this OrderExpanded.  # noqa: E501
        :type: list[ShippingTrackingInfo]
        """

        self._shipping_tracking_info_list = shipping_tracking_info_list

    @property
    def shipping_method_code(self):
        """Gets the shipping_method_code of this OrderExpanded.  # noqa: E501


        :return: The shipping_method_code of this OrderExpanded.  # noqa: E501
        :rtype: str
        """
        return self._shipping_method_code

    @shipping_method_code.setter
    def shipping_method_code(self, shipping_method_code):
        """Sets the shipping_method_code of this OrderExpanded.


        :param shipping_method_code: The shipping_method_code of this OrderExpanded.  # noqa: E501
        :type: str
        """

        self._shipping_method_code = shipping_method_code

    @property
    def shipping_region_code(self):
        """Gets the shipping_region_code of this OrderExpanded.  # noqa: E501


        :return: The shipping_region_code of this OrderExpanded.  # noqa: E501
        :rtype: str
        """
        return self._shipping_region_code

    @shipping_region_code.setter
    def shipping_region_code(self, shipping_region_code):
        """Sets the shipping_region_code of this OrderExpanded.


        :param shipping_region_code: The shipping_region_code of this OrderExpanded.  # noqa: E501
        :type: str
        """

        self._shipping_region_code = shipping_region_code

    @property
    def tracking_required(self):
        """Gets the tracking_required of this OrderExpanded.  # noqa: E501


        :return: The tracking_required of this OrderExpanded.  # noqa: E501
        :rtype: bool
        """
        return self._tracking_required

    @tracking_required.setter
    def tracking_required(self, tracking_required):
        """Sets the tracking_required of this OrderExpanded.


        :param tracking_required: The tracking_required of this OrderExpanded.  # noqa: E501
        :type: bool
        """

        self._tracking_required = tracking_required

    @property
    def refunds(self):
        """Gets the refunds of this OrderExpanded.  # noqa: E501


        :return: The refunds of this OrderExpanded.  # noqa: E501
        :rtype: list[OrderRefund]
        """
        return self._refunds

    @refunds.setter
    def refunds(self, refunds):
        """Sets the refunds of this OrderExpanded.


        :param refunds: The refunds of this OrderExpanded.  # noqa: E501
        :type: list[OrderRefund]
        """

        self._refunds = refunds

    @property
    def supplier_invoice_number(self):
        """Gets the supplier_invoice_number of this OrderExpanded.  # noqa: E501


        :return: The supplier_invoice_number of this OrderExpanded.  # noqa: E501
        :rtype: str
        """
        return self._supplier_invoice_number

    @supplier_invoice_number.setter
    def supplier_invoice_number(self, supplier_invoice_number):
        """Sets the supplier_invoice_number of this OrderExpanded.


        :param supplier_invoice_number: The supplier_invoice_number of this OrderExpanded.  # noqa: E501
        :type: str
        """

        self._supplier_invoice_number = supplier_invoice_number

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
        if issubclass(OrderExpanded, dict):
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
        if not isinstance(other, OrderExpanded):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other