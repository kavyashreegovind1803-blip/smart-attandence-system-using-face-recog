# Smart Attendance System Using Face Recognition

A college project implementing an automated attendance system using facial recognition technology built with Python Flask and MySQL.

## Features

- **Face Registration**: Register users with facial recognition
- **Automated Attendance**: Mark attendance using face recognition
- **Admin Dashboard**: View statistics and manage users
- **Real-time Processing**: Instant face detection and recognition
- **Secure Database**: MySQL database with proper data management
- **Responsive UI**: Bootstrap-based modern interface

## Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Face Recognition**: OpenCV, face_recognition library
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Development**: XAMPP (for local MySQL server)

## Prerequisites

1. **Python 3.8+** installed on your system
2. **XAMPP** or **MySQL Server** running
3. **Webcam** (built-in or USB camera)
4. **docker**

## Installation

### Step 1: Clone/Download the Project
```bash
cd smart-attendance-system
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup MySQL Database

1. **Start XAMPP** and ensure MySQL is running
2. **Open phpMyAdmin** (http://localhost/phpmyadmin)
3. **Run the database setup script**:
```bash
python setup_database.py
```

### Step 4: Configure Database (if needed)
Edit `config/database.py` if your MySQL settings are different:
```python
self.host = 'localhost'
self.database = 'attendance_system'
self.user = 'root'
self.password = ''  # Your MySQL password
self.port = 3306
```

## Running the Application

1. **Start the Flask application**:
```bash
python app.py
```

2. **Open your web browser** and go to:
```
http://localhost:5000
```

## Usage Guide

### For Students/Employees:

1. **Register**: 
   - Go to Register page
   - Fill in your details
   - Click "Register with Face"
   - Position your face in camera and press SPACE

2. **Mark Attendance**:
   - Go to Mark Attendance page
   - Click "Mark My Attendance"
   - Position your face in camera and press SPACE
   - System will recognize and mark attendance

### For Administrators:

1. **Login**: 
   - Go to Admin page
   - Default credentials: `admin` / `admin123`

2. **Dashboard**:
   - View total registered users
   - Check today's attendance count
   - Access reports and management features

## Project Structure

```
smart-attendance-system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── setup_database.py      # Database setup script
├── README.md             # This file
├── config/
│   └── database.py       # Database configuration
├── utils/
│   └── face_utils.py     # Face recognition utilities
├── app/
│   ├── templates/        # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── register.html
│   │   ├── attendance.html
│   │   ├── admin_login.html
│   │   └── admin_dashboard.html
│   └── static/
│       └── css/
│           └── style.css # Custom styles
└── face_encodings/       # Stored face encodings
```

## Database Schema

### Users Table
- `id` (Primary Key)
- `name` (Full Name)
- `email` (Email Address)
- `roll_number` (Student/Employee ID)
- `face_encoding` (Encoded face data)
- `created_at` (Registration timestamp)

### Attendance Table
- `id` (Primary Key)
- `user_id` (Foreign Key to users)
- `date` (Attendance date)
- `time` (Attendance time)
- `status` (Present/Absent)
- `created_at` (Record timestamp)

### Admin Table
- `id` (Primary Key)
- `username` (Admin username)
- `password` (Admin password)
- `created_at` (Creation timestamp)

## Troubleshooting

### Common Issues:

1. **Camera not working**:
   - Check if camera is connected
   - Close other applications using camera
   - Try changing camera index in code (0, 1, 2...)

2. **MySQL connection error**:
   - Ensure XAMPP MySQL is running
   - Check database credentials in `config/database.py`
   - Verify database exists

3. **Face recognition not working**:
   - Ensure good lighting
   - Position face clearly in frame
   - Only one face should be visible during registration

4. **Module not found errors**:
   - Reinstall requirements: `pip install -r requirements.txt`
   - Use virtual environment if needed

## Future Enhancements

- [ ] Multiple camera support
- [ ] Advanced reporting features
- [ ] Email notifications
- [ ] Mobile app integration
- [ ] Cloud deployment
- [ ] Attendance analytics
- [ ] Export to Excel/PDF

## Contributing

This is a college project. Feel free to fork and enhance for educational purposes.

## License

This project is for educational purposes only.

## Contact

For questions or issues, please contact the project team.
