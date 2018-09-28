import os
import sys 

import boto3

import launchdarkly_api
import logging


class LaunchDarklyApi():
    """Interface to LaunchDarkly API"""

    def __init__(self, apiKey, domain):
        """Instantiate a new LaunchDarklyApi instance. 

        :param apiKey: API Access Key for LaunchDarkly
        :param domain: domain to use for generating hostnames
        """
        self.apiKey = apiKey
        self.domain = domain
        self.logger = logging.getLogger()

        # get new LD client 
        configuration = launchdarkly_api.Configuration()
        configuration.api_key['Authorization'] = apiKey
        self.client = launchdarkly_api.ProjectsApi(launchdarkly_api.ApiClient(configuration))
        

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


class LightSailApi():
    """Interface to AWS LightSail API"""
    BUNDLE_ID = "nano_2_0"
    AVAILABILITY_ZONE = "us-west-2a"

    def __init__(self, accessKey=None, secret=None, keyPairName=None):
        """Instantiate a new LightSailApi instance. 

        :param accessKey: AWS Access Key ID
        :param secret: AWS Secret Access Key
        """
        self.accessKey = accessKey
        self.secret = secret
        self.keyPairName = keyPairName
        self.logger = logging.getLogger()
        self.client = boto3.client('lightsail')

    def getCentosBlueprint(self):
        """Get first CentOS Blueprint."""
        resp = self.client.get_blueprints(
            includeInactive=False
        )
        blueprints = [x['blueprintId'] for x in resp['blueprints'] if x['name'] == 'CentOS']
        return blueprints[0]

    def getUserData(self):
        """Return Init Script for New Instances."""
        with open('scripts/init.sh', 'r') as initScript:
            data = initScript.read()
            return data

    def provisionInstance(self, hostname):
        """Create new Lightsail Instance.

        :param hostname: hostname to use 
        """
        response = self.client.create_instances(
            instanceNames=[
                hostname,
            ],
            availabilityZone = self.AVAILABILITY_ZONE,
            blueprintId = self.getCentosBlueprint(),
            bundleId = self.BUNDLE_ID,
            userData = self.getUserData(),
            keyPairName = self.keyPairName
        )
        self.logger.info('Creating new instance called {0}'.format(hostname))
        return response

    def checkProvisionedInstance(self, hostname):
        """Check to see if an Instance Exists.

        :param hostnames: list of hostnames to check
        """
        try:
            instance = self.client.get_instance(instanceName=hostname)
            self.logger.info("Instance {0} already exists.".format(hostname))
        except self.client.exceptions.NotFoundException:
            self.provisionInstance(hostname)


if __name__ == '__main__':
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    # this will become the entry point to the 
    # flask provision custom command
    l = LaunchDarklyApi(os.environ.get('LD_API_KEY'), 'ldsolutions.tk')
    a = LightSailApi(keyPairName='SupportService')

    envs = l.getEnvironments('support-service')

    for env in envs:
        a.checkProvisionedInstance(env['hostname'])