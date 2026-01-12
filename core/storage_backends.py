"""
Custom storage backends for AWS S3
"""
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """
    Storage backend for media files (user uploads)
    Files will be stored in the 'media/' prefix in S3
    """
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
