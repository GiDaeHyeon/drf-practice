# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developers/getting-started/python/

import os
import json

import boto3
from botocore.exceptions import ClientError


def get_secret() -> dict:
    """
    AWS Secret Manager에서 Secret을 가져와 딕셔너리로 리턴합니다.
    로컬에서 개발을 진행할 때에는 AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ID가 환경변수로 설정되어있어야 합니다.

    :return:
    secret_key_values (dict) AWS Secret Manager에 등록된 secrets
    """
    secret_name = os.environ.get('DRF_PRACTICE_SECRET_NAME')
    region_name = os.environ.get('AWS_REGION', None)

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', None),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ID', None)
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
