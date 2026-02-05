from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import cv2
import numpy as np
import base64
from PIL import Image
import io
import pickle
import os
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
    
    # Redirect to camera capture page with user data
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
        
        # Generate a simple face encoding (demo version)
        face_encoding = face_utils.process_image_for_encoding(image_array)
        
        if face_encoding is not None:
            connection = db_config.get_connection()
            cursor = connection.cursor()
            
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