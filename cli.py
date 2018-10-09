"""SupportService CLI

A CLI interface used for provisioning, deploying, and updating 
SupportService. 
"""
import logging
import os
import subprocess
import sys

import click

from cli.generators import RelayConfigGenerator, SecretsGenerator
from cli.ld import LaunchDarklyApi
from cli.aws import AwsApi

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
    """Deploy SupportService to LightSail."""
    l = LaunchDarklyApi(os.environ.get('LD_API_KEY'), 'ldsolutions.tk')
    a = AwsApi(keyPairName='SupportService')

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

cli.add_command(deploy_relay)
cli.add_command(deploy)

if __name__ == '__main__':
    cli()
