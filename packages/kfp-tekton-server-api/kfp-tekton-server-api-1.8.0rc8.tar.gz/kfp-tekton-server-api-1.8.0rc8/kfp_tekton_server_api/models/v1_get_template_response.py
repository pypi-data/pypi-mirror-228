# coding: utf-8

"""
    Kubeflow Pipelines API

    This file contains REST API specification for Kubeflow Pipelines. The file is autogenerated from the swagger definition.

    Contact: kubeflow-pipelines@google.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from kfp_tekton_server_api.configuration import Configuration


class V1GetTemplateResponse(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'template': 'str'
    }

    attribute_map = {
        'template': 'template'
    }

    def __init__(self, template=None, local_vars_configuration=None):  # noqa: E501
        """V1GetTemplateResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._template = None
        self.discriminator = None

        if template is not None:
            self.template = template

    @property
    def template(self):
        """Gets the template of this V1GetTemplateResponse.  # noqa: E501

        The template of the pipeline specified in a GetTemplate request, or of a pipeline version specified in a GetPipelinesVersionTemplate request.  # noqa: E501

        :return: The template of this V1GetTemplateResponse.  # noqa: E501
        :rtype: str
        """
        return self._template

    @template.setter
    def template(self, template):
        """Sets the template of this V1GetTemplateResponse.

        The template of the pipeline specified in a GetTemplate request, or of a pipeline version specified in a GetPipelinesVersionTemplate request.  # noqa: E501

        :param template: The template of this V1GetTemplateResponse.  # noqa: E501
        :type template: str
        """

        self._template = template

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, V1GetTemplateResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1GetTemplateResponse):
            return True

        return self.to_dict() != other.to_dict()
