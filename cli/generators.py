"""Generator Module.

Generates templates using jinja. 
"""
import os
from jinja2 import Environment, PackageLoader


class ConfigGenerator():
    """Abstract configuration generator using Jinja"""

    def __init__(self):
        self.env = Environment(
            loader=PackageLoader('cli', 'templates')
        )
    
    def generate_relay_config(self, environments):
        """Generate docker-compose.relay.yml."""
        template = self.env.get_template('docker-compose.relay.jinja')

        with open('docker-compose.relay.yml', 'w') as docker_compose_file:
            t = template.render(
                envs = environments
            )
            docker_compose_file.write(t)
    
    def generate_prod_config(self, environment):
        """Generate production docker-compose."""
        template = self.env.get_template('docker-compose.prod.jinja')

        with open('docker-compose.prod.yml', 'w') as docker_compose_file:
            t = template.render(
                env = environment
            )
            docker_compose_file.write(t)

    def generate_apm_config(self):
        """Generate apm-server.yml file."""
        template = self.env.get_template('apm-server.jinja')

        with open('apm-server.yml', 'w') as apm_server_file:
            t = template.render(
                elk_host = os.environ.get('ELK_HOST'),
                elk_username = os.environ.get('ELK_USERNAME'),
                elk_password = os.environ.get('ELK_PASSWORD')
            )
            apm_server_file.write(t)