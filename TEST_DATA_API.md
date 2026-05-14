# 📋 Complete API Test Data - Copy & Paste Ready

## ⚠️ IMPORTANT - Do this FIRST:
Login to get a token:

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin@example.com",
    "password": "admin123"
  }'
```

You'll get a response like:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Copy the token and replace `YOUR_TOKEN_HERE` in all requests below**

---

## 1️⃣ CREATE TEACHERS

### Teacher 1 - Math Teacher
```bash
curl -X POST "http://localhost:8000/api/v1/teachers/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "first_name": "Rajesh",
    "last_name": "Kumar",
    "email": "rajesh.kumar@school.com",
    "age": 35
  }'
```
**Save the `teacher_id`: 1**

### Teacher 2 - English Teacher
```bash
curl -X POST "http://localhost:8000/api/v1/teachers/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "first_name": "Priya",
    "last_name": "Singh",
    "email": "priya.singh@school.com",
    "age": 32
  }'
```
**Save the `teacher_id`: 2**

### Teacher 3 - Science Teacher
```bash
curl -X POST "http://localhost:8000/api/v1/teachers/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "first_name": "Arjun",
    "last_name": "Patel",
    "email": "arjun.patel@school.com",
    "age": 40
  }'
```
**Save the `teacher_id`: 3**

---

## 2️⃣ CREATE SUBJECTS

### Subject 1 - Mathematics
```bash
curl -X POST "http://localhost:8000/api/v1/subjects/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "subject_code": "MATH101",
    "subject_name": "Mathematics",
    "description": "Advanced Mathematics for Grade 10",
    "teacher_id": 1
  }'
```
**Save the `subject_id`: 1**

### Subject 2 - English
```bash
curl -X POST "http://localhost:8000/api/v1/subjects/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "subject_code": "ENG101",
    "subject_name": "English",
    "description": "English Language and Literature",
    "teacher_id": 2
  }'
```
**Save the `subject_id`: 2**

### Subject 3 - Physics
```bash
curl -X POST "http://localhost:8000/api/v1/subjects/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "subject_code": "PHY101",
    "subject_name": "Physics",
    "description": "Physics Fundamentals",
    "teacher_id": 3
  }'
```
**Save the `subject_id`: 3**

### Subject 4 - Chemistry
```bash
curl -X POST "http://localhost:8000/api/v1/subjects/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "subject_code": "CHEM101",
    "subject_name": "Chemistry",
    "description": "Chemistry Basics",
    "teacher_id": 3
  }'
```
**Save the `subject_id`: 4**

---

## 3️⃣ CREATE STUDENTS

### Student 1
```bash
curl -X POST "http://localhost:8000/api/v1/students/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "first_name": "Aarav",
    "last_name": "Sharma",
    "email": "aarav.sharma@student.com",
    "age": 15
  }'
```
**Save the `student_id`: 1**

### Student 2
```bash
curl -X POST "http://localhost:8000/api/v1/students/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "first_name": "Ananya",
    "last_name": "Verma",
    "email": "ananya.verma@student.com",
    "age": 15
  }'
```
**Save the `student_id`: 2**

### Student 3
```bash
curl -X POST "http://localhost:8000/api/v1/students/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "first_name": "Rohan",
    "last_name": "Gupta",
    "email": "rohan.gupta@student.com",
    "age": 15
  }'
```
**Save the `student_id`: 3**

---

## 4️⃣ CREATE CLASSES

### Class 1 - Grade 10A (Science)
```bash
curl -X POST "http://localhost:8000/api/v1/classes/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "class_name": "10A",
    "grade_level": 10,
    "section": "Science",
    "room_number": "101"
  }'
```
**Save the `class_id`: 1**

### Class 2 - Grade 10B (Science)
```bash
curl -X POST "http://localhost:8000/api/v1/classes/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "class_name": "10B",
    "grade_level": 10,
    "section": "Science",
    "room_number": "102"
  }'
```
**Save the `class_id`: 2**

---

## 5️⃣ ENROLL STUDENTS TO CLASSES

### Enroll Aarav to Class 10A
```bash
curl -X POST "http://localhost:8000/api/v1/classes/enrollment/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "student_id": 1,
    "class_id": 1
  }'
```
**Save the `enrollment_id`: 1**

### Enroll Ananya to Class 10A
```bash
curl -X POST "http://localhost:8000/api/v1/classes/enrollment/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "student_id": 2,
    "class_id": 1
  }'
```
**Save the `enrollment_id`: 2**

### Enroll Rohan to Class 10B
```bash
curl -X POST "http://localhost:8000/api/v1/classes/enrollment/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "student_id": 3,
    "class_id": 2
  }'
```
**Save the `enrollment_id`: 3**

---

## 6️⃣ CREATE CLASS TIMETABLE (MAIN SCHEDULE)

### **Monday Class 10A**

#### Monday 09:00-10:00 - Mathematics
```bash
curl -X POST "http://localhost:8000/api/v1/class-timetable/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "class_id": 1,
    "subject_id": 1,
    "teacher_id": 1,
    "day_of_week": "Monday",
    "start_time": "09:00:00",
    "end_time": "10:00:00",
    "room_number": "101"
  }'
```

#### Monday 10:00-11:00 - English
```bash
curl -X POST "http://localhost:8000/api/v1/class-timetable/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "class_id": 1,
    "subject_id": 2,
    "teacher_id": 2,
    "day_of_week": "Monday",
    "start_time": "10:00:00",
    "end_time": "11:00:00",
    "room_number": "101"
  }'
```

#### Monday 11:00-12:00 - Physics
```bash
curl -X POST "http://localhost:8000/api/v1/class-timetable/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "class_id": 1,
    "subject_id": 3,
    "teacher_id": 3,
    "day_of_week": "Monday",
    "start_time": "11:00:00",
    "end_time": "12:00:00",
    "room_number": "Lab-A"
  }'
```

---

### **Tuesday Class 10A**

#### Tuesday 09:00-10:00 - Chemistry
```bash
curl -X POST "http://localhost:8000/api/v1/class-timetable/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "class_id": 1,
    "subject_id": 4,
    "teacher_id": 3,
    "day_of_week": "Tuesday",
    "start_time": "09:00:00",
    "end_time": "10:00:00",
    "room_number": "Lab-B"
  }'
```

#### Tuesday 10:00-11:00 - Mathematics
```bash
curl -X POST "http://localhost:8000/api/v1/class-timetable/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "class_id": 1,
    "subject_id": 1,
    "teacher_id": 1,
    "day_of_week": "Tuesday",
    "start_time": "10:00:00",
    "end_time": "11:00:00",
    "room_number": "101"
  }'
```

#### Tuesday 11:00-12:00 - English
```bash
curl -X POST "http://localhost:8000/api/v1/class-timetable/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "class_id": 1,
    "subject_id": 2,
    "teacher_id": 2,
    "day_of_week": "Tuesday",
    "start_time": "11:00:00",
    "end_time": "12:00:00",
    "room_number": "101"
  }'
```

---

### **Wednesday Class 10A**

#### Wednesday 09:00-10:00 - Physics
```bash
curl -X POST "http://localhost:8000/api/v1/class-timetable/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "class_id": 1,
    "subject_id": 3,
    "teacher_id": 3,
    "day_of_week": "Wednesday",
    "start_time": "09:00:00",
    "end_time": "10:00:00",
    "room_number": "Lab-A"
  }'
```

#### Wednesday 10:00-11:00 - English
```bash
curl -X POST "http://localhost:8000/api/v1/class-timetable/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "class_id": 1,
    "subject_id": 2,
    "teacher_id": 2,
    "day_of_week": "Wednesday",
    "start_time": "10:00:00",
    "end_time": "11:00:00",
    "room_number": "101"
  }'
```

#### Wednesday 11:00-12:00 - Mathematics
```bash
curl -X POST "http://localhost:8000/api/v1/class-timetable/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "class_id": 1,
    "subject_id": 1,
    "teacher_id": 1,
    "day_of_week": "Wednesday",
    "start_time": "11:00:00",
    "end_time": "12:00:00",
    "room_number": "101"
  }'
```

---

### **Thursday Class 10A**

#### Thursday 09:00-10:00 - English
```bash
curl -X POST "http://localhost:8000/api/v1/class-timetable/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "class_id": 1,
    "subject_id": 2,
    "teacher_id": 2,
    "day_of_week": "Thursday",
    "start_time": "09:00:00",
    "end_time": "10:00:00",
    "room_number": "101"
  }'
```

#### Thursday 10:00-11:00 - Chemistry
```bash
curl -X POST "http://localhost:8000/api/v1/class-timetable/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "class_id": 1,
    "subject_id": 4,
    "teacher_id": 3,
    "day_of_week": "Thursday",
    "start_time": "10:00:00",
    "end_time": "11:00:00",
    "room_number": "Lab-B"
  }'
```

#### Thursday 11:00-12:00 - Physics
```bash
curl -X POST "http://localhost:8000/api/v1/class-timetable/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "class_id": 1,
    "subject_id": 3,
    "teacher_id": 3,
    "day_of_week": "Thursday",
    "start_time": "11:00:00",
    "end_time": "12:00:00",
    "room_number": "Lab-A"
  }'
```

---

### **Friday Class 10A**

#### Friday 09:00-10:00 - Mathematics
```bash
curl -X POST "http://localhost:8000/api/v1/class-timetable/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "class_id": 1,
    "subject_id": 1,
    "teacher_id": 1,
    "day_of_week": "Friday",
    "start_time": "09:00:00",
    "end_time": "10:00:00",
    "room_number": "101"
  }'
```

#### Friday 10:00-11:00 - Physics
```bash
curl -X POST "http://localhost:8000/api/v1/class-timetable/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "class_id": 1,
    "subject_id": 3,
    "teacher_id": 3,
    "day_of_week": "Friday",
    "start_time": "10:00:00",
    "end_time": "11:00:00",
    "room_number": "Lab-A"
  }'
```

#### Friday 11:00-12:00 - English
```bash
curl -X POST "http://localhost:8000/api/v1/class-timetable/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "class_id": 1,
    "subject_id": 2,
    "teacher_id": 2,
    "day_of_week": "Friday",
    "start_time": "11:00:00",
    "end_time": "12:00:00",
    "room_number": "101"
  }'
```

---

## 7️⃣ VIEW/GET ENDPOINTS (Test Data Retrieval)

### Get All Classes
```bash
curl -X GET "http://localhost:8000/api/v1/classes/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get Specific Class (Class 10A)
```bash
curl -X GET "http://localhost:8000/api/v1/classes/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get All Students in Class 10A
```bash
curl -X GET "http://localhost:8000/api/v1/classes/1/students" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get Class 10A Timetable (Entire Week)
```bash
curl -X GET "http://localhost:8000/api/v1/class-timetable/class/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get Class 10A Timetable for Monday Only
```bash
curl -X GET "http://localhost:8000/api/v1/class-timetable/class/1/day/Monday" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get Teacher 1's (Rajesh) Full Weekly Schedule
```bash
curl -X GET "http://localhost:8000/api/v1/teacher-timetable/teacher/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get Teacher 1's Schedule for Monday Only
```bash
curl -X GET "http://localhost:8000/api/v1/teacher-timetable/teacher/1/day/Monday" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get Teacher 1's Classes for Class 10A Only
```bash
curl -X GET "http://localhost:8000/api/v1/teacher-timetable/teacher/1/class/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get Student 1's (Aarav) Full Weekly Schedule
```bash
curl -X GET "http://localhost:8000/api/v1/student-timetable/student/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get Student 1's Schedule for Monday Only
```bash
curl -X GET "http://localhost:8000/api/v1/student-timetable/student/1/day/Monday" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get All Teachers
```bash
curl -X GET "http://localhost:8000/api/v1/teachers/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get All Students
```bash
curl -X GET "http://localhost:8000/api/v1/students/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get All Subjects
```bash
curl -X GET "http://localhost:8000/api/v1/subjects/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 8️⃣ UPDATE ENDPOINT EXAMPLE

### Update Class 10A Room Number
```bash
curl -X PUT "http://localhost:8000/api/v1/classes/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "room_number": "103"
  }'
```

### Update a Timetable Entry (Move Monday 09:00 Math to 08:00)
```bash
curl -X PUT "http://localhost:8000/api/v1/class-timetable/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "start_time": "08:00:00",
    "end_time": "09:00:00"
  }'
```

---

## 9️⃣ DELETE ENDPOINT EXAMPLE

### Remove Student from Class (Remove Aarav from 10A)
```bash
curl -X DELETE "http://localhost:8000/api/v1/classes/enrollment/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Delete a Timetable Entry
```bash
curl -X DELETE "http://localhost:8000/api/v1/class-timetable/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📊 Data Relationship Summary

```
Teachers (3):
├── Teacher 1: Rajesh (Math)
├── Teacher 2: Priya (English)
└── Teacher 3: Arjun (Science & Chemistry)

Subjects (4):
├── Subject 1: Mathematics → Teacher 1
├── Subject 2: English → Teacher 2
├── Subject 3: Physics → Teacher 3
└── Subject 4: Chemistry → Teacher 3

Students (3):
├── Student 1: Aarav → Enrolled in Class 10A
├── Student 2: Ananya → Enrolled in Class 10A
└── Student 3: Rohan → Enrolled in Class 10B

Classes (2):
├── Class 10A (Room 101) - 2 Students
└── Class 10B (Room 102) - 1 Student

Class 10A Timetable (Mon-Fri, 3 hours/day):
├── Monday: Math, English, Physics
├── Tuesday: Chemistry, Math, English
├── Wednesday: Physics, English, Math
├── Thursday: English, Chemistry, Physics
└── Friday: Math, Physics, English
```

---

## 💡 Quick Test Flow

1. **Login** → Get token
2. **Create 3 Teachers**
3. **Create 4 Subjects** (linked to teachers)
4. **Create 3 Students**
5. **Create 2 Classes**
6. **Enroll 3 Students** to classes
7. **Create 17 Timetable Entries** (class schedule for 5 days)
8. **Test GET Endpoints** to view timetables
9. **Test UPDATE** to modify entries
10. **Test DELETE** to remove entries

Enjoy! 🎉
