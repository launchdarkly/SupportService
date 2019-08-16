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
                envs = environments,
                circle_sha1 = os.environ.get('CIRCLE_SHA1') or 'latest',
                AWS_QUICKSIGHT_ACCESS_KEY_ID = os.environ.get('AWS_QUICKSIGHT_ACCESS_KEY_ID'), # from circle
                AWS_QUICKSIGHT_SECRET_ACCESS_KEY_ID = os.environ.get('AWS_QUICKSIGHT_SECRET_ACCESS_KEY_ID'), # from circle
                AWS_ACCOUNT_ID = os.environ.get('AWS_ACCOUNT_ID'), # from circle
                AWS_QUICKSIGHT_DASHBOARD_ID = os.environ.get('AWS_QUICKSIGHT_DASHBOARD_ID') # from circle
            )
            docker_compose_file.write(t)

    def generate_nginx_config(self, domain, environments):
        """Generate Nginx Config."""
        template = self.env.get_template('nginx.conf.jinja')

        with open('nginx.conf', 'w+') as nginx_file:
            t = template.render(
                domain = domain,
                envs = environments
            )
            nginx_file.write(t)
