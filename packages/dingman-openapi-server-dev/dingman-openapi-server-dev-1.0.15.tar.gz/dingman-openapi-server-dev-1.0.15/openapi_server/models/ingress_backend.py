# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.ingress_backend_service import IngressBackendService
from openapi_server import util

from openapi_server.models.ingress_backend_service import IngressBackendService  # noqa: E501

class IngressBackend(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, service=None):  # noqa: E501
        """IngressBackend - a model defined in OpenAPI

        :param service: The service of this IngressBackend.  # noqa: E501
        :type service: IngressBackendService
        """
        self.openapi_types = {
            'service': IngressBackendService
        }

        self.attribute_map = {
            'service': 'service'
        }

        self._service = service

    @classmethod
    def from_dict(cls, dikt) -> 'IngressBackend':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The IngressBackend of this IngressBackend.  # noqa: E501
        :rtype: IngressBackend
        """
        return util.deserialize_model(dikt, cls)

    @property
    def service(self):
        """Gets the service of this IngressBackend.


        :return: The service of this IngressBackend.
        :rtype: IngressBackendService
        """
        return self._service

    @service.setter
    def service(self, service):
        """Sets the service of this IngressBackend.


        :param service: The service of this IngressBackend.
        :type service: IngressBackendService
        """

        self._service = service
