import os
from typing import Literal
from ftplib import FTP
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import boto3

def upload_file(destination: Literal["s3", "gdrive", "ftp"], file_path: str, **kwargs) -> str:
    try:
        if not os.path.exists(file_path):
            return "File does not exist"

        if destination == "s3":
            s3 = boto3.client("s3")
            s3.upload_file(file_path, kwargs["bucket"], kwargs["object_name"])
            return "Uploaded to S3"

        elif destination == "gdrive":
            creds = Credentials.from_service_account_file(kwargs["service_account_file"])
            drive_service = build("drive", "v3", credentials=creds)
            file_metadata = {"name": os.path.basename(file_path)}
            media = MediaFileUpload(file_path, resumable=True)
            drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
            return "Uploaded to Google Drive"

        elif destination == "ftp":
            ftp = FTP(kwargs["host"])
            ftp.login(kwargs["user"], kwargs["passwd"])
            with open(file_path, "rb") as f:
                ftp.storbinary(f"STOR {os.path.basename(file_path)}", f)
            ftp.quit()
            return "Uploaded to FTP"

        else:
            return "Unsupported destination"
    except Exception as e:
        return f"Error uploading file: {str(e)}"