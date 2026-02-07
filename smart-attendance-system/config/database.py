import mysql.connector
from mysql.connector import Error
import os

class DatabaseConfig:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.database = os.getenv('DB_NAME', 'attendance_system')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')  # Default XAMPP password
        self.port = int(os.getenv('DB_PORT', '3306'))

    def get_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def create_database(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port
            )
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.close()
            connection.close()
            print("Database created successfully")
        except Error as e:
            print(f"Error creating database: {e}")

    def create_tables(self):
        connection = self.get_connection()
        if connection:
            cursor = connection.cursor()
            
            # Users table
            users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                roll_number VARCHAR(50) UNIQUE NOT NULL,
                face_encoding TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            # Attendance table
            attendance_table = """
            CREATE TABLE IF NOT EXISTS attendance (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                date DATE NOT NULL,
                time TIME NOT NULL,
                status ENUM('Present', 'Absent') DEFAULT 'Present',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
            
            # Admin table
            admin_table = """
            CREATE TABLE IF NOT EXISTS admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            cursor.execute(users_table)
            cursor.execute(attendance_table)
            cursor.execute(admin_table)
            
            # Insert default admin
            cursor.execute("SELECT COUNT(*) FROM admin")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO admin (username, password) VALUES ('admin', 'admin123')")
            
            connection.commit()
            cursor.close()
            connection.close()
            print("Tables created successfully")