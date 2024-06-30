import boto3
import csv
import os
import logging
import json

s3 = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        if key.startswith('uploaded/'):
            response = s3.get_object(Bucket=bucket, Key=key)
            lines = response['Body'].read().decode('utf-8').splitlines()
            reader = csv.DictReader(lines)
            
            for row in reader:
                logger.info(json.dumps(row))

            parsed_key = key.replace('uploaded/', 'parsed/')
            s3.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': key}, Key=parsed_key)

            s3.delete_object(Bucket=bucket, Key=key)
