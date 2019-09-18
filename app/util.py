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

def artifical_delay(duration):
    # Delays are in seconds
    MIN_LOAD_DELAY = 1
    MAX_LOAD_DELAY = 3
    LOAD_DELAY_TRIGGER = 30

    # multi-variate flag is a string, so doing string comparison
    if duration == LOAD_DELAY_TRIGGER:
        time.sleep(random.randint(MIN_LOAD_DELAY,MAX_LOAD_DELAY))

    return
