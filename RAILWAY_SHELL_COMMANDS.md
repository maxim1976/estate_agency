# Railway Web Shell - Quick Commands

## 🚀 After Opening Railway Web Shell

You'll see a prompt like:
```
root@abc123:/app#
```

## 📋 Commands to Run (in order)

### 1. Check if migrations ran:
```bash
python manage.py showmigrations
```

**Look for `[X]` marks:**
```
properties
 [X] 0001_initial
 [X] 0002_property_listing_type
 [X] 0003_property_latitude_property_longitude
 [X] 0004_company
 [X] 0005_agent_is_authorized
```

If you see `[ ]` (empty), run migrations.

---

### 2. Run migrations (if needed):
```bash
python manage.py migrate
```

Should show:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying properties.0001_initial... OK
  ...
```

---

### 3. Create Superuser:
```bash
python manage.py createsuperuser
```

**It will prompt:**
```
Username (leave blank to use 'root'): admin
Email address: your-email@example.com
Password: 
Password (again):
```

**Enter:**
- Username: `admin` (or your choice)
- Email: Your real email
- Password: **Strong password** (min 8 characters)
- Confirm password

**Success message:**
```
Superuser created successfully.
```

---

### 4. Verify database tables:
```bash
python manage.py dbshell
```

Then type:
```sql
\dt
```

**Should show tables like:**
```
 public | auth_user
 public | properties_agent
 public | properties_property
 public | properties_propertyimage
 public | properties_contact
 public | properties_company
```

Type `\q` to exit.

---

### 5. Exit shell:
```bash
exit
```

---

## ✅ After Creating Superuser

1. **Go to admin panel:**
   ```
   https://web-production-f280.up.railway.app/admin/
   ```

2. **Login with:**
   - Username: `admin` (what you chose)
   - Password: (what you set)

3. **Create test data:**
   - Admin → Agents → Add Agent
   - Check ✅ "Is authorized"
   - Save
   
4. **Test the site:**
   - Homepage: `/`
   - Properties: `/properties/`
   - Register: `/register/`
   - Dashboard: `/dashboard/` (login as agent)

---

## 🐛 Common Issues

### Issue: "python: command not found"
**Solution:** Use `python3` instead:
```bash
python3 manage.py createsuperuser
```

### Issue: "django.db.utils.OperationalError: no such table"
**Solution:** Run migrations first:
```bash
python manage.py migrate
```

### Issue: Password validation error
**Solution:** Use stronger password:
- At least 8 characters
- Not too common (not "password123")
- Mix of letters and numbers

---

## 🎯 Quick Checklist

- [ ] Open Railway Web Shell
- [ ] Run: `python manage.py showmigrations`
- [ ] Run: `python manage.py migrate` (if needed)
- [ ] Run: `python manage.py createsuperuser`
- [ ] Enter username, email, password
- [ ] See "Superuser created successfully"
- [ ] Go to `/admin/` and login
- [ ] Create test agent and properties

---

**Done!** Your Railway app is now fully set up! 🎉
