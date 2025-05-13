import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def create_bucket(bucket_name, region):

    try:
        s3_client = boto3.client('s3', region_name=region)
    
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )

        return True
    except ClientError as e:
        return False

def delete_bucket(bucket_name):
    try:
        s3_client = boto3.client('s3')
        s3_client.delete_bucket(Bucket=bucket_name)

        return True
    except ClientError as e:
        return False

def check_if_bucket_exists(bucket_name):
    try:
        s3_client = boto3.client('s3')
        s3_client.head_bucket(Bucket=bucket_name)

        return True
    except ClientError as e:
        return False

def upload_data_to_s3(bucket_name, object_name, data):
    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=data)

        return True
    except Exception as e:
        return False

def upload_file_to_s3(bucket_name, object_name, file_path):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)

        return True
    except Exception as e:
        return False

def download_file_from_s3(bucket_name, object_name, local_file_path):
    s3_client = boto3.client('s3')
    try:
        s3_client.download_file(bucket_name, object_name, local_file_path)

        return True
    except Exception as e:
        return False
    
def download_content_from_s3(bucket_name, object_name):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
        content = response['Body']

        return content
    except Exception as e:
        raise e

def generate_presigned_url(bucket_name, object_key, expiration=24):
    s3_client = boto3.client('s3')
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration
        )
        
        return url
    except Exception as e:
        raise e