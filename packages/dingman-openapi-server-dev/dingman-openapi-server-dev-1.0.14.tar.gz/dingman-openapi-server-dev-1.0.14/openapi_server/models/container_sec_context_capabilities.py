# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class ContainerSecContextCapabilities(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, add=None, drop=None):  # noqa: E501
        """ContainerSecContextCapabilities - a model defined in OpenAPI

        :param add: The add of this ContainerSecContextCapabilities.  # noqa: E501
        :type add: List[str]
        :param drop: The drop of this ContainerSecContextCapabilities.  # noqa: E501
        :type drop: List[str]
        """
        self.openapi_types = {
            'add': List[str],
            'drop': List[str]
        }

        self.attribute_map = {
            'add': 'add',
            'drop': 'drop'
        }

        self._add = add
        self._drop = drop

    @classmethod
    def from_dict(cls, dikt) -> 'ContainerSecContextCapabilities':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ContainerSecContext_capabilities of this ContainerSecContextCapabilities.  # noqa: E501
        :rtype: ContainerSecContextCapabilities
        """
        return util.deserialize_model(dikt, cls)

    @property
    def add(self):
        """Gets the add of this ContainerSecContextCapabilities.

        Added capabilities.  # noqa: E501

        :return: The add of this ContainerSecContextCapabilities.
        :rtype: List[str]
        """
        return self._add

    @add.setter
    def add(self, add):
        """Sets the add of this ContainerSecContextCapabilities.

        Added capabilities.  # noqa: E501

        :param add: The add of this ContainerSecContextCapabilities.
        :type add: List[str]
        """

        self._add = add

    @property
    def drop(self):
        """Gets the drop of this ContainerSecContextCapabilities.

        Removed capabilities.  # noqa: E501

        :return: The drop of this ContainerSecContextCapabilities.
        :rtype: List[str]
        """
        return self._drop

    @drop.setter
    def drop(self, drop):
        """Sets the drop of this ContainerSecContextCapabilities.

        Removed capabilities.  # noqa: E501

        :param drop: The drop of this ContainerSecContextCapabilities.
        :type drop: List[str]
        """

        self._drop = drop
