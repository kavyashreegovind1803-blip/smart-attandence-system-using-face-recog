# Quick Start Guide - Smart Attendance System

## 🚀 Deploy to Production (5 Minutes)

### Prerequisites
- Docker and Docker Compose installed
- Git installed
- Port 5000 and 3306 available

### Step 1: Clone & Navigate
```bash
git clone https://github.com/ShahidKhan48/smart-attandence-system.git
cd smart-attandence-system/smart-attendance-system
```

### Step 2: Deploy
```bash
docker-compose up -d --build
```

### Step 3: Verify
```bash
# Check containers
docker ps

# Should see:
# - attendance_web (running)
# - attendance_mysql (healthy)
```

### Step 4: Access Application
Open browser: **http://localhost:5000**

---

## 📋 What's New in v1.1.0

### ✅ Changes
- **Removed**: Mobile number field from registration
- **Fixed**: Admin users page (was showing internal error)
- **Updated**: Database schema (no mobile column)

### 🔧 Migration (If Upgrading)
```bash
# Backup first
docker exec attendance_mysql mysqldump -u root -p attendance_system > backup.sql

# Run migration
docker exec -i attendance_mysql mysql -u root -p attendance_system < migrate_remove_mobile.sql

# Rebuild
docker-compose down
docker-compose up -d --build
```

---

## 🎯 Quick Test

### Test Registration
1. Go to: http://localhost:5000/register
2. Fill in:
   - Name: John Doe
   - Email: john@example.com
   - Roll Number: EMP001
3. Capture face photo
4. Verify success message

### Test Admin Panel
1. Go to: http://localhost:5000/admin
2. Login:
   - Username: `admin`
   - Password: `admin123`
3. Check all pages:
   - Dashboard ✅
   - Users ✅ (Fixed - no error)
   - Today's Report ✅
   - Monthly Report ✅
   - Settings ✅

### Test Attendance
1. Go to: http://localhost:5000/attendance
2. Capture face
3. Verify attendance marked

---

## 🔍 Troubleshooting

### Containers won't start
```bash
docker-compose logs
```

### Database connection error
```bash
docker exec -it attendance_mysql mysql -u root -p
```

### Port already in use
```bash
# Change ports in docker-compose.yml
ports:
  - "5001:5000"  # Change 5000 to 5001
```

---

## 📊 Current Status

| Component | Status | Port |
|-----------|--------|------|
| Web App | ✅ Running | 5000 |
| MySQL | ✅ Healthy | 3306 |
| Registration | ✅ Working | - |
| Admin Panel | ✅ Fixed | - |
| Attendance | ✅ Working | - |

---

## 🔐 Security (Production)

### Change Admin Password
```sql
docker exec -it attendance_mysql mysql -u root -p
USE attendance_system;
UPDATE admin SET password = 'new_secure_password' WHERE username = 'admin';
```

### Change DB Password
Update in `docker-compose.yml`:
```yaml
MYSQL_ROOT_PASSWORD: your_secure_password
```

---

## 📝 Registration Fields

### Current Fields (v1.1.0)
- ✅ Name (alphabets only, max 60 chars)
- ✅ Email (valid format required)
- ✅ Roll Number (unique)
- ✅ Face Photo (captured via camera)

### Removed Fields
- ❌ Mobile Number (removed in v1.1.0)

---

## 🛠️ Useful Commands

### View Logs
```bash
docker logs attendance_web --tail 50
docker logs attendance_mysql --tail 20
```

### Restart Containers
```bash
docker-compose restart
```

### Stop Everything
```bash
docker-compose down
```

### Rebuild After Code Changes
```bash
docker-compose down
docker-compose up -d --build
```

### Database Backup
```bash
docker exec attendance_mysql mysqldump -u root -p attendance_system > backup_$(date +%Y%m%d).sql
```

### Database Restore
```bash
docker exec -i attendance_mysql mysql -u root -p attendance_system < backup.sql
```

---

## 📚 Documentation

- **Full Deployment Guide**: `PRODUCTION_DEPLOYMENT.md`
- **Verification Report**: `VERIFICATION_REPORT.md`
- **Change Log**: `CHANGELOG.md`
- **Main README**: `../README.md`

---

## ✅ Deployment Checklist

- [x] Code updated (mobile field removed)
- [x] Database schema updated
- [x] Docker containers built
- [x] All endpoints tested (200 OK)
- [x] Admin users page fixed
- [x] No errors in logs
- [ ] Admin password changed (production)
- [ ] Database password changed (production)
- [ ] HTTPS configured (production)
- [ ] Backups configured (production)

---

## 🎉 You're Ready!

Your Smart Attendance System is ready for production deployment.

**Access:** http://localhost:5000  
**Admin:** http://localhost:5000/admin  
**Credentials:** admin / admin123 (change in production!)

**Need Help?** Check `PRODUCTION_DEPLOYMENT.md` for detailed instructions.
