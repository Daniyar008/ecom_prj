"""
Custom storage backend for Supabase Storage
Uses django-storages S3Boto3Storage with Supabase S3-compatible API
"""

from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class SupabaseMediaStorage(S3Boto3Storage):
    """
    Custom storage class for Supabase Storage (S3-compatible)
    """

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = "media"  # Folder inside bucket
    file_overwrite = False
    default_acl = "public-read"
    querystring_auth = False  # Don't add auth tokens to URLs (public access)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override for Supabase
        self.endpoint_url = settings.AWS_S3_ENDPOINT_URL
        self.region_name = getattr(settings, "AWS_S3_REGION_NAME", None)
        self.custom_domain = getattr(settings, "AWS_S3_CUSTOM_DOMAIN", None)
