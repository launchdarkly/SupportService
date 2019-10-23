from flask import current_app as app
from flask_caching import Cache

from app.util import getLdMachineUser

cache = Cache()
#with app.app_context():
#    CACHE_TIMEOUT = lambda : app.ldclient.variation('cache-timeout', getLdMachineUser(), 50)

#def CachingDisabled(app):
#    return app.ldclient.variation('disable-caching', getLdMachineUser(), True)
