# lambda_handler.py

import os
import json
from .lambda_executor import LambdaExecutor
from .s3_operations import S3Operations
from .dynamo_operations import DynamoOperations
from .sns_operations import SnsOperations


table_name = os.environ['TABLE_NAME']
done_topic_arn = os.environ['TOPIC_ARN']

executor = LambdaExecutor(
    s3_operations=S3Operations(),
    dynamo_operations=DynamoOperations(),
    sns_operations=SnsOperations(),
    table_name=table_name,
    done_topic_arn=done_topic_arn,
)

def handler(sns_event, context):
    print("Event : " + str(sns_event))
    print("Context : " + str(context))
    for record in sns_event['Records']:
        message = json.loads(record['Sns']['Message'])
        print("Start Message : " + str(message))
        executor.execute(message)
        print("Done Message : " + str(message))
    print("Done Event : " + str(sns_event))
