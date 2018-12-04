"""SupportService CLI

A CLI interface used for provisioning, deploying, and updating 
SupportService. 
"""
import os
import subprocess
import sys
import ldclient 
import logging 

import click
import click_log

from cli.generators import ConfigGenerator
from cli.ld import LaunchDarklyApi
from cli.aws import AwsApi

# set up logging 
logger = logging.getLogger(__name__)
click_log.basic_config(logger)

# key for production environment
ldclient.set_sdk_key(os.environ.get("LD_PROD_KEY"))
client = ldclient.get()

@click.group()
@click_log.simple_verbosity_option(logger)
def cli():
    pass

@click.command()
def deploy_relay():
    """Deploy LD Relay to LightSail."""
    l = LaunchDarklyApi(os.environ.get('LD_API_KEY'), 'ldsolutions.tk')
    envs = l.getEnvironments('support-service')
    c = ConfigGenerator()

    c.generate_relay_config(envs)

    subprocess.run(
        ["./scripts/deploy_relay.sh"]
    )

@click.command()
@click_log.simple_verbosity_option(logger)
def deploy():
    """Deploy SupportService to LightSail.
    
    Uses a feature flag to disable automatically deploying specific 
    environments. It can be found in the production environment of
    the support-service project. 
    """
    l = LaunchDarklyApi(os.environ.get('LD_API_KEY'), 'ldsolutions.tk')
    a = AwsApi(keyPairName='SupportService')
    c = ConfigGenerator()

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
            a.upsert_instance(hostname)

            # upset Route 53 record for instance
            a.upsertDnsRecord(hostname)

            # generate docker-compose file 
            c.generate_prod_config(env)
            c.generate_nginx_config(env)

            # run reploy script
            subprocess.run(["./scripts/deploy.sh", "{0}".format(hostname)], check=True)
        else:
            click.echo("Not Auto Deploying, auto-deploy-env flag is off for {0}".format(hostname))

cli.add_command(deploy_relay)
cli.add_command(deploy)

if __name__ == '__main__':
    cli()
