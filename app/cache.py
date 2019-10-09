import ldclient
from flask_caching import Cache

from app.util import getLdMachineUser

cache = Cache()

# Operational Feature Flags
CACHE_TIMEOUT = lambda : ldclient.get().variation('cache-timeout', getLdMachineUser(), 50)

def CachingDisabled():
    return ldclient.get().variation('disable-caching', getLdMachineUser(), True)
