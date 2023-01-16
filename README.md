# resque-scheduler-lambda
A lambda that drops a Sheduled job into a resque-managed redis queue

### Environment Variables
| variable name   | description                    |  type  | default | required |
| --------------- | ------------------------------ | :----: | :-----: | :------: |
| REDIS_USERNAME  | username of the redis instance | string |   no    |   yes    |
| REDIS_PASSWORD  | password of the redis instance | string |   no    |   yes    |
| REDIS_HOST      | hostname of the redis instance | string |   no    |   yes    |
| REDIS_PORT      | port of the redis instance     | string |   no    |   yes    |
| REDIS_DB        | db of the redis instance       | string |   no    |   yes    |
| SCHEDULED_QUEUE | name of the queue              | string |   no    |   yes    |