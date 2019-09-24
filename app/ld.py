"""ld module

Wrapper for the LaunchDarkly API

Note that the API SDK is generated using swagger. The entire library is
stored in the lib/ directory since we do not currently publish this anywhere.
"""
import launchdarkly_api
import logging
import json

class LaunchDarklyApi():
    """Wrapper for the LaunchDarkly API"""

    def __init__(self, apiKey):
        """Instantiate a new LaunchDarklyApi instance.

        :param apiKey: API Access Key for LaunchDarkly
        :param domain: domain to use for generating hostnames
        """
        self.apiKey = apiKey

        # get new LD client
        configuration = launchdarkly_api.Configuration()
        configuration.api_key['Authorization'] = apiKey
        self.client = launchdarkly_api.ProjectsApi(
            launchdarkly_api.ApiClient(configuration))

    def get_project(self, project_key):
        resp = self.client.get_project(project_key)

        return resp
