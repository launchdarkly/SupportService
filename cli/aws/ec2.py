"""aws.ec2 module

Wrapper for AWS Boto EC2 Client 
"""
import os
import boto3

class EC2Client():
    """Interface to EC2 Client"""

    def __init__(self, logger=None, accessKey=None, secret=None):
        """Instantiate a new EC2 Client Instance

        :param logger: Instance of Logger
        :param accessKey: AWS Access Key ID
        :param secret: AWS Secret Access Key
        """
        self.logger = logger
        self.accessKey = accessKey
        self.secret = secret
        self.region = os.environ.get('AWS_DEFAULT_REGION')
        self.client = boto3.client('ec2')
    
    def getRelayInstances(self):
        """Return list of relay instances from EC2."""
        response = self.client.describe_instances(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': ['ld-relay*']
                }
            ]
        )
        return response['Reservations'][0]['Instances']
    