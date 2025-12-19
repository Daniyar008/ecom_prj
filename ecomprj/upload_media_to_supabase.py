#!/usr/bin/env python
"""
Script to upload existing local media files to Supabase Storage
Run this after configuring Supabase Storage settings
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecomprj.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from pathlib import Path
import boto3
from botocore.exceptions import ClientError


def upload_to_supabase():
    """Upload all local media files to Supabase Storage"""

    if not settings.USE_SUPABASE_STORAGE:
        print("❌ Supabase Storage is not enabled. Set USE_SUPABASE_STORAGE=True")
        return

    if not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY:
        print("❌ Supabase Storage credentials are not configured")
        print("   Set SUPABASE_STORAGE_ACCESS_KEY and SUPABASE_STORAGE_SECRET_KEY")
        return

    # Create S3 client for Supabase
    s3_client = boto3.client(
        "s3",
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    bucket = settings.AWS_STORAGE_BUCKET_NAME
    media_root = Path(settings.MEDIA_ROOT)

    if not media_root.exists():
        print(f"❌ Media root does not exist: {media_root}")
        return

    print(f"📁 Uploading from: {media_root}")
    print(f"📤 Uploading to bucket: {bucket}")
    print(f"🔗 Endpoint: {settings.AWS_S3_ENDPOINT_URL}")
    print("-" * 50)

    uploaded = 0
    failed = 0
    skipped = 0

    # Walk through all files in media folder
    for root, dirs, files in os.walk(media_root):
        for filename in files:
            local_path = Path(root) / filename

            # Skip hidden files and system files
            if filename.startswith(".") or filename.endswith(".tmp"):
                skipped += 1
                continue

            # Calculate relative path for S3 key
            relative_path = local_path.relative_to(media_root)
            s3_key = f"media/{str(relative_path).replace(os.sep, '/')}"

            # Determine content type
            content_type = get_content_type(filename)

            try:
                # Check if file already exists
                try:
                    s3_client.head_object(Bucket=bucket, Key=s3_key)
                    print(f"⏭️  Already exists: {s3_key}")
                    skipped += 1
                    continue
                except ClientError as e:
                    if e.response["Error"]["Code"] != "404":
                        raise

                # Upload file
                with open(local_path, "rb") as f:
                    s3_client.put_object(
                        Bucket=bucket,
                        Key=s3_key,
                        Body=f,
                        ContentType=content_type,
                        ACL="public-read",
                    )
                print(f"✅ Uploaded: {s3_key}")
                uploaded += 1

            except Exception as e:
                print(f"❌ Failed: {s3_key} - {str(e)}")
                failed += 1

    print("-" * 50)
    print(f"📊 Summary:")
    print(f"   ✅ Uploaded: {uploaded}")
    print(f"   ⏭️  Skipped: {skipped}")
    print(f"   ❌ Failed: {failed}")


def get_content_type(filename):
    """Get content type based on file extension"""
    ext = filename.lower().split(".")[-1] if "." in filename else ""

    content_types = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "jfif": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp",
        "svg": "image/svg+xml",
        "ico": "image/x-icon",
        "pdf": "application/pdf",
        "mp4": "video/mp4",
        "mp3": "audio/mpeg",
        "json": "application/json",
        "txt": "text/plain",
    }

    return content_types.get(ext, "application/octet-stream")


if __name__ == "__main__":
    print("=" * 50)
    print("Supabase Storage Upload Script")
    print("=" * 50)
    upload_to_supabase()
