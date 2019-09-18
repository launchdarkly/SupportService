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

    def __init__(self, apiKey, domain):
        """Instantiate a new LaunchDarklyApi instance.

        :param apiKey: API Access Key for LaunchDarkly
        :param domain: domain to use for generating hostnames
        """
        self.apiKey = apiKey
        self.domain = domain

        # get new LD client
        configuration = launchdarkly_api.Configuration()
        configuration.api_key['Authorization'] = apiKey
        self.client = launchdarkly_api.ProjectsApi(
            launchdarkly_api.ApiClient(configuration))

    def format_hostname(self, key):
        """Returns formatted hostname for an environment.

        :param key: environment key
        """
        return "{0}.{1}".format(key, self.domain)

    def get_environments(self, projectKey):
        """Returns List of Environments for a Project.

        Includes name, key, and mobile key.

        :param projectKey: Key for project

        :returns: Collection of Environments
        """
        resp = self.client.get_project(projectKey)

        return resp

    def get_environment(self, environment_key):
        #logging.info(project.environments)
        for env in project.environments:
            logging.info(env.name)
            if env.name == environment_key:
                return env


    def get_project(self, project_key):
        resp = self.client.get_project(project_key)

        return resp
