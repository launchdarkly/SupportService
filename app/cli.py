import logging
import os
import subprocess
import sys
import time

import boto3

import launchdarkly_api

from jinja2 import Environment, PackageLoader

class SecretsGenerator():
    """Generate scripts/secrets.sh file"""
    
    def __init__(self, sdk_key, frontend_key):
        """Instantiate new SecretsGenerator()

        :param sdk_key: LaunchDarkly SDK key 
        :param frontend_key: LaunchDarkly Frontend ID
        """
        self.database_url = "postgresql://supportService:supportService@db/supportService"
        self.sdk_key = sdk_key
        self.frontend_key = frontend_key
        self.env = Environment(
            loader=PackageLoader('app', 'templates')
        )
        self.template = self.env.get_template('secrets.jinja')

    def generate_template(self):
        """Generate a new Secrets File."""
        with open('scripts/secrets.sh', 'w') as secrets_file:
            t = self.template.render(
                database_url=self.database_url, 
                ld_sdk_key=self.sdk_key, 
                ld_frontend_key=self.frontend_key)
            secrets_file.write(t)
        
        return None

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
        self.region = os.environ.get('AWS_DEFAULT_REGION')
        self.hostedZoneId = os.environ.get('AWS_HOSTED_ZONE_ID')
        self.logger = logging.getLogger()
        self.client = boto3.client('lightsail')
        self.dns = boto3.client('route53')

    def upsertDnsRecord(self, instanceIp, hostname):
        """Create or Update DNS Record for Instance.
        
        :param instanceIp: IP address of new instnace.
        :param hostname: hostname to use for new instance.
        """
        response = self.dns.change_resource_record_sets(
            HostedZoneId=self.hostedZoneId,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': hostname,
                            'Type': 'A',
                            'TTL': 300,
                            'ResourceRecords': [
                                {
                                    'Value': instanceIp
                                }
                            ]
                        }
                    }
                ]
            }
        )

        self.logger.debug(response)
        return response

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

    def getInstanceIp(self, instanceName):
        """Return IP address for instance.

        :param instanceName: name of LightSail isntance
        """
        response = self.client.get_instance(instanceName=instanceName)

        while ('publicIpAddress' not in response['instance']) or (len(response['instance']['publicIpAddress']) < 0):
            self.logger.info("IP for {0} not yet assigned, sleeping".format(instanceName))
            time.sleep(1)
            response = self.client.get_instance(instanceName=instanceName)

        return response['instance']['publicIpAddress']

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

def deploy_command():
    """Deploy to LightSail."""
    l = LaunchDarklyApi(os.environ.get('LD_API_KEY'), 'ldsolutions.tk')
    a = LightSailApi(keyPairName='SupportService')

    envs = l.getEnvironments('support-service')

    for env in envs:
        # create instance if needed
        a.checkProvisionedInstance(env['hostname'])

        # get instance IP address
        ipAddress = a.getInstanceIp(env['hostname'])

        # upset Route 53 record for instance
        a.upsertDnsRecord(ipAddress, env['hostname'])

        # generate secrets
        secrets_generator = SecretsGenerator(env['api_key'], env['client_id'])
        secrets_generator.generate_template()

        # run reploy script
        subprocess.run(["./scripts/deploy.sh", "{0}".format(ipAddress)], check=True)

if __name__ == '__main__':
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    deploy_command()
