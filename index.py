from redis import Redis
import boto3
import json
import uuid
import datetime
import os
import botocore
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()
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
        region_name=os.environ.get('REGION')
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


if os.environ.get('REDIS_SECRET_NAME'):
    redis_password = get_secret(os.environ.get('REDIS_SECRET_NAME'))
else:
    redis_password = os.environ.get('REDIS_PASSWORD')


def lambda_handler(event, context):

    r = Redis(
        host=os.environ.get('REDIS_HOST'),
        port=os.environ.get('REDIS_PORT'),
        db=os.environ.get('REDIS_DB'),
        username=os.environ.get('REDIS_USERNAME'),
        password=redis_password)

    id = str(uuid.uuid4())

    message_body = {
        'class': 'ActiveJob::QueueAdapters::ResqueAdapter::JobWrapper',
        'args': [
            {
                'job_class': event,
                'job_id': id,
                'queue_name': os.environ.get('SCHEDULED_QUEUE'),
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

    r.rpush(os.environ.get('SCHEDULED_QUEUE'), json.dumps(message_body))


# if __name__ == "__main__":
#     event = "Scheduled::QueueMessageLockJob"
#     lambda_handler(event, None)
