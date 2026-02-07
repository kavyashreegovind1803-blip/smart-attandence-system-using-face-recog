# 🎓 Smart Attendance System Using Face Recognition

A modern, automated attendance management system that uses facial recognition technology to mark attendance. Built with Flask, OpenCV, and MySQL, containerized with Docker for easy deployment.

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)

---

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation Guide](#-installation-guide)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Navigate to Project Directory](#step-2-navigate-to-project-directory)
  - [Step 3: Run with Docker](#step-3-run-with-docker)
  - [Step 4: Access the Application](#step-4-access-the-application)
- [Application Guide](#-application-guide)
  - [User Features](#user-features)
  - [Admin Features](#admin-features)
- [Troubleshooting](#-troubleshooting)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🔐 Core Features
- **Real-time Face Detection & Recognition** - Automatic face detection using camera
- **Automated Attendance Marking** - No manual intervention required
- **Duplicate Prevention** - Cannot mark attendance twice in a day
- **User Registration** - Easy registration with face capture
- **Admin Dashboard** - Comprehensive management interface

### 📊 Admin Features
- **User Management** - View all registered users
- **Today's Report** - Real-time attendance tracking
- **Monthly Analytics** - Attendance percentage with color-coded indicators
- **Settings Panel** - System configuration options
- **Secure Login** - Session-based authentication

### 🎨 UI/UX Features
- **Responsive Design** - Works on desktop and mobile
- **Modern Interface** - Bootstrap 5 with Font Awesome icons
- **Easy Navigation** - Intuitive user interface
- **Real-time Camera Feed** - Live preview during registration and attendance

---

## 🔧 Prerequisites

Before you begin, make sure you have the following installed on your system:

### Required Software:
1. **Docker Desktop** (Recommended - Easiest Method)
   - Windows: [Download Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
   - Mac: [Download Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
   - Linux: [Install Docker Engine](https://docs.docker.com/engine/install/)

2. **Git** (for cloning the repository)
   - Windows: [Download Git for Windows](https://git-scm.com/download/win)
   - Mac: `brew install git` or [Download](https://git-scm.com/download/mac)
   - Linux: `sudo apt-get install git`

3. **Web Browser** (Chrome, Firefox, or Edge)

### Hardware Requirements:
- **Webcam** (built-in or USB camera)
- **RAM:** 4GB minimum (8GB recommended)
- **Storage:** 2GB free space
- **Processor:** Intel i3 or equivalent

---

## 🚀 Installation Guide

Follow these steps carefully to set up the Smart Attendance System on your computer.

### Step 1: Clone the Repository

Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux) and run:

```bash
git clone https://github.com/yourusername/smart-attendance-system.git
```

**Alternative:** If you don't have Git, download the ZIP file from GitHub and extract it.

---

### Step 2: Navigate to Project Directory

After cloning, navigate into the project folder:

```bash
cd smart-attendance-system
cd smart-attendance-system
```

**Verify you're in the correct directory:**
```bash
# Windows (Command Prompt)
dir

# Mac/Linux
ls
```

You should see files like `docker-compose.yml`, `Dockerfile`, `app.py`, etc.

---

### Step 3: Run with Docker

Docker will automatically set up everything (Python, MySQL, dependencies) for you.

#### 3.1 Start Docker Desktop

- **Windows/Mac:** Open Docker Desktop application and wait until it says "Docker is running"
- **Linux:** Docker should already be running after installation

#### 3.2 Build and Start the Application

Run this command in your terminal (make sure you're in the `smart-attendance-system` directory):

```bash
docker-compose up -d
```

**What this command does:**
- `docker-compose` - Uses Docker Compose to manage multiple containers
- `up` - Starts the containers
- `-d` - Runs in detached mode (background)

**First-time setup will take 5-10 minutes** as it downloads and builds everything.

#### 3.3 Check if Containers are Running

```bash
docker-compose ps
```

You should see two containers running:
- `attendance_web` - Flask application (Status: Up)
- `attendance_mysql` - MySQL database (Status: Up, Healthy)

#### 3.4 View Logs (Optional)

To see what's happening:

```bash
docker-compose logs -f
```

Press `Ctrl+C` to stop viewing logs (containers will keep running).

---

### Step 4: Access the Application

Once the containers are running, open your web browser and go to:

```
http://localhost:5000
```

**🎉 Congratulations!** The Smart Attendance System is now running on your computer.

---

## 📖 Application Guide

### User Features

#### 1️⃣ Home Page
- **URL:** `http://localhost:5000/`
- **Description:** Landing page with navigation to all features
- **Actions:**
  - Click "Register" to create a new user
  - Click "Mark Attendance" to mark your attendance
  - Click "Admin" to access admin dashboard

---

#### 2️⃣ User Registration

**URL:** `http://localhost:5000/register`

**Steps to Register:**

1. **Fill the Registration Form:**
   - Enter your **Full Name**
   - Enter your **Email Address**
   - Enter your **Roll Number** (Student ID)
   - Click **"Register"** button

2. **Capture Your Photo:**
   - Allow camera access when prompted by browser
   - Position your face in the camera frame
   - Make sure your face is clearly visible
   - Click **"Capture Photo"** button
   - Review the captured photo
   - Click **"Submit Registration"**

3. **Success:**
   - You'll see a success message
   - Your face is now registered in the system

**Tips for Best Results:**
- ✅ Good lighting (face should be well-lit)
- ✅ Look directly at the camera
- ✅ Remove glasses if possible
- ✅ Neutral expression
- ❌ Avoid shadows on face
- ❌ Don't cover face with hands/objects

---

#### 3️⃣ Mark Attendance

**URL:** `http://localhost:5000/attendance`

**Steps to Mark Attendance:**

1. **Open Attendance Page:**
   - Click "Mark Attendance" from home page
   - Or directly visit `http://localhost:5000/attendance`

2. **Allow Camera Access:**
   - Browser will ask for camera permission
   - Click "Allow" to enable camera

3. **Position Your Face:**
   - Stand in front of the camera
   - Make sure your face is clearly visible
   - System will automatically detect your face

4. **Capture and Submit:**
   - Click **"Capture & Mark Attendance"** button
   - System will recognize your face
   - Attendance will be marked automatically

5. **Confirmation:**
   - Success message: "Attendance marked for [Your Name]"
   - Error message if face not recognized: "Face not recognized. Please register first."
   - Already marked: "Attendance already marked today"

**Important Notes:**
- ✅ You can only mark attendance **once per day**
- ✅ You must be **registered** before marking attendance
- ✅ Face must be **clearly visible** for recognition

---

### Admin Features

#### 🔐 Admin Login

**URL:** `http://localhost:5000/admin`

**Default Admin Credentials:**
```
Username: admin
Password: admin123
```

**⚠️ Important:** Change the default password after first login for security.

**Steps to Login:**
1. Go to `http://localhost:5000/admin`
2. Enter username: `admin`
3. Enter password: `admin123`
4. Click **"Login"** button
5. You'll be redirected to Admin Dashboard

---

#### 📊 Admin Dashboard

**URL:** `http://localhost:5000/admin/dashboard`

**Overview:**
- **Statistics Cards:**
  - 📈 Total Registered Users
  - ✅ Today's Attendance Count

- **Quick Action Buttons:**
  - 👥 View All Users
  - 📅 Today's Report
  - 📊 Monthly Report
  - ⚙️ Settings

---

#### 👥 View All Users

**URL:** `http://localhost:5000/admin/users`

**Features:**
- View complete list of registered users
- Information displayed:
  - User ID
  - Full Name
  - Email Address
  - Roll Number
  - Registration Date & Time
- Total user count at bottom
- Back to Dashboard button

**Use Cases:**
- Check who is registered in the system
- Verify user information
- Get registration timestamps

---

#### 📅 Today's Report

**URL:** `http://localhost:5000/admin/today_report`

**Features:**
- Real-time attendance for current day
- Information displayed:
  - Serial Number
  - Student Name
  - Roll Number
  - Check-in Time (HH:MM:SS)
- Total present count
- Current date display
- Empty state message if no attendance

**Use Cases:**
- Monitor who attended today
- Check attendance timestamps
- Quick daily attendance verification

---

#### 📊 Monthly Report

**URL:** `http://localhost:5000/admin/monthly_report`

**Features:**
- Comprehensive monthly attendance analytics
- Information displayed:
  - Student Name
  - Roll Number
  - Days Present (count)
  - Attendance Percentage
- **Color-Coded Badges:**
  - 🟢 **Green (≥75%):** Good attendance
  - 🟡 **Yellow (50-74%):** Average attendance
  - 🔴 **Red (<50%):** Poor attendance
- Based on 22 working days per month
- Current month and year display

**Use Cases:**
- Monthly performance tracking
- Identify students with low attendance
- Generate attendance reports
- Academic performance correlation

---

#### ⚙️ Settings

**URL:** `http://localhost:5000/admin/settings`

**Features:**

**1. Admin Profile Section:**
- View current username
- Change password (coming soon)

**2. System Settings:**
- Working days per month (default: 22)
- Minimum attendance percentage (default: 75%)
- Face recognition threshold (default: 0.6)

**3. Danger Zone:**
- Clear all attendance records (with confirmation)
- Delete all users (with confirmation)

**⚠️ Warning:** Actions in Danger Zone are irreversible!

---

#### 🚪 Logout

**URL:** `http://localhost:5000/admin/logout`

**Steps:**
1. Click **"Logout"** button in top-right corner of any admin page
2. Session will be cleared
3. Redirected to admin login page

**Security Note:** Always logout when finished, especially on shared computers.

---

## 🔧 Docker Commands Reference

### Basic Commands

**Start the application:**
```bash
docker-compose up -d
```

**Stop the application:**
```bash
docker-compose down
```

**Restart the application:**
```bash
docker-compose restart
```

**View running containers:**
```bash
docker-compose ps
```

**View logs:**
```bash
# All logs
docker-compose logs

# Follow logs (real-time)
docker-compose logs -f

# Logs for specific service
docker-compose logs web
docker-compose logs mysql
```

**Rebuild containers (after code changes):**
```bash
docker-compose up -d --build
```

**Stop and remove everything (including volumes):**
```bash
docker-compose down -v
```

---

## 🐛 Troubleshooting

### Issue 1: Docker not starting

**Error:** "Cannot connect to Docker daemon"

**Solution:**
- Make sure Docker Desktop is running
- Windows: Check system tray for Docker icon
- Mac: Check menu bar for Docker icon
- Restart Docker Desktop

---

### Issue 2: Port 5000 already in use

**Error:** "Port 5000 is already allocated"

**Solution:**
```bash
# Stop the conflicting service or change port in docker-compose.yml
# Edit docker-compose.yml and change:
ports:
  - "5001:5000"  # Changed from 5000:5000

# Then access at http://localhost:5001
```

---

### Issue 3: Camera not working

**Error:** "Camera access denied" or "No camera detected"

**Solution:**
- Check browser permissions (allow camera access)
- Make sure no other application is using the camera
- Try a different browser (Chrome recommended)
- Check if camera is properly connected (for USB cameras)

---

### Issue 4: Face not recognized

**Error:** "Face not recognized. Please register first."

**Solution:**
- Make sure you are registered in the system
- Ensure good lighting conditions
- Position face clearly in front of camera
- Remove glasses or accessories if possible
- Try re-registering with better photo quality

---

### Issue 5: Database connection error

**Error:** "Can't connect to MySQL server"

**Solution:**
```bash
# Wait for MySQL to be fully ready (takes 30-60 seconds)
docker-compose logs mysql

# Look for: "ready for connections"

# If still not working, restart:
docker-compose restart mysql
```

---

### Issue 6: Containers not starting

**Error:** Various startup errors

**Solution:**
```bash
# Clean up and restart
docker-compose down -v
docker-compose up -d --build

# Check logs for specific errors
docker-compose logs -f
```

---

## 💻 Technology Stack

### Backend
- **Python 3.9** - Programming language
- **Flask 2.3.3** - Web framework
- **OpenCV 4.8.1** - Computer vision library
- **face_recognition 1.3.0** - Face recognition library
- **MySQL 8.0** - Database
- **mysql-connector-python** - Database connector

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling
- **JavaScript** - Interactivity
- **Bootstrap 5.3.0** - UI framework
- **Font Awesome 6.0.0** - Icons
- **jQuery 3.6.0** - DOM manipulation

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

---

## 📁 Project Structure

```
smart-attendance-system/
│
├── app/
│   ├── static/
│   │   └── css/
│   │       └── style.css          # Custom styles
│   └── templates/
│       ├── base.html              # Base template
│       ├── index.html             # Home page
│       ├── register.html          # Registration form
│       ├── capture_photo.html     # Photo capture page
│       ├── mark_attendance_camera.html  # Attendance marking
│       ├── admin_login.html       # Admin login
│       ├── admin_dashboard.html   # Admin dashboard
│       ├── admin_users.html       # User management
│       ├── admin_today_report.html     # Today's report
│       ├── admin_monthly_report.html   # Monthly report
│       └── admin_settings.html    # Settings page
│
├── config/
│   └── database.py                # Database configuration
│
├── utils/
│   ├── __init__.py
│   └── face_utils.py              # Face recognition utilities
│
├── app.py                         # Main Flask application
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker Compose configuration
├── .dockerignore                  # Docker ignore file
├── init.sql                       # Database initialization
├── setup_database.py              # Database setup script
├── deploy.sh                      # Deployment script
├── README.md                      # This file
└── DOCKER_README.md               # Docker-specific documentation
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/AmazingFeature`
3. **Commit your changes:** `git commit -m 'Add some AmazingFeature'`
4. **Push to the branch:** `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**[Your Name]**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- OpenCV community for computer vision tools
- Flask framework developers
- face_recognition library by Adam Geitgey
- Bootstrap team for the UI framework
- All contributors and testers

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [GitHub Issues](https://github.com/yourusername/smart-attendance-system/issues)
3. Create a new issue with detailed description
4. Contact: your.email@example.com

---

## 🔄 Version History

- **v1.0.0** (Current)
  - Initial release
  - Face detection and recognition
  - User registration
  - Attendance marking
  - Admin dashboard with reports
  - Docker deployment

---

## 🎯 Future Enhancements

- [ ] Mobile application (Android/iOS)
- [ ] Cloud deployment (AWS/Azure/GCP)
- [ ] Email notifications for attendance
- [ ] SMS alerts for low attendance
- [ ] Export reports to PDF/Excel
- [ ] Multi-camera support
- [ ] Integration with existing ERP systems
- [ ] Advanced analytics and insights
- [ ] Attendance prediction using ML
- [ ] QR code backup attendance method

---

## ⭐ Star this Repository

If you find this project useful, please give it a star! ⭐

---

**Made with ❤️ for educational institutions and organizations**
