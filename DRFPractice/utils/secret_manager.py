# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developers/getting-started/python/

import os
import json
import boto3
from botocore.exceptions import ClientError


def get_secret() -> dict:
    secret_name = os.environ.get('DRF_PRACTICE_SECRET_NAME')
    region_name = os.environ.get('AWS_REGION', None)  # For DEV

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', None),  # For DEV
        aws_secret_access_key=os.environ.get('AWS_SECRET_ID', None)  # For DEV
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
        return json.loads(get_secret_value_response['SecretString'])
