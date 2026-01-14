# AWS Integration Guide for Django Projects

This guide documents the AWS S3 integration pattern used in this project, designed for smooth implementation in future Django projects.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [AWS Setup](#aws-setup)
- [Django Configuration](#django-configuration)
- [Environment Variables](#environment-variables)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

---

## Overview

This implementation uses **AWS S3** for media file storage in production while maintaining local file storage for development. The configuration includes:

- **Primary Service**: Amazon S3 (Simple Storage Service)
- **Storage Backend**: `django-storages` with boto3
- **Static Files**: Whitenoise (local serving, not S3)
- **Media Files**: S3 in production, local filesystem in development
- **Image Processing**: django-imagekit with S3 support

### Architecture Benefits
- ✅ Scalable media storage
- ✅ Reduced server disk usage
- ✅ CDN-ready (S3 URLs can be fronted with CloudFront)
- ✅ Fallback to local storage when AWS credentials are missing
- ✅ No ACL complexity (uses bucket-level permissions)

---

## Prerequisites

### Required Python Packages

Add to `requirements.txt`:
```txt
boto3==1.34.144
botocore==1.34.144
django-storages==1.14.2
django-imagekit==6.0.0
django-environ==0.12.0
dj-database-url==2.1.0
whitenoise==6.6.0
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### Required AWS Services
1. **AWS Account** with appropriate permissions
2. **IAM User** with programmatic access
3. **S3 Bucket** for media storage

---

## AWS Setup

### 1. Create IAM User

1. Navigate to **IAM Console** → **Users** → **Create User**
2. Username: `django-s3-media-user` (or your project name)
3. Enable **Programmatic access** (Access Key)
4. Attach permissions (next step)

### 2. Set IAM Permissions

Create a custom policy for your S3 bucket:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::YOUR-BUCKET-NAME/*",
                "arn:aws:s3:::YOUR-BUCKET-NAME"
            ]
        }
    ]
}
```

**Important**: Replace `YOUR-BUCKET-NAME` with your actual bucket name.

### 3. Create S3 Bucket

1. Navigate to **S3 Console** → **Create Bucket**
2. **Bucket Name**: Choose a unique name (e.g., `your-project-media-production`)
3. **Region**: Select closest to your users (e.g., `ap-northeast-1` for Asia-Pacific)
4. **Block Public Access**: Keep all enabled (we'll use IAM, not ACLs)
5. **Bucket Versioning**: Optional (recommended for production)
6. **Encryption**: Enable (AES-256 or AWS-KMS)

### 4. Configure Bucket CORS (If Needed)

If you need browser uploads, add CORS policy:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
        "AllowedOrigins": ["https://your-domain.com"],
        "ExposeHeaders": ["ETag"],
        "MaxAgeSeconds": 3000
    }
]
```

### 5. Save AWS Credentials

**Never commit credentials to git!**

Store in:
- Development: `.env` file (gitignored)
- Production: Platform environment variables (Railway, Heroku, etc.)

Example format:
```env
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=ap-northeast-1
```

---

## Django Configuration

### 1. Settings Structure

Organize settings into environment-specific files:
```
config/settings/
├── __init__.py
├── base.py          # Shared settings
├── development.py   # Local development
├── production.py    # Production with S3
└── test.py         # Testing
```

### 2. Base Settings (`base.py`)

```python
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialize environ
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY', default='django-insecure-change-me')

# Basic media/static configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 3. Production Settings (`production.py`)

```python
from .base import *
import dj_database_url

DEBUG = env('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['yourdomain.com'])

# Database
database_url = os.environ.get('DATABASE_URL')
if database_url:
    DATABASES = {
        'default': dj_database_url.config(
            default=database_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default='')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', default='')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='ap-northeast-1')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
AWS_S3_ENDPOINT_URL = f'https://s3.{AWS_S3_REGION_NAME}.amazonaws.com'
AWS_LOCATION = 'media'

# Storage configuration - conditional based on AWS credentials
if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME:
    # Use S3 for media files
    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3.S3Storage',
            'OPTIONS': {
                'access_key': AWS_ACCESS_KEY_ID,
                'secret_key': AWS_SECRET_ACCESS_KEY,
                'bucket_name': AWS_STORAGE_BUCKET_NAME,
                'region_name': AWS_S3_REGION_NAME,
                'endpoint_url': AWS_S3_ENDPOINT_URL,
                'location': AWS_LOCATION,
            },
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        },
    }
    
    # Update MEDIA_URL to use S3
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    
    # ImageKit configuration for S3
    IMAGEKIT_DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'
    IMAGEKIT_CACHEFILE_STORAGE = 'storages.backends.s3.S3Storage'
else:
    # Fallback to local storage
    STORAGES = {
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        },
    }
    IMAGEKIT_DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Security settings
SECURE_SSL_REDIRECT = env('SECURE_SSL_REDIRECT', default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### 4. Development Settings (`development.py`)

```python
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

# Use SQLite for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Use local file storage (no S3)
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

# Disable security features for local development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
```

---

## Environment Variables

### Development (`.env` file)

Create `.env` in project root:
```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-for-development
DJANGO_SETTINGS_MODULE=config.settings.development

# AWS S3 (optional for local dev)
# AWS_ACCESS_KEY_ID=
# AWS_SECRET_ACCESS_KEY=
# AWS_STORAGE_BUCKET_NAME=
# AWS_S3_REGION_NAME=ap-northeast-1

# Database (optional - defaults to SQLite)
# DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
```

### Production (Platform Environment Variables)

Set these in your deployment platform (Railway, Heroku, AWS EB, etc.):

```env
DEBUG=False
SECRET_KEY=strong-random-production-key
DJANGO_SETTINGS_MODULE=config.settings.production

# Required for S3
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCY
AWS_STORAGE_BUCKET_NAME=your-production-bucket
AWS_S3_REGION_NAME=ap-northeast-1

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Security
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
SECURE_SSL_REDIRECT=True
```

### Security Note
- Use strong, random `SECRET_KEY` (generate with `python -m secrets`)
- Never commit `.env` to version control
- Add `.env` to `.gitignore`
- Rotate AWS keys periodically

---

## Testing

### Test File Upload

Create a test view to verify S3 integration:

```python
# apps/shop/tests/test_s3_upload.py
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.shop.models import Product

class S3UploadTest(TestCase):
    def test_image_upload_to_s3(self):
        """Test that images are uploaded to S3 in production"""
        # Create a test image
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )
        
        # Create product with image
        product = Product.objects.create(
            name='Test Product',
            price=100,
            image=image
        )
        
        # Check that image URL points to S3 (or local in dev)
        self.assertIsNotNone(product.image.url)
        
        # In production, should contain S3 domain
        if not settings.DEBUG:
            self.assertIn('s3.', product.image.url)
```

Run tests:
```bash
python manage.py test
```

### Manual S3 Test

Python shell test:
```python
python manage.py shell

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Upload test file
path = default_storage.save('test.txt', ContentFile(b'Hello S3!'))
print(f"Saved to: {path}")

# Get URL
url = default_storage.url(path)
print(f"URL: {url}")

# Verify
assert default_storage.exists(path)

# Cleanup
default_storage.delete(path)
```

---

## Deployment

### Pre-Deployment Checklist

- [ ] AWS IAM user created with correct permissions
- [ ] S3 bucket created and configured
- [ ] Environment variables set in deployment platform
- [ ] `requirements.txt` includes all AWS dependencies
- [ ] Settings reference correct environment module
- [ ] `.env` file is in `.gitignore`
- [ ] Static files collected: `python manage.py collectstatic`
- [ ] Database migrations applied: `python manage.py migrate`

### Railway Deployment

1. **Set Environment Variables** in Railway dashboard:
   ```
   DJANGO_SETTINGS_MODULE=config.settings.production
   AWS_ACCESS_KEY_ID=your-key
   AWS_SECRET_ACCESS_KEY=your-secret
   AWS_STORAGE_BUCKET_NAME=your-bucket
   AWS_S3_REGION_NAME=ap-northeast-1
   ```

2. **Verify `railway.json`**:
   ```json
   {
     "$schema": "https://railway.app/railway.schema.json",
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "gunicorn config.wsgi:application",
       "restartPolicyType": "ON_FAILURE",
       "restartPolicyMaxRetries": 10
     }
   }
   ```

3. **Deploy**:
   ```bash
   git push origin main
   ```

### Heroku Deployment

```bash
# Set environment variables
heroku config:set DJANGO_SETTINGS_MODULE=config.settings.production
heroku config:set AWS_ACCESS_KEY_ID=your-key
heroku config:set AWS_SECRET_ACCESS_KEY=your-secret
heroku config:set AWS_STORAGE_BUCKET_NAME=your-bucket
heroku config:set AWS_S3_REGION_NAME=ap-northeast-1

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
```

---

## Troubleshooting

### Common Issues

#### 1. **403 Forbidden Error**

**Symptoms**: Cannot upload files, getting permission denied errors.

**Solutions**:
- Verify IAM user has correct S3 permissions
- Check bucket policy doesn't block uploads
- Ensure AWS credentials are correct
- Verify `AWS_STORAGE_BUCKET_NAME` matches actual bucket

#### 2. **NoSuchBucket Error**

**Symptoms**: Bucket does not exist error.

**Solutions**:
- Verify bucket name is correct (no typos)
- Check bucket exists in correct region
- Ensure `AWS_S3_REGION_NAME` matches bucket region

#### 3. **Files Not Appearing After Upload**

**Symptoms**: Upload succeeds but files not accessible.

**Solutions**:
- Check `MEDIA_URL` is correctly configured
- Verify S3 URL construction in settings
- Test file access directly via S3 console
- Check browser console for CORS errors

#### 4. **ACL Errors (Access Control List)**

**Symptoms**: `AccessControlListNotSupported` or ACL-related errors.

**Solutions**:
- **DO NOT** set `AWS_DEFAULT_ACL` (removed in this implementation)
- Use bucket-level permissions instead of object ACLs
- Ensure bucket has "Block all public access" enabled
- Use IAM for access control

#### 5. **ImageKit Not Using S3**

**Symptoms**: Original images in S3 but thumbnails stored locally.

**Solutions**:
```python
# Ensure these are set in production.py
IMAGEKIT_DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'
IMAGEKIT_CACHEFILE_STORAGE = 'storages.backends.s3.S3Storage'
```

### Debug Commands

Check current storage backend:
```python
from django.core.files.storage import default_storage
print(default_storage.__class__)
# Should show: storages.backends.s3.S3Storage
```

List S3 bucket contents:
```bash
aws s3 ls s3://your-bucket-name/media/ --recursive
```

Test AWS credentials:
```bash
aws sts get-caller-identity
```

---

## Best Practices

### Security

1. **Never Commit Credentials**
   - Add `.env` to `.gitignore`
   - Use environment variables for all secrets
   - Rotate AWS keys every 90 days

2. **Principle of Least Privilege**
   - Create dedicated IAM user per project
   - Grant only necessary S3 permissions
   - Use bucket policies for additional restrictions

3. **Enable Encryption**
   - Enable S3 bucket encryption (AES-256)
   - Use HTTPS only (`SECURE_SSL_REDIRECT = True`)

### Performance

1. **Use CloudFront CDN** (Optional Enhancement)
   ```python
   AWS_S3_CUSTOM_DOMAIN = 'dxxxxx.cloudfront.net'
   AWS_CLOUDFRONT_KEY_ID = env('AWS_CLOUDFRONT_KEY_ID')
   AWS_CLOUDFRONT_KEY = env('AWS_CLOUDFRONT_KEY').encode('ascii')
   ```

2. **Optimize Images**
   - Use `django-imagekit` for automatic resizing
   - Generate thumbnails on upload
   - Set appropriate cache headers

3. **Enable S3 Transfer Acceleration** (For Global Apps)
   ```python
   AWS_S3_USE_ACCELERATE_ENDPOINT = True
   ```

### Cost Management

1. **Lifecycle Policies**
   - Archive old media to Glacier after 90 days
   - Delete temporary files automatically

2. **Monitor Usage**
   - Set up billing alerts in AWS
   - Review S3 metrics monthly
   - Clean up unused files

3. **Optimize Storage Class**
   - Use S3 Standard for active files
   - Use S3 Intelligent-Tiering for variable access

### Development Workflow

1. **Use Different Buckets Per Environment**
   ```
   your-project-media-development
   your-project-media-staging
   your-project-media-production
   ```

2. **Test Locally First**
   - Keep AWS credentials optional in development
   - Fallback to local storage when missing
   - Test uploads in dev before deploying

3. **Backup Strategy**
   - Enable S3 versioning
   - Set up cross-region replication for critical data
   - Regular backups of database metadata

---

## Additional Resources

### AWS Documentation
- [S3 Getting Started](https://docs.aws.amazon.com/AmazonS3/latest/userguide/GetStartedWithS3.html)
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [S3 Security](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)

### Django Libraries
- [django-storages](https://django-storages.readthedocs.io/)
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [django-imagekit](https://django-imagekit.readthedocs.io/)

### Tools
- [AWS CLI](https://aws.amazon.com/cli/)
- [S3 Browser](https://s3browser.com/)

---

## Quick Reference

### Essential Settings Variables
```python
AWS_ACCESS_KEY_ID                # IAM user access key
AWS_SECRET_ACCESS_KEY            # IAM user secret key
AWS_STORAGE_BUCKET_NAME          # S3 bucket name
AWS_S3_REGION_NAME              # AWS region (e.g., ap-northeast-1)
AWS_S3_CUSTOM_DOMAIN            # S3 URL domain
AWS_S3_ENDPOINT_URL             # S3 endpoint
AWS_LOCATION                    # Folder prefix in bucket
```

### Common AWS Regions
- `us-east-1` - US East (N. Virginia)
- `us-west-2` - US West (Oregon)
- `eu-west-1` - Europe (Ireland)
- `ap-northeast-1` - Asia Pacific (Tokyo)
- `ap-southeast-1` - Asia Pacific (Singapore)

### Useful Commands
```bash
# Collect static files
python manage.py collectstatic --noinput

# Create cache table
python manage.py createcachetable

# Test S3 connection
python manage.py shell -c "from django.core.files.storage import default_storage; print(default_storage.exists('test.txt'))"

# List AWS CLI profiles
aws configure list-profiles

# Sync local files to S3
aws s3 sync ./media s3://your-bucket/media/
```

---

## Changelog

- **2026-01-14**: Initial version based on pastry shop project
  - S3 integration with django-storages
  - Conditional storage backend (S3/local)
  - ImageKit S3 support
  - Removed ACL configuration to avoid errors
  - Whitenoise for static files

---

## License

This guide is provided as-is for use in your projects. Modify as needed for your specific requirements.

---

**Last Updated**: January 14, 2026  
**Project**: Real Estate Agency Platform (Taiwan)  
**Author**: Development Team
