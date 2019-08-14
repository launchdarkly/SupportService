"""
Utility Functions
"""
import socket
import logging
import random
import time

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

def newServerFunctionality(duration):
    # Delays are in seconds
    min_load_delay = 1
    max_load_delay = 3

    # multi-variate flag is a string, so doing string comparison
    if duration == '30':
        time.sleep(random.randint(min_load_delay,max_load_delay))
    
    return 