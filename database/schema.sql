-- Face Recognition Attendance System Database Schema
-- Database: attendance_system

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS attendance_system;
USE attendance_system;

-- Students table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    roll_no VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    image LONGBLOB,
    face_encoding TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_roll_no (roll_no),
    INDEX idx_name (name)
);

-- Subjects table
CREATE TABLE IF NOT EXISTS subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_code VARCHAR(20) UNIQUE NOT NULL,
    subject_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_subject_code (subject_code)
);

-- Users table (for teachers/admins)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    enrollment VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('teacher', 'admin', 'student') DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_enrollment (enrollment),
    INDEX idx_username (username)
);

-- Attendance table
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    status ENUM('present', 'absent') DEFAULT 'present',
    marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    marked_by INT,
    attendance_type ENUM('manual', 'automatic') DEFAULT 'automatic',
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (marked_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_student_date (student_id, attendance_date),
    INDEX idx_subject_date (subject_id, attendance_date),
    UNIQUE KEY unique_attendance (student_id, subject_id, attendance_date)
);

-- Insert default subjects
INSERT INTO subjects (subject_code, subject_name) VALUES
('AI', 'Artificial Intelligence'),
('ML', 'Machine Learning'),
('ENT', 'Entrepreneurship and Startups'),
('MATH', 'Mathematics'),
('IKS', 'IKS'),
('MPI', 'Microprocessors & Interfacing')
ON DUPLICATE KEY UPDATE subject_name = VALUES(subject_name);

-- Sample view for attendance reports
CREATE OR REPLACE VIEW attendance_report AS
SELECT 
    s.roll_no,
    s.name AS student_name,
    sub.subject_name,
    a.attendance_date,
    a.status,
    a.attendance_type,
    a.marked_at
FROM attendance a
JOIN students s ON a.student_id = s.id
JOIN subjects sub ON a.subject_id = sub.id
ORDER BY a.attendance_date DESC, s.roll_no;

-- View for attendance statistics
CREATE OR REPLACE VIEW attendance_stats AS
SELECT 
    s.roll_no,
    s.name,
    sub.subject_name,
    COUNT(*) AS total_classes,
    SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) AS classes_attended,
    ROUND((SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS attendance_percentage
FROM attendance a
JOIN students s ON a.student_id = s.id
JOIN subjects sub ON a.subject_id = sub.id
GROUP BY s.id, sub.id
ORDER BY s.roll_no, sub.subject_name;
