-- Migration script to remove mobile column from users table
-- Run this if you have existing database with mobile column

USE attendance_system;

-- Check if mobile column exists and drop it
ALTER TABLE users DROP COLUMN IF EXISTS mobile;
