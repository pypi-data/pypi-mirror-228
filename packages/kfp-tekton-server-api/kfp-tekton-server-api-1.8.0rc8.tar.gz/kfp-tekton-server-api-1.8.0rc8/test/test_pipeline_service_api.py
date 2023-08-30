# coding: utf-8

"""
    Kubeflow Pipelines API

    This file contains REST API specification for Kubeflow Pipelines. The file is autogenerated from the swagger definition.

    Contact: kubeflow-pipelines@google.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import kfp_tekton_server_api
from kfp_tekton_server_api.api.pipeline_service_api import PipelineServiceApi  # noqa: E501
from kfp_tekton_server_api.rest import ApiException


class TestPipelineServiceApi(unittest.TestCase):
    """PipelineServiceApi unit test stubs"""

    def setUp(self):
        self.api = kfp_tekton_server_api.api.pipeline_service_api.PipelineServiceApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_pipeline_service_create_pipeline(self):
        """Test case for pipeline_service_create_pipeline

        Creates a pipeline.  # noqa: E501
        """
        pass

    def test_pipeline_service_create_pipeline_version(self):
        """Test case for pipeline_service_create_pipeline_version

        Adds a pipeline version to the specified pipeline.  # noqa: E501
        """
        pass

    def test_pipeline_service_delete_pipeline(self):
        """Test case for pipeline_service_delete_pipeline

        Deletes a pipeline and its pipeline versions.  # noqa: E501
        """
        pass

    def test_pipeline_service_delete_pipeline_version(self):
        """Test case for pipeline_service_delete_pipeline_version

        Deletes a pipeline version by pipeline version ID. If the deleted pipeline version is the default pipeline version, the pipeline's default version changes to the pipeline's most recent pipeline version. If there are no remaining pipeline versions, the pipeline will have no default version. Examines the run_service_api.ipynb notebook to learn more about creating a run using a pipeline version (https://github.com/kubeflow/pipelines/blob/master/tools/benchmarks/run_service_api.ipynb).  # noqa: E501
        """
        pass

    def test_pipeline_service_get_pipeline(self):
        """Test case for pipeline_service_get_pipeline

        Finds a specific pipeline by ID.  # noqa: E501
        """
        pass

    def test_pipeline_service_get_pipeline_version(self):
        """Test case for pipeline_service_get_pipeline_version

        Gets a pipeline version by pipeline version ID.  # noqa: E501
        """
        pass

    def test_pipeline_service_get_pipeline_version_template(self):
        """Test case for pipeline_service_get_pipeline_version_template

        Returns a YAML template that contains the specified pipeline version's description, parameters and metadata.  # noqa: E501
        """
        pass

    def test_pipeline_service_get_template(self):
        """Test case for pipeline_service_get_template

        Returns a single YAML template that contains the description, parameters, and metadata associated with the pipeline provided.  # noqa: E501
        """
        pass

    def test_pipeline_service_list_pipeline_versions(self):
        """Test case for pipeline_service_list_pipeline_versions

        Lists all pipeline versions of a given pipeline.  # noqa: E501
        """
        pass

    def test_pipeline_service_list_pipelines(self):
        """Test case for pipeline_service_list_pipelines

        Finds all pipelines.  # noqa: E501
        """
        pass

    def test_pipeline_service_update_pipeline_default_version(self):
        """Test case for pipeline_service_update_pipeline_default_version

        Update the default pipeline version of a specific pipeline.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
