# coding: utf-8

"""
    Kubeflow Pipelines API

    This file contains REST API specification for Kubeflow Pipelines. The file is autogenerated from the swagger definition.

    Contact: kubeflow-pipelines@google.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import kfp_tekton_server_api
from kfp_tekton_server_api.models.v1_pipeline import V1Pipeline  # noqa: E501
from kfp_tekton_server_api.rest import ApiException

class TestV1Pipeline(unittest.TestCase):
    """V1Pipeline unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test V1Pipeline
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = kfp_tekton_server_api.models.v1_pipeline.V1Pipeline()  # noqa: E501
        if include_optional :
            return V1Pipeline(
                id = '0', 
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                name = '0', 
                description = '0', 
                parameters = [
                    kfp_tekton_server_api.models.v1_parameter.v1Parameter(
                        name = '0', 
                        value = '0', )
                    ], 
                url = kfp_tekton_server_api.models.v1_url.v1Url(
                    pipeline_url = '0', ), 
                error = '0', 
                default_version = kfp_tekton_server_api.models.v1_pipeline_version.v1PipelineVersion(
                    id = '0', 
                    name = '0', 
                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    parameters = [
                        kfp_tekton_server_api.models.v1_parameter.v1Parameter(
                            name = '0', 
                            value = '0', )
                        ], 
                    code_source_url = '0', 
                    package_url = kfp_tekton_server_api.models.v1_url.v1Url(
                        pipeline_url = '0', ), 
                    resource_references = [
                        kfp_tekton_server_api.models.v1_resource_reference.v1ResourceReference(
                            key = kfp_tekton_server_api.models.v1_resource_key.v1ResourceKey(
                                type = 'UNKNOWN_RESOURCE_TYPE', 
                                id = '0', ), 
                            name = '0', 
                            relationship = 'UNKNOWN_RELATIONSHIP', )
                        ], 
                    description = '0', ), 
                resource_references = [
                    kfp_tekton_server_api.models.v1_resource_reference.v1ResourceReference(
                        key = kfp_tekton_server_api.models.v1_resource_key.v1ResourceKey(
                            type = 'UNKNOWN_RESOURCE_TYPE', 
                            id = '0', ), 
                        name = '0', 
                        relationship = 'UNKNOWN_RELATIONSHIP', )
                    ]
            )
        else :
            return V1Pipeline(
        )

    def testV1Pipeline(self):
        """Test V1Pipeline"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
