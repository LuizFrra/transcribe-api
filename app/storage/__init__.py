"""
Storage package for handling file storage operations.
"""
from .interface import StorageInterface
from .s3_storage import S3Storage, S3StorageError

__all__ = ['StorageInterface', 'S3Storage', 'S3StorageError']