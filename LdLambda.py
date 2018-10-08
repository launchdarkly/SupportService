"""
ld_lambda

Process LaunchDarkly webhooks to trigger a CI build when
a new environment is created. 
"""
import os
import json
import logging

from circleci.api import Api

logger = logging.getLogger()
logger.setLevel(logging.INFO)
circleci = Api(os.environ.get("CIRCLE_TOKEN"))

def trigger_deloy():
    params = {
        'build_parameters[CIRCLE_JOB]': 'deploy'
    }

    circleci.trigger_build(
        username='launchdarkly',
        project='SupportService',
        params=params
    )

def handler(event, context):
    """
    AWS Lambda Handler
    """
    payload = json.loads(event['body'])
    action = payload['accesses'][0]['action']
    
    if  action == 'createEnvironment':
        logger.info("Triggering Deploy for New Environment")
        trigger_deloy()
    else:
        logger.info("Nothing to do for {0}".format(action))

    return {
        'payload': payload
    }

# debug
if __name__ == '__main__':
    trigger_deloy()