# Smart Attendance System - Docker Deployment Guide

## 🚀 Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- Webcam (for face recognition)

### One-Command Deployment
```bash
./deploy.sh
```

### Manual Docker Deployment
```bash
# Build and start services
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🌐 Access the Application

Once deployed, access the web application at:
**http://localhost:5000**

### Default Admin Credentials:
- Username: `admin`
- Password: `admin123`

## 📱 How to Use the Web App

### 1. **Home Page** (http://localhost:5000)
- Overview of system features
- Navigation to all modules

### 2. **Register Users** (http://localhost:5000/register)
- Fill user details (Name, Email, Roll Number)
- Click "Register with Face"
- Camera will open - position face and press SPACE
- Face encoding will be stored in database

### 3. **Mark Attendance** (http://localhost:5000/attendance)
- Click "Mark My Attendance"
- Camera opens - position face and press SPACE
- System recognizes face and marks attendance
- Only one attendance per day allowed

### 4. **Admin Dashboard** (http://localhost:5000/admin)
- Login with admin credentials
- View total users and today's attendance
- Access to management features

## 🔧 Docker Services

### Web Application
- **Port**: 5000
- **Container**: attendance_web
- **Access**: http://localhost:5000

### MySQL Database
- **Port**: 3306
- **Container**: attendance_mysql
- **Database**: attendance_system
- **Username**: appuser
- **Password**: apppassword

## 📊 Database Tables

1. **users** - Stores user information and face encodings
2. **attendance** - Records daily attendance
3. **admin** - Admin credentials

## 🛠️ Development Commands

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs web
docker-compose logs mysql

# Access web container shell
docker-compose exec web bash

# Access MySQL
docker-compose exec mysql mysql -u appuser -p attendance_system

# Rebuild after code changes
docker-compose up --build

# Clean up everything
docker-compose down -v
docker system prune -f
```

## 🔍 Troubleshooting

### Camera Issues
- Ensure camera permissions are granted
- Close other applications using camera
- Camera access works from host machine to Docker container

### Database Connection Issues
- Wait for MySQL to fully start (health check included)
- Check logs: `docker-compose logs mysql`

### Port Conflicts
- Change ports in docker-compose.yml if 5000 or 3306 are in use

## 🌟 Features

✅ **Web-based Interface** - Access from any browser  
✅ **Real-time Face Recognition** - OpenCV + face_recognition  
✅ **MySQL Database** - Persistent data storage  
✅ **Responsive Design** - Bootstrap 5 UI  
✅ **Docker Deployment** - Easy setup and deployment  
✅ **Admin Dashboard** - User and attendance management  

## 📁 Project Structure

```
smart-attendance-system/
├── Dockerfile              # Web app container
├── docker-compose.yml      # Multi-service deployment
├── deploy.sh              # One-click deployment
├── init.sql               # Database initialization
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
└── ...                    # Other project files
```

This is a **complete web application** that you can access through your browser at http://localhost:5000 after deployment! 🎉