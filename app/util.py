"""
Utility Functions
"""
import socket
import logging
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from app.util import check_fetch_aws_embedUrl

def getLdMachineUser(request=None):
    """
    Representation of a non human "user" for use with LaunchDarkly
    """
    if request:
        request_ip = request.remote_addr
    else:
        request_ip = None

    user = {
        "key": socket.gethostname(),
        "ip": request_ip,
        "custom": {
            "type": "machine"
        }
    }

    logging.debug(user)

    return user

def run_fetch_aws_embed_url_function():
    # check_fetch_aws_embedUrl() # trigger the fetch for URL
    print("running job now")

scheduler = BackgroundScheduler()
# scheduler.add_job(func=run_fetch_aws_embed_url_function, trigger="interval", seconds=5) # Runs every 10 hours
# scheduler.start()

"this lives in feature only"
