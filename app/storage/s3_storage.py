from io import BytesIO
import os
from pathlib import Path
from typing import BinaryIO, Union

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from .interface import StorageInterface


class S3StorageError(Exception):
    """Base exception for S3 storage errors"""
    pass


class S3Storage(StorageInterface):
    def __init__(self, bucket_name: str = None, aws_access_key_id: str = None, 
                 aws_secret_access_key: str = None, region_name: str = None):
        """
        Initialize S3 storage with either environment variables or direct configuration.
        
        Args:
            bucket_name (str, optional): S3 bucket name. Defaults to None (uses env var).
            aws_access_key_id (str, optional): AWS access key. Defaults to None (uses env var).
            aws_secret_access_key (str, optional): AWS secret key. Defaults to None (uses env var).
            region_name (str, optional): AWS region. Defaults to None (uses env var).
        """
        load_dotenv()  # Load environment variables from .env file
        
        self.bucket_name = bucket_name or os.getenv('AWS_S3_BUCKET')
        aws_access_key_id = aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
        region_name = region_name or os.getenv('AWS_REGION', 'us-east-1')
        
        if not all([self.bucket_name, aws_access_key_id, aws_secret_access_key]):
            raise ValueError("Missing required S3 configuration. Provide either through constructor or environment variables.")
        
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
    
    def get(self, path: Union[str, Path]) -> BinaryIO:
        """
        Get a file from S3 storage.
        
        Args:
            path (Union[str, Path]): Path to the file in S3
            
        Returns:
            BinaryIO: A file-like object containing the file data
            
        Raises:
            FileNotFoundError: If the file doesn't exist in S3
            S3StorageError: If there's an error accessing S3
        """
        path_str = str(path)
        file_obj = BytesIO()
        
        try:
            self.s3_client.download_fileobj(
                self.bucket_name,
                path_str,
                file_obj
            )
            file_obj.seek(0)  # Reset file pointer to beginning
            return file_obj
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code')
            if error_code == '404' or error_code == 'NoSuchKey':
                raise FileNotFoundError(f"File {path_str} not found in S3 bucket {self.bucket_name}")
            raise S3StorageError(f"Error accessing S3: {str(e)}")
        except Exception as e:
            raise S3StorageError(f"Unexpected error accessing S3: {str(e)}")