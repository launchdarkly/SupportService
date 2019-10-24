
from flask_caching import Cache

from app.admin_ldclient import admin_ldclient
from app.util import getLdMachineUser

cache = Cache()

CACHE_TIMEOUT = lambda : admin_ldclient.variation('cache-timeout', getLdMachineUser(), 50)

def caching_disabled():
    return admin_ldclient.variation('disable-caching', getLdMachineUser(), True)
