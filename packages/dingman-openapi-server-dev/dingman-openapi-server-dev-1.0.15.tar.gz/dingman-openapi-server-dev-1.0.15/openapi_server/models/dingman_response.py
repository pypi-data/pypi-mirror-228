# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class DingmanResponse(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, status=None, message=None):  # noqa: E501
        """DingmanResponse - a model defined in OpenAPI

        :param status: The status of this DingmanResponse.  # noqa: E501
        :type status: str
        :param message: The message of this DingmanResponse.  # noqa: E501
        :type message: str
        """
        self.openapi_types = {
            'status': str,
            'message': str
        }

        self.attribute_map = {
            'status': 'status',
            'message': 'message'
        }

        self._status = status
        self._message = message

    @classmethod
    def from_dict(cls, dikt) -> 'DingmanResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The DingmanResponse of this DingmanResponse.  # noqa: E501
        :rtype: DingmanResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def status(self):
        """Gets the status of this DingmanResponse.

        status of the operation  # noqa: E501

        :return: The status of this DingmanResponse.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this DingmanResponse.

        status of the operation  # noqa: E501

        :param status: The status of this DingmanResponse.
        :type status: str
        """

        self._status = status

    @property
    def message(self):
        """Gets the message of this DingmanResponse.

        message returned from the server  # noqa: E501

        :return: The message of this DingmanResponse.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this DingmanResponse.

        message returned from the server  # noqa: E501

        :param message: The message of this DingmanResponse.
        :type message: str
        """

        self._message = message
