-- Insert sample data into all tables

-- Users (Teachers)
INSERT INTO teachers (first_name, last_name, email, age, password_hash, is_active) VALUES
('John', 'Smith', 'john.smith@school.com', 35, 'hashed_password_1', true),
('Jane', 'Doe', 'jane.doe@school.com', 32, 'hashed_password_2', true),
('Michael', 'Johnson', 'michael.johnson@school.com', 45, 'hashed_password_3', true);

-- Users (Students)
INSERT INTO students (first_name, last_name, email, age, password_hash, is_active) VALUES
('Alice', 'Brown', 'alice.brown@school.com', 16, 'hashed_password_4', true),
('Bob', 'Wilson', 'bob.wilson@school.com', 16, 'hashed_password_5', true),
('Charlie', 'Davis', 'charlie.davis@school.com', 15, 'hashed_password_6', true),
('Diana', 'Miller', 'diana.miller@school.com', 15, 'hashed_password_7', true),
('Eve', 'Taylor', 'eve.taylor@school.com', 16, 'hashed_password_8', true),
('Frank', 'Anderson', 'frank.anderson@school.com', 15, 'hashed_password_9', true),
('Grace', 'Thomas', 'grace.thomas@school.com', 16, 'hashed_password_10', true);

-- Subjects
INSERT INTO subjects (subject_code, subject_name, description, teacher_id) VALUES
('MATH101', 'Mathematics', 'Algebra and Geometry', NULL),
('PHY101', 'Physics', 'Classical Physics', NULL),
('CHEM101', 'Chemistry', 'Organic Chemistry', NULL),
('ENG101', 'English', 'English Literature', NULL);

-- Classes
INSERT INTO classes (class_name, section, grade_level, room_number) VALUES
('10A', 'A', 10, '201'),
('10B', 'B', 10, '202'),
('9A', 'A', 9, '301'),
('9B', 'B', 9, '302');

-- Class Timetable (using subqueries for dynamic IDs)
INSERT INTO class_timetable (class_id, subject_id, teacher_id, day_of_week, start_time, end_time) VALUES
((SELECT class_id FROM classes WHERE class_name='10A' LIMIT 1), (SELECT subject_id FROM subjects WHERE subject_code='MATH101' LIMIT 1), (SELECT teacher_id FROM teachers ORDER BY teacher_id LIMIT 1), 'Monday', '09:00', '10:00'),
((SELECT class_id FROM classes WHERE class_name='10A' LIMIT 1), (SELECT subject_id FROM subjects WHERE subject_code='PHY101' LIMIT 1), (SELECT teacher_id FROM teachers ORDER BY teacher_id DESC LIMIT 1 OFFSET 1), 'Monday', '10:00', '11:00'),
((SELECT class_id FROM classes WHERE class_name='10A' LIMIT 1), (SELECT subject_id FROM subjects WHERE subject_code='CHEM101' LIMIT 1), (SELECT teacher_id FROM teachers ORDER BY teacher_id DESC LIMIT 1), 'Tuesday', '09:00', '10:00'),
((SELECT class_id FROM classes WHERE class_name='10B' LIMIT 1), (SELECT subject_id FROM subjects WHERE subject_code='MATH101' LIMIT 1), (SELECT teacher_id FROM teachers ORDER BY teacher_id LIMIT 1), 'Tuesday', '10:00', '11:00'),
((SELECT class_id FROM classes WHERE class_name='10B' LIMIT 1), (SELECT subject_id FROM subjects WHERE subject_code='ENG101' LIMIT 1), (SELECT teacher_id FROM teachers ORDER BY teacher_id LIMIT 1), 'Wednesday', '11:00', '12:00'),
((SELECT class_id FROM classes WHERE class_name='9A' LIMIT 1), (SELECT subject_id FROM subjects WHERE subject_code='PHY101' LIMIT 1), (SELECT teacher_id FROM teachers ORDER BY teacher_id DESC LIMIT 1 OFFSET 1), 'Monday', '14:00', '15:00'),
((SELECT class_id FROM classes WHERE class_name='9B' LIMIT 1), (SELECT subject_id FROM subjects WHERE subject_code='CHEM101' LIMIT 1), (SELECT teacher_id FROM teachers ORDER BY teacher_id DESC LIMIT 1), 'Wednesday', '14:00', '15:00');

-- Student Enrollment (using subqueries for dynamic IDs)
INSERT INTO student_enrollment (student_id, class_id) VALUES
((SELECT student_id FROM students WHERE first_name='Alice' LIMIT 1), (SELECT class_id FROM classes WHERE class_name='10A' LIMIT 1)),
((SELECT student_id FROM students WHERE first_name='Bob' LIMIT 1), (SELECT class_id FROM classes WHERE class_name='10A' LIMIT 1)),
((SELECT student_id FROM students WHERE first_name='Charlie' LIMIT 1), (SELECT class_id FROM classes WHERE class_name='10B' LIMIT 1)),
((SELECT student_id FROM students WHERE first_name='Diana' LIMIT 1), (SELECT class_id FROM classes WHERE class_name='10B' LIMIT 1)),
((SELECT student_id FROM students WHERE first_name='Eve' LIMIT 1), (SELECT class_id FROM classes WHERE class_name='9A' LIMIT 1)),
((SELECT student_id FROM students WHERE first_name='Frank' LIMIT 1), (SELECT class_id FROM classes WHERE class_name='9A' LIMIT 1)),
((SELECT student_id FROM students WHERE first_name='Grace' LIMIT 1), (SELECT class_id FROM classes WHERE class_name='9B' LIMIT 1));

-- Attendance (using subqueries for dynamic IDs)
INSERT INTO attendance (student_id, teacher_id, date, status, remarks) VALUES
((SELECT student_id FROM students WHERE first_name='Alice' LIMIT 1), (SELECT teacher_id FROM teachers ORDER BY teacher_id LIMIT 1), '2024-05-10', 'present', 'On time'),
((SELECT student_id FROM students WHERE first_name='Bob' LIMIT 1), (SELECT teacher_id FROM teachers ORDER BY teacher_id LIMIT 1), '2024-05-10', 'present', 'On time'),
((SELECT student_id FROM students WHERE first_name='Charlie' LIMIT 1), (SELECT teacher_id FROM teachers ORDER BY teacher_id DESC LIMIT 1 OFFSET 1), '2024-05-10', 'absent', 'Sick leave'),
((SELECT student_id FROM students WHERE first_name='Diana' LIMIT 1), (SELECT teacher_id FROM teachers ORDER BY teacher_id DESC LIMIT 1 OFFSET 1), '2024-05-10', 'present', 'On time'),
((SELECT student_id FROM students WHERE first_name='Alice' LIMIT 1), (SELECT teacher_id FROM teachers ORDER BY teacher_id LIMIT 1), '2024-05-11', 'present', 'On time'),
((SELECT student_id FROM students WHERE first_name='Bob' LIMIT 1), (SELECT teacher_id FROM teachers ORDER BY teacher_id LIMIT 1), '2024-05-11', 'late', 'Arrived 10 mins late'),
((SELECT student_id FROM students WHERE first_name='Charlie' LIMIT 1), (SELECT teacher_id FROM teachers ORDER BY teacher_id DESC LIMIT 1 OFFSET 1), '2024-05-11', 'present', 'On time'),
((SELECT student_id FROM students WHERE first_name='Diana' LIMIT 1), (SELECT teacher_id FROM teachers ORDER BY teacher_id DESC LIMIT 1 OFFSET 1), '2024-05-11', 'absent', 'Doctor appointment'),
((SELECT student_id FROM students WHERE first_name='Eve' LIMIT 1), (SELECT teacher_id FROM teachers ORDER BY teacher_id DESC LIMIT 1 OFFSET 1), '2024-05-10', 'present', 'On time'),
((SELECT student_id FROM students WHERE first_name='Frank' LIMIT 1), (SELECT teacher_id FROM teachers ORDER BY teacher_id DESC LIMIT 1), '2024-05-10', 'present', 'On time'),
((SELECT student_id FROM students WHERE first_name='Grace' LIMIT 1), (SELECT teacher_id FROM teachers ORDER BY teacher_id DESC LIMIT 1), '2024-05-10', 'absent', 'Not feeling well');
