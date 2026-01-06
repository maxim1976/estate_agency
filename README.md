# Real Estate Agency Platform

A modern, full-featured real estate agency platform built with Django 6.0. Allows agents to register, get authorized by admin, and manage property listings with full CRUD operations.

## ✨ Features

### For Agents
- **Agent Registration & Authentication** - Secure signup and login system
- **Authorization System** - Admin must authorize agents before they can manage properties
- **Dashboard** - Overview of all listings with statistics
- **Property Management (CRUD)**
  - Create new property listings
  - Upload multiple images per property
  - Edit existing properties
  - Delete properties
  - View all your listings in one place
- **Property Types** - House, Apartment, Condo, Villa, Land
- **Listing Types** - For Sale or For Rent

### For Admins
- **Agent Authorization** - Approve or deny agent access
- **Featured Properties** - Mark properties as featured (agents cannot do this)
- **Full Admin Panel** - Manage all properties, agents, and inquiries

### For Visitors
- **Browse Properties** - Filter by location, price, bedrooms, bathrooms, property type
- **Property Details** - View detailed information with image galleries and maps
- **Contact Forms** - Inquire about properties
- **Responsive Design** - Works on desktop, tablet, and mobile

## 🚀 Tech Stack

- **Backend**: Django 6.0
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: Django Templates, Tailwind CSS
- **Deployment**: Railway
- **Static Files**: Whitenoise
- **Server**: Gunicorn

## 📋 Requirements

- Python 3.13+
- uv (package manager)
- PostgreSQL (production only)

## 🛠️ Local Development Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd agency
```

### 2. Create virtual environment and install dependencies
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync
```

### 3. Run migrations
```bash
python manage.py migrate
```

### 4. Create a superuser
```bash
python manage.py createsuperuser
```

### 5. Run the development server
```bash
python manage.py runserver
```

### 6. Access the application
- Homepage: http://localhost:8000/
- Admin Panel: http://localhost:8000/admin/
- Properties: http://localhost:8000/properties/

## 👤 User Workflow

### Agent Registration Flow
1. Visit `/register/` to create an agent account
2. Login at `/login/`
3. Visit `/dashboard/` - you'll see "Authorization Pending" message
4. Admin goes to `/admin/` → Agents → checks "is_authorized" for your account
5. Refresh `/dashboard/` - you can now manage properties!

### Creating Properties
1. Login as authorized agent
2. Go to Dashboard → "Add New Property"
3. Fill in all property details
4. Upload images (multiple allowed)
5. Submit - property appears in your dashboard
6. View on public site at `/properties/`

### Admin Control
1. Login to `/admin/`
2. **Authorize Agents**: Agents → check "is_authorized"
3. **Feature Properties**: Properties → check "featured" (only admins can do this)
4. **Manage Everything**: Full CRUD access to all data

## 🚀 Production Deployment (Railway)

### Quick Deploy (5 Steps)

1. **Generate SECRET_KEY**
   ```bash
   python generate_secret_key.py
   ```

2. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Railway"
   git push origin main
   ```

3. **Create Railway Project**
   - Go to https://railway.app/
   - New Project → Deploy from GitHub repo
   - Add PostgreSQL database

4. **Set Environment Variables** (Railway Dashboard → Variables)
   ```env
   SECRET_KEY=<paste-from-step-1>
   DEBUG=False
   ALLOWED_HOSTS=<your-app>.up.railway.app
   ```

5. **Create Superuser** (Railway Shell)
   ```bash
   python manage.py createsuperuser
   ```

### 📚 Detailed Deployment Guides
- **Quick Reference**: See `DEPLOY_QUICK.md`
- **Full Guide**: See `RAILWAY_DEPLOYMENT.md`
- **Checklist**: See `CHECKLIST.md`

## 📁 Project Structure

```
agency/
├── core/                      # Django project settings
│   ├── settings.py           # ✅ Production-ready
│   ├── urls.py
│   └── wsgi.py
├── properties/               # Main application
│   ├── models.py            # Company, Agent, Property, PropertyImage, Contact
│   ├── views.py             # CRUD views for properties
│   ├── forms.py             # Property and image forms
│   ├── admin.py             # Admin configuration
│   └── urls.py
├── templates/               # Django templates
│   ├── base.html
│   ├── properties/
│   │   ├── home.html
│   │   ├── property_list.html
│   │   ├── property_detail.html
│   │   ├── agent_dashboard.html
│   │   ├── property_form.html
│   │   └── ...
│   └── includes/
│       ├── _header.html
│       └── _footer.html
├── media/                   # User uploads (ephemeral on Railway!)
├── staticfiles/            # Generated on deploy
├── pyproject.toml          # Dependencies
├── railway.toml           # Railway config
├── Procfile              # Process definition
├── .env.example         # Environment template
├── .gitignore
├── manage.py
├── generate_secret_key.py
├── RAILWAY_DEPLOYMENT.md
├── DEPLOY_QUICK.md
└── CHECKLIST.md
```

## 🔧 Configuration Files

### `pyproject.toml`
Contains all dependencies including production packages:
- django, pillow, django-extensions
- gunicorn, whitenoise (production server & static files)
- psycopg2-binary, dj-database-url (PostgreSQL)

### `railway.toml`
Defines the deployment command:
```toml
[deploy]
startCommand = "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn core.wsgi --bind 0.0.0.0:$PORT"
```

### `settings.py` (Production)
- Reads `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` from environment
- Uses PostgreSQL when `DEBUG=False`
- Whitenoise for static file serving
- Security headers enabled

## ⚠️ Important Notes

### Media Files (Images)
**Railway's filesystem is ephemeral** - uploaded images are deleted on deploy!

**Solutions:**
1. **Recommended**: Use Cloudinary or AWS S3 (see `RAILWAY_DEPLOYMENT.md`)
2. **Quick Fix**: Commit sample images to Git (not for real user uploads)

### Featured Properties
- Only admins can mark properties as "featured"
- Agents see the feature status but cannot change it
- Featured properties appear on homepage

### Agent Authorization
- New agents must be authorized by admin before managing properties
- Prevents spam registrations
- Admin control via `/admin/` → Agents → check "is_authorized"

## 🎯 Environment Variables

### Development (.env)
```env
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Production (Railway)
```env
SECRET_KEY=<generate-with-script>
DEBUG=False
ALLOWED_HOSTS=<your-app>.up.railway.app
DATABASE_URL=<auto-provided-by-railway>
```

## 🐛 Troubleshooting

### "DisallowedHost" error
Update `ALLOWED_HOSTS` in Railway variables to match your domain.

### Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Images not showing after deploy
Configure cloud storage (Cloudinary/S3) - see `RAILWAY_DEPLOYMENT.md`

### Can't create properties
1. Check agent is logged in
2. Admin must authorize agent at `/admin/` → Agents

### Database errors
```bash
python manage.py migrate
```

## 📚 Documentation

- **`RAILWAY_DEPLOYMENT.md`** - Comprehensive deployment guide
- **`DEPLOY_QUICK.md`** - Quick reference card
- **`CHECKLIST.md`** - Pre-deployment checklist
- **`COMPANY_MODEL_GUIDE.md`** - Company model documentation
- **`TEMPLATE_DOCUMENTATION.md`** - Template system docs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## 📄 License

This project is private. All rights reserved.

## 🆘 Support

- Check documentation in the docs folder
- Review Railway logs for deployment issues
- See `RAILWAY_DEPLOYMENT.md` for common issues

---

**Built with Django 6.0** | **Deployed on Railway** | **Last Updated: January 6, 2026**
