"""
Quick test script to populate all test data in one go.
Run this after your FastAPI server is running.

Usage:
    python test_data.py
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/v1"
TOKEN = None

# Color codes for terminal output
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def print_step(title: str):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{title}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

def print_success(msg: str, data: Dict = None):
    print(f"{GREEN}✓ {msg}{RESET}")
    if data:
        print(f"  ID: {data.get('id') or data.get('teacher_id') or data.get('student_id') or data.get('class_id') or data.get('subject_id')}")

def print_error(msg: str, error: str = None):
    print(f"{RED}✗ {msg}{RESET}")
    if error:
        print(f"  Error: {error}")

def print_info(msg: str):
    print(f"{YELLOW}ℹ {msg}{RESET}")

def login(username: str = "admin@example.com", password: str = "admin123") -> bool:
    """Login and get JWT token"""
    global TOKEN
    print_step("STEP 0: LOGIN")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": username, "password": password}
        )
        
        if response.status_code == 200:
            TOKEN = response.json()["access_token"]
            print_success("Login successful", {"token": TOKEN[:20] + "..."})
            return True
        else:
            print_error(f"Login failed: {response.status_code}", response.text)
            return False
    except Exception as e:
        print_error("Login error", str(e))
        return False

def get_headers():
    """Get authorization headers"""
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }

def create_teachers() -> Dict[str, int]:
    """Create 3 teachers"""
    print_step("STEP 1: CREATE TEACHERS")
    
    teachers_data = [
        {
            "first_name": "Rajesh",
            "last_name": "Kumar",
            "email": "rajesh.kumar@school.com",
            "age": 35
        },
        {
            "first_name": "Priya",
            "last_name": "Singh",
            "email": "priya.singh@school.com",
            "age": 32
        },
        {
            "first_name": "Arjun",
            "last_name": "Patel",
            "email": "arjun.patel@school.com",
            "age": 40
        }
    ]
    
    teachers = {}
    for i, teacher in enumerate(teachers_data, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/teachers/",
                json=teacher,
                headers=get_headers()
            )
            
            if response.status_code == 201:
                teacher_id = response.json()["teacher_id"]
                teachers[f"teacher_{i}"] = teacher_id
                print_success(f"Teacher {i}: {teacher['first_name']} {teacher['last_name']}", {"teacher_id": teacher_id})
            else:
                print_error(f"Failed to create teacher {i}", response.text)
        except Exception as e:
            print_error(f"Error creating teacher {i}", str(e))
    
    return teachers

def create_subjects(teachers: Dict[str, int]) -> Dict[str, int]:
    """Create 4 subjects"""
    print_step("STEP 2: CREATE SUBJECTS")
    
    subjects_data = [
        {
            "subject_code": "MATH101",
            "subject_name": "Mathematics",
            "description": "Advanced Mathematics for Grade 10",
            "teacher_id": teachers["teacher_1"]
        },
        {
            "subject_code": "ENG101",
            "subject_name": "English",
            "description": "English Language and Literature",
            "teacher_id": teachers["teacher_2"]
        },
        {
            "subject_code": "PHY101",
            "subject_name": "Physics",
            "description": "Physics Fundamentals",
            "teacher_id": teachers["teacher_3"]
        },
        {
            "subject_code": "CHEM101",
            "subject_name": "Chemistry",
            "description": "Chemistry Basics",
            "teacher_id": teachers["teacher_3"]
        }
    ]
    
    subjects = {}
    for i, subject in enumerate(subjects_data, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/subjects/",
                json=subject,
                headers=get_headers()
            )
            
            if response.status_code == 201:
                subject_id = response.json()["subject_id"]
                subjects[f"subject_{i}"] = subject_id
                print_success(f"Subject {i}: {subject['subject_name']}", {"subject_id": subject_id})
            else:
                print_error(f"Failed to create subject {i}", response.text)
        except Exception as e:
            print_error(f"Error creating subject {i}", str(e))
    
    return subjects

def create_students() -> Dict[str, int]:
    """Create 3 students"""
    print_step("STEP 3: CREATE STUDENTS")
    
    students_data = [
        {
            "first_name": "Aarav",
            "last_name": "Sharma",
            "email": "aarav.sharma@student.com",
            "age": 15
        },
        {
            "first_name": "Ananya",
            "last_name": "Verma",
            "email": "ananya.verma@student.com",
            "age": 15
        },
        {
            "first_name": "Rohan",
            "last_name": "Gupta",
            "email": "rohan.gupta@student.com",
            "age": 15
        }
    ]
    
    students = {}
    for i, student in enumerate(students_data, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/students/",
                json=student,
                headers=get_headers()
            )
            
            if response.status_code == 201:
                student_id = response.json()["student_id"]
                students[f"student_{i}"] = student_id
                print_success(f"Student {i}: {student['first_name']} {student['last_name']}", {"student_id": student_id})
            else:
                print_error(f"Failed to create student {i}", response.text)
        except Exception as e:
            print_error(f"Error creating student {i}", str(e))
    
    return students

def create_classes() -> Dict[str, int]:
    """Create 2 classes"""
    print_step("STEP 4: CREATE CLASSES")
    
    classes_data = [
        {
            "class_name": "10A",
            "grade_level": 10,
            "section": "Science",
            "room_number": "101"
        },
        {
            "class_name": "10B",
            "grade_level": 10,
            "section": "Science",
            "room_number": "102"
        }
    ]
    
    classes = {}
    for i, class_data in enumerate(classes_data, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/classes/",
                json=class_data,
                headers=get_headers()
            )
            
            if response.status_code == 201:
                class_id = response.json()["class_id"]
                classes[f"class_{i}"] = class_id
                print_success(f"Class {i}: {class_data['class_name']}", {"class_id": class_id})
            else:
                print_error(f"Failed to create class {i}", response.text)
        except Exception as e:
            print_error(f"Error creating class {i}", str(e))
    
    return classes

def enroll_students(students: Dict[str, int], classes: Dict[str, int]) -> Dict[str, int]:
    """Enroll students to classes"""
    print_step("STEP 5: ENROLL STUDENTS")
    
    enrollments_data = [
        {"student_id": students["student_1"], "class_id": classes["class_1"]},
        {"student_id": students["student_2"], "class_id": classes["class_1"]},
        {"student_id": students["student_3"], "class_id": classes["class_2"]}
    ]
    
    enrollments = {}
    for i, enrollment in enumerate(enrollments_data, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/classes/enrollment/",
                json=enrollment,
                headers=get_headers()
            )
            
            if response.status_code == 201:
                enrollment_id = response.json()["enrollment_id"]
                enrollments[f"enrollment_{i}"] = enrollment_id
                print_success(f"Enrollment {i}: Student {enrollment['student_id']} → Class {enrollment['class_id']}", {"enrollment_id": enrollment_id})
            else:
                print_error(f"Failed to enroll student {i}", response.text)
        except Exception as e:
            print_error(f"Error enrolling student {i}", str(e))
    
    return enrollments

def create_timetable(classes: Dict[str, int], subjects: Dict[str, int], teachers: Dict[str, int]) -> int:
    """Create class timetable for the week"""
    print_step("STEP 6: CREATE CLASS TIMETABLE")
    
    # Full week timetable for Class 10A
    class_id = classes["class_1"]
    
    timetable_entries = [
        # Monday
        {"day": "Monday", "start": "09:00:00", "end": "10:00:00", "subject": "subject_1", "teacher": "teacher_1"},
        {"day": "Monday", "start": "10:00:00", "end": "11:00:00", "subject": "subject_2", "teacher": "teacher_2"},
        {"day": "Monday", "start": "11:00:00", "end": "12:00:00", "subject": "subject_3", "teacher": "teacher_3"},
        
        # Tuesday
        {"day": "Tuesday", "start": "09:00:00", "end": "10:00:00", "subject": "subject_4", "teacher": "teacher_3"},
        {"day": "Tuesday", "start": "10:00:00", "end": "11:00:00", "subject": "subject_1", "teacher": "teacher_1"},
        {"day": "Tuesday", "start": "11:00:00", "end": "12:00:00", "subject": "subject_2", "teacher": "teacher_2"},
        
        # Wednesday
        {"day": "Wednesday", "start": "09:00:00", "end": "10:00:00", "subject": "subject_3", "teacher": "teacher_3"},
        {"day": "Wednesday", "start": "10:00:00", "end": "11:00:00", "subject": "subject_2", "teacher": "teacher_2"},
        {"day": "Wednesday", "start": "11:00:00", "end": "12:00:00", "subject": "subject_1", "teacher": "teacher_1"},
        
        # Thursday
        {"day": "Thursday", "start": "09:00:00", "end": "10:00:00", "subject": "subject_2", "teacher": "teacher_2"},
        {"day": "Thursday", "start": "10:00:00", "end": "11:00:00", "subject": "subject_4", "teacher": "teacher_3"},
        {"day": "Thursday", "start": "11:00:00", "end": "12:00:00", "subject": "subject_3", "teacher": "teacher_3"},
        
        # Friday
        {"day": "Friday", "start": "09:00:00", "end": "10:00:00", "subject": "subject_1", "teacher": "teacher_1"},
        {"day": "Friday", "start": "10:00:00", "end": "11:00:00", "subject": "subject_3", "teacher": "teacher_3"},
        {"day": "Friday", "start": "11:00:00", "end": "12:00:00", "subject": "subject_2", "teacher": "teacher_2"},
    ]
    
    created_count = 0
    for entry in timetable_entries:
        try:
            payload = {
                "class_id": class_id,
                "subject_id": subjects[entry["subject"]],
                "teacher_id": teachers[entry["teacher"]],
                "day_of_week": entry["day"],
                "start_time": entry["start"],
                "end_time": entry["end"],
                "room_number": "101"
            }
            
            response = requests.post(
                f"{BASE_URL}/class-timetable/",
                json=payload,
                headers=get_headers()
            )
            
            if response.status_code == 201:
                created_count += 1
                subject_name = ["Mathematics", "English", "Physics", "Chemistry"][int(entry["subject"].split("_")[1]) - 1]
                print_success(f"{entry['day']} {entry['start']}-{entry['end']}: {subject_name}")
            else:
                print_error(f"Failed to create timetable entry for {entry['day']}", response.text)
        except Exception as e:
            print_error(f"Error creating timetable entry", str(e))
    
    print_info(f"Total timetable entries created: {created_count}/15")
    return created_count

def test_get_endpoints(students: Dict[str, int], teachers: Dict[str, int], classes: Dict[str, int]):
    """Test GET endpoints"""
    print_step("STEP 7: TEST GET ENDPOINTS")
    
    # Get class timetable
    print_info("Getting Class 10A full week timetable...")
    try:
        response = requests.get(
            f"{BASE_URL}/class-timetable/class/{classes['class_1']}",
            headers=get_headers()
        )
        if response.status_code == 200:
            print_success(f"Retrieved {len(response.json())} timetable entries for Class 10A")
        else:
            print_error("Failed to get class timetable", response.text)
    except Exception as e:
        print_error("Error getting class timetable", str(e))
    
    # Get teacher timetable
    print_info("Getting Teacher 1 (Rajesh) full week schedule...")
    try:
        response = requests.get(
            f"{BASE_URL}/teacher-timetable/teacher/{teachers['teacher_1']}",
            headers=get_headers()
        )
        if response.status_code == 200:
            print_success(f"Retrieved {len(response.json())} classes for Teacher 1")
        else:
            print_error("Failed to get teacher timetable", response.text)
    except Exception as e:
        print_error("Error getting teacher timetable", str(e))
    
    # Get student timetable
    print_info("Getting Student 1 (Aarav) class schedule...")
    try:
        response = requests.get(
            f"{BASE_URL}/student-timetable/student/{students['student_1']}",
            headers=get_headers()
        )
        if response.status_code == 200:
            print_success(f"Retrieved {len(response.json())} classes for Student 1")
        else:
            print_error("Failed to get student timetable", response.text)
    except Exception as e:
        print_error("Error getting student timetable", str(e))
    
    # Get class students
    print_info("Getting all students in Class 10A...")
    try:
        response = requests.get(
            f"{BASE_URL}/classes/{classes['class_1']}/students",
            headers=get_headers()
        )
        if response.status_code == 200:
            print_success(f"Retrieved {len(response.json())} students in Class 10A")
        else:
            print_error("Failed to get class students", response.text)
    except Exception as e:
        print_error("Error getting class students", str(e))

def main():
    """Run all tests"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}  SCHOOL TIMETABLE - TEST DATA CREATION{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    # Login
    if not login():
        print_error("Cannot proceed without login")
        return
    
    # Create data in order
    teachers = create_teachers()
    if not teachers:
        return
    
    subjects = create_subjects(teachers)
    if not subjects:
        return
    
    students = create_students()
    if not students:
        return
    
    classes = create_classes()
    if not classes:
        return
    
    enrollments = enroll_students(students, classes)
    if not enrollments:
        return
    
    created_entries = create_timetable(classes, subjects, teachers)
    if created_entries == 0:
        return
    
    # Test GET endpoints
    test_get_endpoints(students, teachers, classes)
    
    # Summary
    print_step("SUMMARY")
    print(f"{GREEN}✓ Successfully created:{RESET}")
    print(f"  - {len(teachers)} Teachers")
    print(f"  - {len(subjects)} Subjects")
    print(f"  - {len(students)} Students")
    print(f"  - {len(classes)} Classes")
    print(f"  - {len(enrollments)} Student Enrollments")
    print(f"  - {created_entries} Timetable Entries")
    print(f"\n{YELLOW}Now visit: http://localhost:8000/docs{RESET}")
    print(f"{YELLOW}Test the endpoints using Swagger UI!{RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}Interrupted by user{RESET}")
    except Exception as e:
        print(f"\n{RED}Unexpected error: {e}{RESET}")
