"""ld module 

Wrapper for the LaunchDarkly API 

Note that the API SDK is generated using swagger. The entire library is 
stored in the lib/ directory since we do not currently publish this anywhere. 
"""
import launchdarkly_api


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
        
    def formatHostname(self, key):
        """Returns formatted hostname for an environment.

        :param key: environment key 
        """
        return "{0}.{1}".format(key, self.domain)

    def getEnvironments(self, projectKey):
        """Returns List of Environments for a Project.

        Includes name, key, and mobile key, and formatted hostname.

        :param projectKey: Key for project 

        :returns: Collection of Environments
        """
        resp = self.client.get_project(projectKey)
        envs = []

        for env in resp.environments:
            env = dict(
                key=env.key,
                api_key = env.api_key,
                client_id = env.id,
                hostname = self.formatHostname(env.key)
            )
            envs.append(env)
        
        return envs