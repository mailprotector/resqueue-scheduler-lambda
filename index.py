from redis import Redis
import boto3
import json
import uuid
import datetime
import os
import botocore
from botocore.exceptions import ClientError
from rq import Queue

redis_host = os.environ.get('REDIS_HOST')
redis_port = os.environ.get('REDIS_PORT')
redis_username = os.environ.get('REDIS_USERNAME')
redis_secret_name = os.environ.get('REDIS_SECRET_NAME')
scheduled_queue = os.environ.get('SCHEDULED_QUEUE')
region_name = os.environ.get('REGION')

if os.environ.get('AWS_PROFILE'):
    session = boto3.Session(
        profile_name=os.environ.get('AWS_PROFILE', 'dev'),
        region_name=region_name
    )
else:
    session = boto3.session.Session()


def get_secret(secret_name):
    """
    Query the secrets manager for the secret values necessary to read from the prod cluster and write to the metrics cluster
    Parameters:
    secret_name (string): secretsmanager name to query
    Returns:
    string - unencrypted secret value
    """

    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise e
    else:
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']


def lambda_handler(event, context):

    r = Redis(
        host='redis_hostname',
        port='redis_port',
        username='redis_username',
        password=get_secret(redis_secret_name))

    id = str(uuid.uuid4())

    message_body = {
        'class': 'ActiveJob::QueueAdapters::ResqueAdapter::JobWrapper',
        'args': [
            {
                'job_class': event,
                'job_id': id,
                'queue_name': scheduled_queue,
                'priority': None,
                'enqueued_at': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                'locale': 'en',
                'timezone': 'UTC',
                'executions': 0,
                'exception_executions': {},
                'arguments': []
            }
        ]
    }


r.push(scheduled_queue, json.dumps(message_body))


if __name__ == "__main__":
    event = {
        "task_name": "test"
    }
    lambda_handler(event, None)
