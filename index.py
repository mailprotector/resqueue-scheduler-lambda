from redis import Redis
import boto3
import json
import uuid
import datetime
import os
import botocore
from botocore.exceptions import ClientError
from aws_lambda_powertools.utilities import parameters

session = boto3.session.Session()

if os.environ.get('REDIS_SECRET_NAME'):
    redis_password = parameters.get_secret(
        os.environ.get('REDIS_SECRET_NAME'), max_age=os.environ.get('SECRET_CACHE_AGE', default=300))
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
        'class': os.environ.get('SCHEDULED_JOB_CLASS'),
        'args': [
            {
                'job_class': event,
                'job_id': id,
                'queue_name': os.environ.get('SCHEDULED_QUEUE', default='scheduled'),
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

    r.rpush(
        f"{os.environ.get('SCHEDULED_QUEUE_PREFIX')}:{os.environ.get('SCHEDULED_QUEUE')}", json.dumps(message_body))

# if __name__ == "__main__":
#     event = "Scheduled::QueueMessageLockJob"
#     lambda_handler(event, None)
