import os
import ldclient
from ldclient import Config as LdConfig
from app.ld import LaunchDarklyApi


class AdminClient:
    PROJECT_NAME = os.environ.get("LD_PROJECT_NAME", "support-service")

    def __init__(self):
        self.ld = LaunchDarklyApi(os.environ.get('LD_API_KEY'))
        self.project = self.ld.get_project(AdminClient.PROJECT_NAME)


    def admin_ldclient(self):
        for env in self.project.environments:
            if env.name == 'admin':
                admin_env = env
                break

        ld_config = LdConfig(
            sdk_key = admin_env.api_key,
            connect_timeout = 30,
            read_timeout = 30
        )
        return ldclient.LDClient(config=ld_config)

admin_ldclient = AdminClient().admin_ldclient()
