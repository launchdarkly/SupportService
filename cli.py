"""SupportService CLI

A CLI interface used for provisioning, deploying, and updating 
SupportService. 
"""
import os
import subprocess
import sys
import ldclient 

import click

from cli.generators import RelayConfigGenerator, SecretsGenerator, ElkConfigGenerator
from cli.ld import LaunchDarklyApi
from cli.aws import AwsApi

# key for production environment
ldclient.set_sdk_key(os.environ.get("LD_PROD_KEY"))
client = ldclient.get()

@click.group()
def cli():
    pass

@click.command()
def deploy_relay():
    """Deploy LD Relay to LightSail."""
    l = LaunchDarklyApi(os.environ.get('LD_API_KEY'), 'ldsolutions.tk')
    envs = l.getEnvironments('support-service')
    r = RelayConfigGenerator(environments = envs)

    r.generate_template()
    subprocess.run(
        ["./scripts/deploy_relay.sh"]
    )

@click.command()
def deploy():
    """Deploy SupportService to LightSail.
    
    Uses a feature flag to disable automatically deploying specific 
    environments. It can be found in the production environment of
    the support-service project. 
    """
    l = LaunchDarklyApi(os.environ.get('LD_API_KEY'), 'ldsolutions.tk')
    a = AwsApi(keyPairName='SupportService')

    envs = l.getEnvironments('support-service')

    for env in envs:

        hostname = env['hostname']

        ctx = {
            "key": "circleci",
            "custom": {
                "hostname": hostname
            }
        }

        if client.variation("auto-deploy-env", ctx, False):
            click.echo("Deploying {0}".format(hostname))
            # create instance if needed
            a.checkProvisionedInstance(hostname)

            # get instance IP address
            ipAddress = a.getInstanceIp(hostname)

            # upset Route 53 record for instance
            a.upsertDnsRecord(ipAddress, hostname)

            # generate secrets
            secrets_generator = SecretsGenerator(env['api_key'], env['client_id'])
            secrets_generator.generate_template()

            # run reploy script
            subprocess.run(["./scripts/deploy.sh", "{0}".format(ipAddress)], check=True)
        else:
            click.echo("Not Auto Deploying, auto-deploy-env flag is off for {0}".format(hostname))

cli.add_command(deploy_relay)
cli.add_command(deploy)

if __name__ == '__main__':
    cli()
