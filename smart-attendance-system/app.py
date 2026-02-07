from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import cv2
import numpy as np
import base64
from PIL import Image
import io
import pickle
import os
import re
from datetime import datetime, date
from config.database import DatabaseConfig
from utils.face_utils import FaceRecognitionUtils

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = 'your-secret-key-here'

# Initialize database
db_config = DatabaseConfig()
face_utils = FaceRecognitionUtils()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    connection = db_config.get_connection()
    cursor = connection.cursor()
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE date = %s", (date.today(),))
    today_attendance = cursor.fetchone()[0]
    
    cursor.close()
    connection.close()
    
    return render_template('admin_dashboard.html', 
                         total_users=total_users, 
                         today_attendance=today_attendance)

@app.route('/admin/users')
def admin_users():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    connection = db_config.get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, email, roll_number, created_at FROM users ORDER BY created_at DESC")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('admin_users.html', users=users)

@app.route('/admin/today_report')
def admin_today_report():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    connection = db_config.get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT u.name, u.roll_number, a.time 
        FROM attendance a 
        JOIN users u ON a.user_id = u.id 
        WHERE a.date = %s 
        ORDER BY a.time DESC
    """, (date.today(),))
    attendance_records = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('admin_today_report.html', 
                         attendance_records=attendance_records,
                         report_date=date.today())

@app.route('/admin/monthly_report')
def admin_monthly_report():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    connection = db_config.get_connection()
    cursor = connection.cursor()
    
    # Get current month's attendance
    cursor.execute("""
        SELECT u.name, u.roll_number, COUNT(a.id) as days_present
        FROM users u
        LEFT JOIN attendance a ON u.id = a.user_id 
            AND MONTH(a.date) = MONTH(CURDATE()) 
            AND YEAR(a.date) = YEAR(CURDATE())
        GROUP BY u.id, u.name, u.roll_number
        ORDER BY u.name
    """)
    monthly_records = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('admin_monthly_report.html', 
                         monthly_records=monthly_records,
                         current_month=datetime.now().strftime('%B %Y'))

@app.route('/admin/settings')
def admin_settings():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    return render_template('admin_settings.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully')
    return redirect(url_for('admin_login'))

@app.route('/admin/clear_attendance', methods=['POST'])
def clear_attendance():
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.get_json()
    clear_type = data.get('type', 'all')
    date_value = data.get('date', None)
    
    try:
        connection = db_config.get_connection()
        cursor = connection.cursor()
        
        if clear_type == 'date' and date_value:
            cursor.execute("DELETE FROM attendance WHERE date = %s", (date_value,))
            affected = cursor.rowcount
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'success': True, 'message': f'Cleared {affected} attendance record(s) for {date_value}'})
        elif clear_type == 'all':
            cursor.execute("DELETE FROM attendance")
            affected = cursor.rowcount
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'success': True, 'message': f'Cleared all {affected} attendance records'})
        else:
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'Invalid request'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/admin/delete_user', methods=['POST'])
def delete_user():
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.get_json()
    delete_type = data.get('type', 'single')
    user_id = data.get('user_id', None)
    
    try:
        connection = db_config.get_connection()
        cursor = connection.cursor()
        
        if delete_type == 'single' and user_id:
            # Delete user's attendance first
            cursor.execute("DELETE FROM attendance WHERE user_id = %s", (user_id,))
            # Delete user
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'success': True, 'message': 'User deleted successfully'})
        elif delete_type == 'all':
            # Delete all attendance first
            cursor.execute("DELETE FROM attendance")
            # Delete all users
            cursor.execute("DELETE FROM users")
            affected = cursor.rowcount
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'success': True, 'message': f'Deleted all {affected} users'})
        else:
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'Invalid request'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/admin/get_users_list', methods=['GET'])
def get_users_list():
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    try:
        connection = db_config.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, roll_number FROM users ORDER BY name")
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        
        users_list = [{'id': user[0], 'name': user[1], 'roll_number': user[2]} for user in users]
        return jsonify({'success': True, 'users': users_list})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/attendance')
def attendance():
    return render_template('mark_attendance_camera.html')

@app.route('/mark_attendance_with_photo', methods=['POST'])
def mark_attendance_with_photo():
    data = request.get_json()
    photo_data = data['photo']
    
    try:
        # Process the base64 image
        image_data = photo_data.split(',')[1]  # Remove data:image/jpeg;base64, prefix
        image_bytes = base64.b64decode(image_data)
        
        # Convert to OpenCV format for face detection
        image = Image.open(io.BytesIO(image_bytes))
        image_array = np.array(image)
        
        # Generate face encoding from captured image
        face_encoding = face_utils.process_image_for_encoding(image_array)
        
        if face_encoding is not None:
            # Compare with stored encodings
            connection = db_config.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, face_encoding FROM users")
            users = cursor.fetchall()
            
            for user in users:
                stored_encoding = pickle.loads(bytes.fromhex(user[2]))
                # Use our simplified face comparison
                best_match_index, distance = face_utils.compare_faces([stored_encoding], face_encoding)
                
                if best_match_index is not None:
                    # Check if already marked today
                    cursor.execute("""
                        SELECT * FROM attendance 
                        WHERE user_id = %s AND date = %s
                    """, (user[0], date.today()))
                    
                    if cursor.fetchone() is None:
                        # Mark attendance
                        cursor.execute("""
                            INSERT INTO attendance (user_id, date, time) 
                            VALUES (%s, %s, %s)
                        """, (user[0], date.today(), datetime.now().time()))
                        connection.commit()
                        
                        cursor.close()
                        connection.close()
                        return jsonify({'success': True, 'message': f'Attendance marked for {user[1]}'})
                    else:
                        cursor.close()
                        connection.close()
                        return jsonify({'success': False, 'message': 'Attendance already marked today'})
            
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'Face not recognized. Please register first.'})
        else:
            return jsonify({'success': False, 'message': 'No face detected in the image'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error processing attendance: {str(e)}'})

@app.route('/login_admin', methods=['POST'])
def login_admin():
    username = request.form['username']
    password = request.form['password']
    
    connection = db_config.get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
    admin = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if admin:
        session['admin_logged_in'] = True
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Invalid credentials')
        return redirect(url_for('admin_login'))

@app.route('/register_user', methods=['POST'])
def register_user():
    name = request.form['name']
    email = request.form['email']
    roll_number = request.form['roll_number']
    
    # Server-side validation
    # Validate name (alphabets and spaces only, max 60 chars)
    if not name or len(name) > 60 or not all(c.isalpha() or c.isspace() for c in name):
        flash('Invalid name. Use alphabets only (maximum 60 characters).', 'danger')
        return redirect(url_for('register'))
    
    # Validate email format
    email_regex = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        flash('Invalid email format. Please use format like user@gmail.com', 'danger')
        return redirect(url_for('register'))
    
    # Check for duplicates
    connection = db_config.get_connection()
    cursor = connection.cursor()
    
    # Check for duplicate roll number
    cursor.execute("SELECT name FROM users WHERE roll_number = %s", (roll_number,))
    existing_roll = cursor.fetchone()
    if existing_roll:
        cursor.close()
        connection.close()
        flash(f'Roll number already registered with user: {existing_roll[0]}', 'danger')
        return redirect(url_for('register'))
    
    # Check for duplicate email
    cursor.execute("SELECT name FROM users WHERE email = %s", (email,))
    existing_email = cursor.fetchone()
    if existing_email:
        cursor.close()
        connection.close()
        flash(f'Email already registered with user: {existing_email[0]}', 'danger')
        return redirect(url_for('register'))
    
    cursor.close()
    connection.close()
    
    # All validations passed, redirect to camera capture page
    return render_template('capture_photo.html', 
                         name=name, 
                         email=email,
                         roll_number=roll_number)

@app.route('/register_user_with_photo', methods=['POST'])
def register_user_with_photo():
    data = request.get_json()
    name = data['name']
    email = data['email']
    roll_number = data['roll_number']
    photo_data = data['photo']
    
    try:
        # Process the base64 image
        image_data = photo_data.split(',')[1]  # Remove data:image/jpeg;base64, prefix
        image_bytes = base64.b64decode(image_data)
        
        # Convert to OpenCV format for face detection
        image = Image.open(io.BytesIO(image_bytes))
        image_array = np.array(image)
        
        # Generate face encoding
        face_encoding = face_utils.process_image_for_encoding(image_array)
        
        if face_encoding is not None:
            connection = db_config.get_connection()
            cursor = connection.cursor()
            
            # Check for duplicate face
            cursor.execute("SELECT id, name, face_encoding FROM users")
            existing_users = cursor.fetchall()
            
            if existing_users:
                # Compare with all existing faces
                for user in existing_users:
                    user_id, user_name, stored_encoding_hex = user
                    stored_encoding = pickle.loads(bytes.fromhex(stored_encoding_hex))
                    
                    # Compare faces with tolerance of 0.3 (stricter matching)
                    match_index, distance = face_utils.compare_faces([stored_encoding], face_encoding, tolerance=0.3)
                    
                    if match_index is not None:
                        cursor.close()
                        connection.close()
                        return jsonify({
                            'success': False, 
                            'message': f'This face is already registered with user: {user_name}. Please use a different photo or contact admin.'
                        })
            
            # No duplicate found, proceed with registration
            # Convert face encoding to string for storage
            encoding_str = pickle.dumps(face_encoding).hex()
            
            cursor.execute("""
                INSERT INTO users (name, email, roll_number, face_encoding) 
                VALUES (%s, %s, %s, %s)
            """, (name, email, roll_number, encoding_str))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return jsonify({'success': True, 'message': f'User {name} registered successfully!'})
        else:
            return jsonify({'success': False, 'message': 'No face detected in the image. Please try again.'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error registering user: {str(e)}'})

@app.route('/mark_attendance')
def mark_attendance():
    # Get face encoding from camera
    face_encoding = face_utils.capture_face_encoding()
    
    if face_encoding is not None:
        # Compare with stored encodings
        connection = db_config.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, face_encoding FROM users")
        users = cursor.fetchall()
        
        for user in users:
            stored_encoding = pickle.loads(bytes.fromhex(user[2]))
            # Use our simplified face comparison
            best_match_index, distance = face_utils.compare_faces([stored_encoding], face_encoding)
            
            if best_match_index is not None:
                # Check if already marked today
                cursor.execute("""
                    SELECT * FROM attendance 
                    WHERE user_id = %s AND date = %s
                """, (user[0], date.today()))
                
                if cursor.fetchone() is None:
                    # Mark attendance
                    cursor.execute("""
                        INSERT INTO attendance (user_id, date, time) 
                        VALUES (%s, %s, %s)
                    """, (user[0], date.today(), datetime.now().time()))
                    connection.commit()
                    
                    cursor.close()
                    connection.close()
                    return jsonify({'success': True, 'message': f'Attendance marked for {user[1]}'})
                else:
                    cursor.close()
                    connection.close()
                    return jsonify({'success': False, 'message': 'Attendance already marked today'})
        
        cursor.close()
        connection.close()
        return jsonify({'success': False, 'message': 'Face not recognized'})
    else:
        return jsonify({'success': False, 'message': 'No face detected'})

if __name__ == '__main__':
    # Initialize database
    db_config.create_database()
    db_config.create_tables()
    app.run(host='0.0.0.0', port=5000, debug=False)