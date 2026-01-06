# Railway Deployment Quick Reference

## 🚀 First-Time Deploy (5 Steps)

1. **Generate SECRET_KEY**
   ```bash
   python generate_secret_key.py
   ```
   Copy the output.

2. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Railway deployment"
   git push origin main
   ```

3. **Create Railway Project**
   - Go to https://railway.app/
   - New Project → Deploy from GitHub repo
   - Select your repository

4. **Add PostgreSQL**
   - In Railway project: New → Database → PostgreSQL
   - It auto-links to your Django service

5. **Set Environment Variables**
   Railway Dashboard → Variables → Add:
   ```
   SECRET_KEY=<paste-generated-key>
   DEBUG=False
   ALLOWED_HOSTS=<wait-for-deploy-then-add-domain>
   ```

6. **Update ALLOWED_HOSTS after first deploy**
   - Railway gives you: `your-app-xyz.up.railway.app`
   - Update ALLOWED_HOSTS to this domain
   - Redeploy

7. **Create Superuser**
   Railway Shell:
   ```bash
   python manage.py createsuperuser
   ```

## ⚡ Update Deploy

```bash
git add .
git commit -m "Your changes"
git push origin main
# Railway auto-deploys
```

## 🐛 Quick Troubleshooting

**App not loading?**
```bash
# Railway Shell
python manage.py migrate
python manage.py collectstatic --noinput
```

**Images not showing?**
- Railway filesystem is ephemeral
- Need to use Cloudinary or S3 (see RAILWAY_DEPLOYMENT.md)

**Can't authorize agents?**
```bash
# Railway Shell
python manage.py createsuperuser
# Then go to /admin/ → Agents → Check "is_authorized"
```

## 📝 Required Environment Variables

| Variable | Value | Where to Get |
|----------|-------|--------------|
| SECRET_KEY | `django-insecure-...` | `python generate_secret_key.py` |
| DEBUG | `False` | Hardcode |
| ALLOWED_HOSTS | `your-app.up.railway.app` | From Railway after 1st deploy |
| DATABASE_URL | Auto-set | Railway PostgreSQL service |

## 📦 Files Created for Deployment

- ✅ `railway.toml` - Deploy configuration
- ✅ `Procfile` - Backup start command
- ✅ `pyproject.toml` - Updated with production dependencies
- ✅ `.env.example` - Environment variable template
- ✅ `generate_secret_key.py` - Helper script
- ✅ `RAILWAY_DEPLOYMENT.md` - Full documentation (READ THIS!)
- ✅ Updated `core/settings.py` - Production-ready
- ✅ Updated `.gitignore` - Don't commit secrets

## 🎯 After Deploy Test Checklist

- [ ] Homepage loads: `/`
- [ ] Properties list: `/properties/`
- [ ] Admin panel: `/admin/`
- [ ] Register agent: `/register/`
- [ ] Login: `/login/`
- [ ] Dashboard: `/dashboard/` (after authorization)
- [ ] Create property with images
- [ ] Static files loading (CSS/JS)
- [ ] Images displaying (if cloud storage configured)

## 🔗 Important Links

- Railway Dashboard: https://railway.app/dashboard
- Full Deployment Guide: `RAILWAY_DEPLOYMENT.md`
- Django Admin: `https://your-app.up.railway.app/admin/`

---

Need help? Read the full guide in `RAILWAY_DEPLOYMENT.md`
