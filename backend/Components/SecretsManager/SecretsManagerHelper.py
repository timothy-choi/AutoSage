import boto3
from botocore.exceptions import ClientError
import json

secrets_client = boto3.client("secretsmanager")

def store_secret(name: str, secret_value: str, description: str = "") -> bool:
    try:
        secrets_client.create_secret(
            Name=name,
            SecretString=secret_value,
            Description=description
        )
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceExistsException":
            secrets_client.put_secret_value(
                SecretId=name,
                SecretString=secret_value
            )
            return True
        raise

def retrieve_secret(name: str) -> str:
    try:
        response = secrets_client.get_secret_value(SecretId=name)
        return response["SecretString"]
    except ClientError as e:
        raise Exception(f"Failed to retrieve secret '{name}': {e}")

def delete_secret(name: str, force_delete: bool = False) -> bool:
    try:
        secrets_client.delete_secret(
            SecretId=name,
            ForceDeleteWithoutRecovery=force_delete
        )
        return True
    except ClientError as e:
        raise Exception(f"Failed to delete secret '{name}': {e}")
