# Production Deployment Checklist

## Pre-Deployment Verification

### 1. Code Changes Verified ✅
- [x] Mobile number field removed from all files
- [x] Admin users page fixed (no internal server error)
- [x] All validation working (name, email, roll number)
- [x] Face capture and registration working
- [x] Attendance marking working
- [x] Admin dashboard working
- [x] All reports working (today, monthly)
- [x] Settings page working (clear attendance, delete users)

### 2. Database Schema Updated ✅
- [x] Users table schema updated (mobile column removed)
- [x] Migration script created (`migrate_remove_mobile.sql`)
- [x] All foreign key relationships intact

### 3. Docker Testing ✅
- [x] Docker containers build successfully
- [x] MySQL container healthy
- [x] Web application container running
- [x] All endpoints returning 200 OK
- [x] No errors in application logs

## Production Deployment Steps

### Step 1: Backup Current Production
```bash
# Backup database
docker exec attendance_mysql mysqldump -u root -p attendance_system > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup application files
tar -czf app_backup_$(date +%Y%m%d_%H%M%S).tar.gz smart-attendance-system/
```

### Step 2: Stop Current Production
```bash
cd smart-attendance-system
docker-compose down
```

### Step 3: Pull Latest Code
```bash
git pull origin main
```

### Step 4: Run Database Migration (if existing database)
```bash
# Connect to MySQL and run migration
docker exec -i attendance_mysql mysql -u root -p attendance_system < migrate_remove_mobile.sql
```

### Step 5: Rebuild and Start Containers
```bash
docker-compose up -d --build
```

### Step 6: Verify Deployment
```bash
# Check container status
docker ps

# Check application logs
docker logs attendance_web --tail 50

# Check MySQL logs
docker logs attendance_mysql --tail 20

# Test endpoints
curl -I http://localhost:5000
curl -I http://localhost:5000/register
curl -I http://localhost:5000/admin/users
```

### Step 7: Smoke Testing
1. Open browser: http://localhost:5000
2. Test registration flow:
   - Go to Register page
   - Fill in: Name, Email, Roll Number (no mobile field)
   - Capture face photo
   - Verify registration success
3. Test admin panel:
   - Login to admin (username: admin, password: admin123)
   - Check dashboard statistics
   - View all users (verify no mobile column)
   - Check today's report
   - Check monthly report
   - Test settings (clear attendance, delete user)
4. Test attendance marking:
   - Go to Mark Attendance
   - Capture face
   - Verify attendance marked

## Post-Deployment Monitoring

### Monitor Application Logs
```bash
docker logs -f attendance_web
```

### Monitor Database
```bash
docker exec -it attendance_mysql mysql -u root -p
USE attendance_system;
SHOW TABLES;
DESCRIBE users;
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM attendance;
```

### Health Checks
- Application: http://localhost:5000
- Database: Port 3306 accessible
- Container status: Both containers running and healthy

## Rollback Plan (if needed)

### Quick Rollback
```bash
# Stop current containers
docker-compose down

# Restore from backup
tar -xzf app_backup_YYYYMMDD_HHMMSS.tar.gz

# Restore database
docker exec -i attendance_mysql mysql -u root -p attendance_system < backup_YYYYMMDD_HHMMSS.sql

# Start containers
docker-compose up -d
```

## Environment Variables (Production)

Update `.env` file or docker-compose.yml with production values:
```env
DB_HOST=localhost
DB_NAME=attendance_system
DB_USER=root
DB_PASSWORD=<strong_password>
DB_PORT=3306
FLASK_ENV=production
SECRET_KEY=<generate_strong_secret_key>
```

## Security Recommendations

1. **Change Default Admin Password**
   - Login to admin panel
   - Update password in database
   - Default: username=admin, password=admin123

2. **Use Strong Database Password**
   - Update DB_PASSWORD in environment variables
   - Update docker-compose.yml MYSQL_ROOT_PASSWORD

3. **Enable HTTPS**
   - Use reverse proxy (nginx/apache)
   - Configure SSL certificates
   - Redirect HTTP to HTTPS

4. **Firewall Configuration**
   - Allow only necessary ports
   - Restrict database port (3306) to localhost
   - Allow web port (5000 or 80/443)

5. **Regular Backups**
   - Schedule daily database backups
   - Store backups in secure location
   - Test restore procedures

## Performance Optimization

1. **Use Production WSGI Server**
   - Replace Flask development server with Gunicorn or uWSGI
   - Update Dockerfile CMD

2. **Database Optimization**
   - Add indexes on frequently queried columns
   - Regular database maintenance

3. **Caching**
   - Implement Redis for session management
   - Cache static assets

## Support & Troubleshooting

### Common Issues

**Issue: Container won't start**
```bash
docker-compose logs
docker ps -a
```

**Issue: Database connection error**
```bash
docker exec -it attendance_mysql mysql -u root -p
SHOW DATABASES;
```

**Issue: Face recognition not working**
- Check camera permissions
- Verify OpenCV installation
- Check face_encodings directory permissions

### Contact
- Repository: https://github.com/ShahidKhan48/smart-attandence-system
- Issues: Create GitHub issue with logs and error details

---

## Deployment Completed ✅

Date: _________________
Deployed By: _________________
Version: v1.1.0
Status: _________________
Notes: _________________
