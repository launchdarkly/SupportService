"""
ld_lambda

Process LaunchDarkly webhooks to trigger a CI build when
a new environment is created. 
"""
import os
import json
import logging
import ldclient 

from circleci.api import Api

logger = logging.getLogger()
logger.setLevel(logging.INFO)
circleci = Api(os.environ.get("CIRCLE_TOKEN"))
# key for production environment
ldclient.set_sdk_key(os.environ.get("LD_CLIENT_KEY"))
client = ldclient.get()

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
    logger.info(payload)
    action = payload['accesses'][0]['action']
    resource = payload['accesses'][0]['resource']
    
    ctx = {
        "key": "lambda"
    }

    # this flag is set in the production environment
    if client.variation("auto-deploy-lambda", ctx, False):
        if 'support-service' in resource: 
            if  action == 'createEnvironment':
                logger.info("Triggering Deploy for New Environment")
                trigger_deloy()
            else:
                logger.info("Nothing to do for {0}".format(action))
        else:
            logger.info("Nothing to do for {0}".format(resource))
    else:
        logger.info("Not Auto Deploying, auto-deploy-lambda flag is off.")

    return {
        'payload': payload
    }