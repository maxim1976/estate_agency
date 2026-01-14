"""
Custom storage backends for AWS S3

This module provides custom storage backends for media files.
Uses the modern storages.backends.s3.S3Storage (not deprecated S3Boto3Storage).
ACLs are NOT used - bucket-level permissions should be configured instead.
"""
from storages.backends.s3 import S3Storage


class MediaStorage(S3Storage):
    """
    Storage backend for media files (user uploads)
    Files will be stored in the 'media/' prefix in S3
    
    Note: No ACL is set here. Use IAM policies and bucket permissions
    for access control instead of object-level ACLs.
    """
    location = 'media'
    file_overwrite = False
    # Do NOT set default_acl - S3 buckets block ACLs by default now
