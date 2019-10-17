"""Generator Module.

Generates templates using jinja.
"""
import os
import uuid
from jinja2 import Environment, PackageLoader


class ConfigGenerator():
    """Abstract configuration generator using Jinja"""

    def __init__(self):
        self.env = Environment(
            loader=PackageLoader('app.cli', 'templates')
        )

    def generate_prod_config(self, environments):
        """Generate production docker-compose."""
        template = self.env.get_template('docker-compose.prod.jinja')

        with open('docker-compose.prod.yml', 'w+') as docker_compose_file:
            t = template.render(
                envs=environments,
                circle_sha1=os.environ.get('CIRCLE_SHA1') or 'latest',
                DD_API_KEY=os.environ.get('DD_API_KEY')  # from circle
            )
            docker_compose_file.write(t)

    def generate_nginx_config(self, domain, environments):
        """Generate Nginx Config."""
        template = self.env.get_template('nginx.conf.jinja')

        with open('nginx.conf', 'w+') as nginx_file:
            t = template.render(
                domain=domain,
                envs=environments
            )
            nginx_file.write(t)
