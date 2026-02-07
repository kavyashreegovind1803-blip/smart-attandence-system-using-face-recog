#!/usr/bin/env python3
"""
Database Setup Script for Smart Attendance System
Run this script to initialize the database and tables
"""

from config.database import DatabaseConfig

def main():
    print("Setting up Smart Attendance System Database...")
    
    # Initialize database configuration
    db_config = DatabaseConfig()
    
    # Create database
    print("Creating database...")
    db_config.create_database()
    
    # Create tables
    print("Creating tables...")
    db_config.create_tables()
    
    print("Database setup completed successfully!")
    print("\nDefault admin credentials:")
    print("Username: admin")
    print("Password: admin123")
    print("\nYou can now run the application with: python app.py")

if __name__ == "__main__":
    main()