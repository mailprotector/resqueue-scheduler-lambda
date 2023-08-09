# resque-scheduler-lambda
A lambda that drops a scheduled job into a resque-managed redis queue

### Environment Variables
| variable name          | description                                                |  type  |  default  | required |
| ---------------------- | ---------------------------------------------------------- | :----: | :-------: | :------: |
| REDIS_USERNAME         | username of the redis instance                             | string |    no     |   yes    |
| REDIS_PASSWORD         | password of the redis instance (if running locally)        | string |    no     |    no    |
| REDIS_SECRET_NAME      | password of the redis instance (pull from secrets manager) | string |    no     |   yes    |
| SECRET_CACHE_AGE       | cache age in seconds of the secrets manager query          | string |    300    |    no    |
| REDIS_HOST             | hostname of the redis instance                             | string |    no     |   yes    |
| REDIS_PORT             | port of the redis instance                                 | string |    no     |   yes    |
| REDIS_DB               | db of the redis instance                                   | string |    no     |   yes    |
| SCHEDULED_QUEUE        | name of the queue                                          | string | scheduled |    no    |
| SCHEDULED_JOB_CLASS    | name of the job class                                      | string |    no     |   yes    |
| SCHEDULED_QUEUE_PREFIX | prefix of the queue name                                   | string |    no     |    no    |