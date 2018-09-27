"""
Utility Functions
"""
import socket
import logging

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