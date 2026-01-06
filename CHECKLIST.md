# Pre-Deployment Checklist ✅

Before pushing to Railway, verify these items:

## 📦 Files Created
- [x] `railway.toml` - Railway deployment configuration
- [x] `Procfile` - Backup process definition
- [x] `pyproject.toml` - Updated with production dependencies
- [x] `.env.example` - Environment variables template
- [x] `.gitignore` - Updated to ignore sensitive files
- [x] `generate_secret_key.py` - Secret key generator
- [x] `RAILWAY_DEPLOYMENT.md` - Comprehensive deployment guide
- [x] `DEPLOY_QUICK.md` - Quick reference guide
- [x] `CHECKLIST.md` - This file

## ⚙️ Configuration Updates
- [x] `core/settings.py` - Production-ready (DEBUG, SECRET_KEY, ALLOWED_HOSTS from env)
- [x] `core/settings.py` - Whitenoise middleware added
- [x] `core/settings.py` - PostgreSQL configuration for production
- [x] `core/settings.py` - Security headers enabled
- [x] Database migration created for Agent.is_authorized field

## 🔐 Security
- [x] SECRET_KEY from environment variable
- [x] DEBUG from environment variable (defaults to True for local dev)
- [x] ALLOWED_HOSTS configurable via environment
- [x] `.env` added to `.gitignore`
- [x] Production security headers configured

## 📋 Dependencies Added
- [x] gunicorn (WSGI server for production)
- [x] whitenoise (Static file serving)
- [x] psycopg2-binary (PostgreSQL database adapter)
- [x] dj-database-url (Database URL parser)

## ⚠️ Known Limitations
- [ ] **Media files**: Railway filesystem is ephemeral
  - Solution: Configure Cloudinary or AWS S3 (see RAILWAY_DEPLOYMENT.md)
  - Temporary: Can commit sample images to Git for testing
- [ ] **Email**: No email backend configured
  - Contact form submissions save to database but don't send emails
  - Configure in production: Gmail SMTP, SendGrid, etc.

## 🎯 Before First Deploy

### 1. Generate SECRET_KEY
```bash
python generate_secret_key.py
```
Save the output - you'll need it for Railway.

### 2. Review Settings
- [ ] Verify `core/settings.py` has no hardcoded secrets
- [ ] Check `DEBUG = os.environ.get('DEBUG', 'True') == 'True'`
- [ ] Check `SECRET_KEY = os.environ.get('SECRET_KEY', '...')`

### 3. Test Locally
```bash
# Run development server
python manage.py runserver

# Check pages load:
# - http://localhost:8000/
# - http://localhost:8000/properties/
# - http://localhost:8000/admin/
# - http://localhost:8000/dashboard/ (after login)
```

### 4. Commit Everything
```bash
git add .
git commit -m "Configure for Railway deployment"
git push origin main
```

## 🚀 Railway Setup Steps

### 1. Create Project
- [ ] Go to https://railway.app/
- [ ] New Project → Deploy from GitHub repo
- [ ] Select your repository
- [ ] Railway auto-detects Python/Django

### 2. Add PostgreSQL
- [ ] In Railway project: New → Database → PostgreSQL
- [ ] Verify it's linked to your Django service
- [ ] Check `DATABASE_URL` appears in Variables

### 3. Set Environment Variables
Railway Dashboard → Your Service → Variables:

- [ ] `SECRET_KEY` = (paste from generate_secret_key.py)
- [ ] `DEBUG` = `False`
- [ ] `ALLOWED_HOSTS` = (wait for first deploy to get domain)

### 4. First Deploy
- [ ] Railway automatically deploys on GitHub push
- [ ] Monitor Deploy Logs for errors
- [ ] Note the generated domain: `your-app-xyz.up.railway.app`

### 5. Update ALLOWED_HOSTS
- [ ] Copy the Railway domain
- [ ] Update `ALLOWED_HOSTS` variable: `your-app-xyz.up.railway.app`
- [ ] Redeploy (or wait for auto-redeploy)

### 6. Post-Deploy Setup
In Railway Shell (Settings → Deploy):

```bash
# Create superuser
python manage.py createsuperuser
# Enter: username, email, password

# Verify database
python manage.py dbshell
# Type \dt to see tables, then \q to quit
```

## ✅ Verify Deployment

Test these URLs (replace with your Railway domain):

- [ ] Homepage: `https://your-app.up.railway.app/`
- [ ] Properties: `https://your-app.up.railway.app/properties/`
- [ ] Admin: `https://your-app.up.railway.app/admin/`
- [ ] Register: `https://your-app.up.railway.app/register/`
- [ ] Login: `https://your-app.up.railway.app/login/`

After logging in as agent:
- [ ] Dashboard: `https://your-app.up.railway.app/dashboard/`
- [ ] Create property: Can you add a new property?
- [ ] Upload images: Do images upload? (May not work without cloud storage)

In Admin Panel:
- [ ] Login with superuser credentials
- [ ] Go to Agents
- [ ] Check "is_authorized" for test agent
- [ ] Agent can now see dashboard

## 🐛 If Something Goes Wrong

### Check Railway Logs
Railway Dashboard → Your Service → Logs

Look for:
- Build errors (dependency installation)
- Migration errors (database setup)
- Runtime errors (application crashes)

### Common Fixes

**Build failed:**
```bash
# Check pyproject.toml syntax
# Verify all dependencies are valid
```

**Migrations failed:**
```bash
# In Railway Shell
python manage.py migrate --run-syncdb
```

**Static files not loading:**
```bash
# In Railway Shell
python manage.py collectstatic --noinput
```

**Application crashed:**
- Check `ALLOWED_HOSTS` matches Railway domain
- Check `DATABASE_URL` is set
- Check `SECRET_KEY` is set
- Check logs for specific error

## 📱 Optional: Custom Domain

If you have a custom domain:

1. Railway Dashboard → Your Service → Settings → Domains
2. Add custom domain: `www.yourdomain.com`
3. Add DNS records as shown by Railway
4. Update `ALLOWED_HOSTS`: `www.yourdomain.com,your-app.up.railway.app`

## 🎉 Success Criteria

Your deployment is successful when:

- [x] Homepage loads without errors
- [x] Static files (CSS, JS) are working
- [x] Properties list shows (even if empty)
- [x] Admin panel accessible
- [x] Can register and login as agent
- [x] Superuser can authorize agents
- [x] Authorized agents see dashboard
- [x] Can create/edit/delete properties
- [x] Database persists between deploys
- [x] No 500 errors in logs

## 📚 Next Steps (After Deployment)

### Required for Production:
1. **Media Storage** - Configure Cloudinary or S3 (see RAILWAY_DEPLOYMENT.md)
2. **Email Backend** - Configure SMTP for contact forms
3. **Google Maps API** - Add key for property location maps
4. **SSL Certificate** - Railway provides this automatically
5. **Monitoring** - Set up error tracking (Sentry, etc.)

### Optional Improvements:
- Custom domain
- CDN for static files
- Redis for caching
- Celery for background tasks
- Backup strategy for media files

---

**Ready to deploy?**
1. Read `DEPLOY_QUICK.md` for the 5-step process
2. Read `RAILWAY_DEPLOYMENT.md` for comprehensive guide
3. Follow this checklist step by step

**Last Updated:** January 6, 2026
