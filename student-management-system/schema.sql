-- =============================================================================
-- STUDENT MANAGEMENT SYSTEM - DATABASE SCHEMA (MySQL)
-- Created for S. Vethavalli Portfolio Project
-- =============================================================================

CREATE DATABASE IF NOT EXISTS student_management_db
  CHARACTER SET utf8mb4 
  COLLATE utf8mb4_unicode_ci;

USE student_management_db;

-- 1. Students Table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    roll_no VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    department VARCHAR(50) NOT NULL,
    semester INT NOT NULL DEFAULT 1,
    gender VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Courses Table
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(20) NOT NULL UNIQUE,
    course_name VARCHAR(100) NOT NULL,
    credits INT NOT NULL DEFAULT 3,
    department VARCHAR(50) NOT NULL
);

-- 3. Marks & Performance Table
CREATE TABLE IF NOT EXISTS marks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_code VARCHAR(20) NOT NULL,
    semester INT NOT NULL,
    internal_marks DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
    external_marks DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
    total_marks DECIMAL(5, 2) GENERATED ALWAYS AS (internal_marks + external_marks) STORED,
    grade VARCHAR(5),
    status VARCHAR(10) DEFAULT 'PASS',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_code) REFERENCES courses(course_code) ON DELETE CASCADE
);

-- 4. Attendance Table
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL UNIQUE,
    total_classes INT NOT NULL DEFAULT 100,
    attended_classes INT NOT NULL DEFAULT 85,
    percentage DECIMAL(5, 2) GENERATED ALWAYS AS ((attended_classes / total_classes) * 100) STORED,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- =============================================================================
-- SEED DATA INSERTION
-- =============================================================================

-- Sample Courses
INSERT INTO courses (course_code, course_name, credits, department) VALUES
('CS101', 'Python Programming & Scripting', 4, 'Computer Applications'),
('CS102', 'Relational Database Systems & MySQL', 4, 'Computer Applications'),
('CS103', 'Web Technologies (HTML, CSS, JS)', 3, 'Computer Applications'),
('CS104', 'C Language & Data Structures', 4, 'Computer Applications'),
('DS201', 'Data Analytics & Power BI', 3, 'Data Science')
ON DUPLICATE KEY UPDATE course_name=VALUES(course_name);

-- Sample Students
INSERT INTO students (roll_no, first_name, last_name, email, phone, department, semester, gender) VALUES
('2025MCA001', 'Aarav', 'Sharma', 'aarav.sharma@example.com', '+91 9876543210', 'Computer Applications', 1, 'Male'),
('2025MCA002', 'Priya', 'Sundaram', 'priya.sundaram@example.com', '+91 9876543211', 'Computer Applications', 1, 'Female'),
('2025MCA003', 'Karthik', 'Raman', 'karthik.raman@example.com', '+91 9876543212', 'Computer Applications', 1, 'Male'),
('2025MCA004', 'Deepika', 'Natarajan', 'deepika.n@example.com', '+91 9876543213', 'Data Science', 1, 'Female'),
('2025MCA005', 'Vikram', 'Aditya', 'vikram.aditya@example.com', '+91 9876543214', 'Computer Applications', 1, 'Male'),
('2025MCA006', 'Ananya', 'Iyer', 'ananya.iyer@example.com', '+91 9876543215', 'Data Science', 1, 'Female')
ON DUPLICATE KEY UPDATE first_name=VALUES(first_name);

-- Sample Marks
INSERT INTO marks (student_id, course_code, semester, internal_marks, external_marks, grade, status) VALUES
(1, 'CS101', 1, 23.00, 68.00, 'A+', 'PASS'),
(1, 'CS102', 1, 24.00, 70.00, 'O', 'PASS'),
(2, 'CS101', 1, 25.00, 72.00, 'O', 'PASS'),
(2, 'CS102', 1, 22.00, 65.00, 'A+', 'PASS'),
(3, 'CS101', 1, 18.00, 50.00, 'B+', 'PASS'),
(3, 'CS102', 1, 19.00, 54.00, 'A', 'PASS'),
(4, 'DS201', 1, 24.00, 71.00, 'O', 'PASS'),
(5, 'CS101', 1, 12.00, 30.00, 'F', 'FAIL'),
(6, 'DS201', 1, 22.00, 64.00, 'A+', 'PASS');

-- Sample Attendance
INSERT INTO attendance (student_id, total_classes, attended_classes) VALUES
(1, 100, 92),
(2, 100, 96),
(3, 100, 84),
(4, 100, 95),
(5, 100, 68),
(6, 100, 90)
ON DUPLICATE KEY UPDATE attended_classes=VALUES(attended_classes);
