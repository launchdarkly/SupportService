"""Generator Module.

Generates templates using jinja. 
"""
from jinja2 import Environment, PackageLoader


class ConfigGenerator():
    """Abstract configuration generator using Jinja"""

    def __init__(self):
        self.env = Environment(
            loader=PackageLoader('cli', 'templates')
        )
    
    def generate_relay_config(self, template, environments):
        """Generate docker-compose.relay.yml."""
        template = self.env.get_template(template)

        with open('docker-compose.relay.yml', 'w') as docker_compose_file:
            t = template.render(
                envs = environments
            )
            docker_compose_file.write(t)
    
    def generate_prod_config(self, template, environment):
        """Generate production docker-compose."""
        template = self.env.get_template(template)

class RelayConfigGenerator():
    """Generates docker-compose.relay.yml configuration"""

    def __init__(self, environments):
        """Instantiate new RelayConfigGenerator

        :param environments: Dictionary of environments
        """
        self.environments = environments
        self.env = Environment(
            loader=PackageLoader('cli', 'templates')
        )
        self.template = self.env.get_template('docker-compose.jinja')

    def generate_template(self):
        """Generate docker compose file.
        
        Passes in sdk keys, client ID, and proper prefixes for running
        the relay.
        """
        with open('docker-compose.relay.yml', 'w') as docker_compose_file:
            t = self.template.render(
                envs = self.environments
            )
            docker_compose_file.write(t)

        return None


class SecretsGenerator():
    """Generate scripts/secrets.sh file"""
    
    def __init__(self, sdk_key, frontend_key):
        """Instantiate new SecretsGenerator

        :param sdk_key: LaunchDarkly SDK key 
        :param frontend_key: LaunchDarkly Frontend ID
        """
        self.database_url = "postgresql://supportService:supportService@db/supportService"
        self.sdk_key = sdk_key
        self.frontend_key = frontend_key
        self.env = Environment(
            loader=PackageLoader('cli', 'templates')
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