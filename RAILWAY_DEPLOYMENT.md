# Railway Deployment Guide - Real Estate Agency

## Project Overview
Django 6.0 Real Estate Agency platform with agent authentication, property CRUD, and media uploads.

## Prerequisites
- Railway account: https://railway.app/
- GitHub repository connected to Railway
- PostgreSQL database provisioned in Railway

## 🚀 Quick Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### 2. Create Railway Project
1. Go to https://railway.app/dashboard
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Django from `pyproject.toml`

### 3. Add PostgreSQL Database
1. In your Railway project, click "New" → "Database" → "PostgreSQL"
2. Railway automatically creates `DATABASE_URL` environment variable
3. Link it to your Django service

### 4. Configure Environment Variables
In Railway Dashboard → Your Service → Variables, add:

```env
SECRET_KEY=<generate-secure-key>
DEBUG=False
ALLOWED_HOSTS=<your-app>.up.railway.app
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Deploy!
Railway automatically deploys when you push to `main` branch.

### 6. Post-Deployment Setup
After first successful deploy, run in Railway Shell (Settings → Deploy):

```bash
# Create superuser
python manage.py createsuperuser

# Optional: Load sample data (if you have fixtures)
# python manage.py loaddata properties/fixtures/sample_data.json
```

---

## 📁 Project Structure

```
agency/
├── core/                  # Django project settings
│   ├── settings.py       # ✅ Production-ready (handles DEBUG, DATABASE_URL)
│   ├── urls.py
│   └── wsgi.py
├── properties/           # Main app (agents, properties, CRUD)
├── templates/           # Django templates
├── media/              # ⚠️ User uploads (ephemeral on Railway!)
├── staticfiles/        # ⚠️ Generated on deploy (don't commit)
├── pyproject.toml      # ✅ Dependencies (Railway auto-installs)
├── railway.toml        # ✅ Deployment config
├── Procfile           # ✅ Backup start command
├── .env.example       # Template for local development
├── .gitignore
└── manage.py
```

---

## 🔧 Configuration Files

### `railway.toml`
```toml
[deploy]
startCommand = "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn core.wsgi --bind 0.0.0.0:$PORT"
```

**Why this works:**
- `migrate` → Creates/updates database tables
- `collectstatic --noinput` → Collects static files for Whitenoise
- `gunicorn` → Production WSGI server
- `$PORT` → Railway's dynamic port variable

### `pyproject.toml` - Dependencies
```toml
dependencies = [
    "django>=6.0",
    "django-extensions>=4.1",
    "pillow>=11.0.0",          # Image processing
    "gunicorn>=21.2.0",        # Production server
    "whitenoise>=6.6.0",       # Static file serving
    "psycopg2-binary>=2.9.9",  # PostgreSQL adapter
    "dj-database-url>=2.1.0",  # Database URL parsing
]
```

### `settings.py` - Key Changes
```python
# ✅ Environment-based configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# ✅ Whitenoise middleware (after SecurityMiddleware)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ← Added
    ...
]

# ✅ Production database (at bottom of file)
if not DEBUG:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
        )
    }
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    # Security headers...
```

---

## ⚠️ Critical: Media Files Handling

**Problem:** Railway's filesystem is **ephemeral** - uploaded files (agent photos, property images) are deleted on every deploy!

### Solution Options:

#### Option 1: Cloudinary (Recommended - Free Tier Available)
```bash
# Add to pyproject.toml
dependencies = [
    ...
    "cloudinary>=1.36.0",
    "django-cloudinary-storage>=0.3.0",
]
```

```python
# settings.py
INSTALLED_APPS = [
    ...
    'cloudinary_storage',
    'cloudinary',
    ...
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

#### Option 2: AWS S3
```bash
# Add to pyproject.toml
dependencies = [
    ...
    "boto3>=1.34.0",
    "django-storages>=1.14.0",
]
```

```python
# settings.py
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
```

#### Option 3: Commit Sample Images to Git (Quick Fix)
```bash
# .gitignore - Remove media/ exclusion temporarily
# git add media/
# git commit -m "Add sample property images"
```
**⚠️ Not recommended for user-uploaded content!**

---

## 🐛 Common Issues & Solutions

### Issue 1: "Application failed to respond"
**Cause:** Migrations failed or database not connected

**Solution:**
1. Check Railway Logs → Deploy Logs
2. Verify `DATABASE_URL` is set
3. Ensure PostgreSQL service is linked to Django service
4. Run migrations manually in Railway Shell:
   ```bash
   python manage.py migrate
   ```

### Issue 2: "DisallowedHost at /"
**Cause:** `ALLOWED_HOSTS` not configured correctly

**Solution:**
```env
# Railway Variables
ALLOWED_HOSTS=your-app-name.up.railway.app
```
**Note:** Railway provides the domain after first deploy. Update this variable afterwards.

### Issue 3: Static files (CSS/JS) not loading
**Cause:** `collectstatic` failed or Whitenoise not configured

**Solution:**
1. Check Whitenoise is in `MIDDLEWARE` (after SecurityMiddleware)
2. Check `STATIC_ROOT = BASE_DIR / "staticfiles"` exists
3. Run manually in Railway Shell:
   ```bash
   python manage.py collectstatic --noinput
   ```

### Issue 4: Images not displaying after deploy
**Cause:** Railway's ephemeral filesystem

**Solution:** Implement Cloudinary or S3 (see Media Files section above)

### Issue 5: "ModuleNotFoundError: No module named 'psycopg2'"
**Cause:** Missing PostgreSQL adapter

**Solution:**
- Check `pyproject.toml` includes `psycopg2-binary>=2.9.9`
- Redeploy (Railway auto-installs dependencies)

### Issue 6: Agent authorization not working
**Cause:** No superuser created to authorize agents

**Solution:**
```bash
# In Railway Shell
python manage.py createsuperuser

# Then visit https://your-app.up.railway.app/admin/
# Go to Agents → Check "is_authorized" for agents
```

---

## 🔐 Security Checklist

Before going live:

- [ ] `DEBUG = False` in production
- [ ] Generate strong `SECRET_KEY` (never commit to Git)
- [ ] Set `ALLOWED_HOSTS` to your Railway domain
- [ ] Enable HTTPS redirects (already in settings if DEBUG=False)
- [ ] Secure cookies enabled (already in settings if DEBUG=False)
- [ ] Review agent authorization workflow
- [ ] Set up media file storage (Cloudinary/S3)
- [ ] Configure email backend for contact forms
- [ ] Add Google Maps API key if using maps

---

## 📊 Monitoring & Maintenance

### View Logs
Railway Dashboard → Your Service → Logs

**Log Types:**
- **Build Logs:** Dependency installation, file copying
- **Deploy Logs:** Migrations, collectstatic, startup
- **Application Logs:** Django runtime logs (errors, requests)

### Running Commands
Railway Dashboard → Your Service → Settings → Deploy → Shell

```bash
# Check Django version
python -c "import django; print(django.VERSION)"

# Check database connection
python manage.py dbshell

# List all agents
python manage.py shell
>>> from properties.models import Agent
>>> Agent.objects.all()

# Create test property
python manage.py shell
>>> from properties.models import Property, Agent
>>> agent = Agent.objects.first()
>>> Property.objects.create(title="Test", price=100000, agent=agent, ...)
```

### Database Backups
Railway provides automatic PostgreSQL backups. View in:
Railway Dashboard → PostgreSQL Service → Backups

---

## 🚦 Deployment Workflow

### Development
```bash
# Work on feature branch
git checkout -b feature/new-feature
# Make changes...
python manage.py runserver  # Test locally

# Commit and push
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

### Production Deploy
```bash
# Merge to main
git checkout main
git merge feature/new-feature
git push origin main

# Railway auto-deploys on push to main
# Monitor deploy in Railway Dashboard
```

### Rollback (if needed)
```bash
# Railway Dashboard → Your Service → Deployments
# Click previous successful deployment → "Redeploy"
```

---

## 📝 Environment Variables Reference

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | ✅ Yes | `django-insecure-abc123...` | Django secret key |
| `DEBUG` | ✅ Yes | `False` | Debug mode (False in prod) |
| `ALLOWED_HOSTS` | ✅ Yes | `myapp.up.railway.app` | Allowed domains |
| `DATABASE_URL` | ✅ Auto | `postgresql://...` | PostgreSQL connection (auto-set) |
| `CLOUDINARY_CLOUD_NAME` | Optional | `my-cloud` | Cloudinary media storage |
| `CLOUDINARY_API_KEY` | Optional | `123456789` | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | Optional | `abcdef` | Cloudinary API secret |
| `EMAIL_HOST_USER` | Optional | `noreply@agency.com` | Email sending |
| `EMAIL_HOST_PASSWORD` | Optional | `app-password` | Email password |
| `GOOGLE_MAPS_API_KEY` | Optional | `AIza...` | Google Maps embed |

---

## 🎯 Post-Deployment Testing

1. **Homepage:** Visit `https://your-app.up.railway.app/`
2. **Properties List:** `/properties/`
3. **Agent Registration:** `/register/`
4. **Admin Panel:** `/admin/` (login with superuser)
5. **Agent Dashboard:** `/dashboard/` (login as agent)
6. **Create Property:** Test CRUD operations
7. **Image Upload:** Test property image upload (verify storage solution)
8. **Contact Form:** Submit inquiry from property detail page

---

## 🆘 Support Resources

- **Railway Docs:** https://docs.railway.app/
- **Django Deployment:** https://docs.djangoproject.com/en/6.0/howto/deployment/
- **Whitenoise Docs:** http://whitenoise.evans.io/
- **Cloudinary Django:** https://cloudinary.com/documentation/django_integration

---

## ✅ Best Practices

**DO:**
- ✅ Use environment variables for secrets
- ✅ Keep `DEBUG=False` in production
- ✅ Use cloud storage for media files
- ✅ Monitor Railway logs regularly
- ✅ Test locally before pushing to main
- ✅ Use Railway's automatic backups

**DON'T:**
- ❌ Commit `.env` file to Git
- ❌ Hardcode `SECRET_KEY` or `DATABASE_URL`
- ❌ Run with `DEBUG=True` in production
- ❌ Store uploaded files on Railway filesystem
- ❌ Ignore Railway build warnings
- ❌ Deploy directly to main without testing

---

**Last Updated:** January 6, 2026  
**Django Version:** 6.0  
**Python Version:** 3.13+
