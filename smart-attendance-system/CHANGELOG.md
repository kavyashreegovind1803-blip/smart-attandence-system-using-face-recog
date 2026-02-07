# Changelog - Smart Attendance System

## [v1.1.0] - February 7, 2026

### Removed
- **Mobile Number Field**: Removed mobile number requirement from user registration
  - Removed from registration form (`register.html`)
  - Removed from photo capture page (`capture_photo.html`)
  - Removed from admin users page (`admin_users.html`)
  - Removed from database schema (`database.py`, `init.sql`)
  - Removed from backend validation (`app.py`)

### Fixed
- **Admin Users Page**: Fixed internal server error on `/admin/users` endpoint
  - Updated SQL query to exclude mobile column
  - Updated template to display only: ID, Name, Email, Roll Number, Registered On

### Changed
- **Database Schema**: Users table now contains:
  - `id` (INT, AUTO_INCREMENT, PRIMARY KEY)
  - `name` (VARCHAR(100), NOT NULL)
  - `email` (VARCHAR(100), UNIQUE, NOT NULL)
  - `roll_number` (VARCHAR(50), UNIQUE, NOT NULL)
  - `face_encoding` (TEXT)
  - `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

### Migration
- Created `migrate_remove_mobile.sql` for existing databases
- Run migration: `ALTER TABLE users DROP COLUMN IF EXISTS mobile;`

### Testing
- ✅ Home page: http://localhost:5000 (200 OK)
- ✅ Register page: http://localhost:5000/register (200 OK)
- ✅ Admin users page: http://localhost:5000/admin/users (200 OK)
- ✅ Docker containers running successfully
- ✅ No errors in application logs

### Files Modified
1. `app.py` - Removed mobile validation and database operations
2. `config/database.py` - Updated users table schema
3. `init.sql` - Removed mobile column from CREATE TABLE
4. `app/templates/register.html` - Removed mobile input field and validation
5. `app/templates/capture_photo.html` - Removed mobile from hidden form
6. `app/templates/admin_users.html` - Removed mobile column from table

### Files Created
1. `migrate_remove_mobile.sql` - Migration script for existing databases

---

## [v1.0.0] - February 2026

### Added
- Initial release with face recognition attendance system
- Admin dashboard with user management
- Registration with face capture
- Attendance marking with face recognition
- Name validation (alphabets only, max 60 chars)
- Email validation (proper format with @ and domain)
- Roll number uniqueness check
- Clear attendance functionality (by date or all)
- Delete users functionality (single or all)
- Today's attendance report
- Monthly attendance report
- Admin settings page
