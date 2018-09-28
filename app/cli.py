import launchdarkly_api


class LaunchDarklyApi():
    """Interface to LaunchDarkly API"""

    def __init__(self, apiKey, domain):
        """Instantiate a new LaunchDarklyApi instance. 

        :param apiKey: API Access Key for LaunchDarkly
        :param domain: domain to use for generating hostnames
        """
        self.apiKey = apiKey
        self.domain = domain

    def getClient(self):
        """Get LaunchDarkly API Client."""
        configuration = launchdarkly_api.Configuration()
        configuration.api_key['Authorization'] = self.apiKey
        api = launchdarkly_api.ProjectsApi(launchdarkly_api.ApiClient(configuration))

        return api

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
        resp = self.getClient().get_project(projectKey)
        envs = {'environments': []}

        for env in resp.environments:
            env = dict(
                key=env.key,
                api_key = env.api_key,
                client_id = env.id,
                hostname = self.formatHostname(env.key)
            )
            envs['environments'].append(env)
        
        return envs