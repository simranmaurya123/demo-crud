# New Modules Implementation Plan

This document is only for the new features that need to be added to the existing FastAPI project.

The existing project already contains modules such as authentication, users, students, teachers, and student attendance. This file explains only the new tasks so that the AI or developer can continue the project without confusion.

---

## Current Project Pattern

The project follows this modular pattern:

```text
app/api/v1/<module_name>/
├── __init__.py
├── router.py
├── schemas.py
└── service.py
```

Each new module should follow the same structure.

Shared files already present in the project:

```text
app/api/deps.py        # Authentication and role-based dependencies
core/config.py         # Environment and project configuration
core/constants.py      # Fixed values such as roles and attendance statuses
core/security.py       # JWT and password security logic
db/models.py           # SQLAlchemy database models
db/session.py          # Database session dependency
db/base.py             # Model imports for table creation or migrations
utils/exceptions.py    # Custom exception handling
```

---

# New Modules to Add

The following new modules need to be added:

```text
subjects
timetable
teacher_attendance
```

Optional next module after these:

```text
dashboard
```

Recommended build order:

```text
1. Subjects
2. Timetable
3. Teacher Attendance
4. Dashboard
5. Tests and documentation updates
```

---

# 1. Subjects Module

## Purpose

The subjects module manages academic subjects such as Deep Neural Networks, DBMS, Operating System, Java, etc.

A subject may be assigned to a teacher.

---

## Folder to Create

```text
app/api/v1/subjects/
├── __init__.py
├── router.py
├── schemas.py
└── service.py
```

---

## Database Model

Add this model in `db/models.py`.

```python
class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    subject_code = Column(String, unique=True, nullable=False)
    subject_name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

---

## Pydantic Schemas

Create these in:

```text
app/api/v1/subjects/schemas.py
```

Required schemas:

```text
SubjectBase
SubjectCreate
SubjectUpdate
SubjectResponse
```

Suggested fields:

```text
subject_code: str
subject_name: str
description: Optional[str]
teacher_id: Optional[int]
```

---

## Service Functions

Create these in:

```text
app/api/v1/subjects/service.py
```

Required service functions:

```text
create_subject(db, subject_data)
get_all_subjects(db)
get_subject_by_id(db, subject_id)
update_subject(db, subject_id, subject_data)
delete_subject(db, subject_id)
get_subjects_by_teacher(db, teacher_id)
```

Important validation:

```text
Do not allow duplicate subject_code.
Return 404 if subject does not exist.
Return 400 if teacher_id is invalid, if validation is implemented.
```

---

## API Endpoints

Create these in:

```text
app/api/v1/subjects/router.py
```

Endpoints:

```text
POST    /api/v1/subjects/
GET     /api/v1/subjects/
GET     /api/v1/subjects/{subject_id}
PUT     /api/v1/subjects/{subject_id}
DELETE  /api/v1/subjects/{subject_id}
GET     /api/v1/subjects/teacher/{teacher_id}
```

---

## Role Access

Recommended permissions:

```text
Admin:
- Create subject
- Update subject
- Delete subject
- View all subjects

Teacher:
- View subjects assigned to them

Student:
- View subjects
```

---

# 2. Timetable Module

## Purpose

The timetable module manages class schedules.

A timetable entry connects:

```text
class + section + subject + teacher + day + time + room
```

---

## Folder to Create

```text
app/api/v1/timetable/
├── __init__.py
├── router.py
├── schemas.py
└── service.py
```

---

## Database Model

Add this model in `db/models.py`.

```python
class Timetable(Base):
    __tablename__ = "timetable"

    id = Column(Integer, primary_key=True, index=True)

    class_name = Column(String, nullable=False)
    section = Column(String, nullable=True)

    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    day_of_week = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    room_no = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

---

## Pydantic Schemas

Create these in:

```text
app/api/v1/timetable/schemas.py
```

Required schemas:

```text
TimetableBase
TimetableCreate
TimetableUpdate
TimetableResponse
```

Suggested fields:

```text
class_name: str
section: Optional[str]
subject_id: int
teacher_id: int
day_of_week: str
start_time: time
end_time: time
room_no: Optional[str]
```

---

## Service Functions

Create these in:

```text
app/api/v1/timetable/service.py
```

Required service functions:

```text
create_timetable_entry(db, timetable_data)
get_all_timetable_entries(db)
get_timetable_by_id(db, timetable_id)
update_timetable_entry(db, timetable_id, timetable_data)
delete_timetable_entry(db, timetable_id)
get_timetable_by_teacher(db, teacher_id)
get_timetable_by_class(db, class_name)
get_timetable_by_day(db, day)
```

---

## Important Timetable Validation

Before creating or updating a timetable entry, check for conflicts.

Conflict logic:

```text
same day
AND time overlaps
AND same teacher OR same class OR same room
```

Time overlap condition:

```text
new_start_time < existing_end_time
AND
new_end_time > existing_start_time
```

Validation rules:

```text
1. A teacher cannot be assigned to two classes at the same time.
2. A class cannot have two subjects at the same time.
3. A room cannot be assigned to two classes at the same time.
4. start_time must be less than end_time.
5. day_of_week should be a valid day.
```

---

## API Endpoints

Create these in:

```text
app/api/v1/timetable/router.py
```

Endpoints:

```text
POST    /api/v1/timetable/
GET     /api/v1/timetable/
GET     /api/v1/timetable/{timetable_id}
PUT     /api/v1/timetable/{timetable_id}
DELETE  /api/v1/timetable/{timetable_id}
GET     /api/v1/timetable/teacher/{teacher_id}
GET     /api/v1/timetable/class/{class_name}
GET     /api/v1/timetable/day/{day}
```

---

## Role Access

Recommended permissions:

```text
Admin:
- Create timetable
- Update timetable
- Delete timetable
- View all timetable records

Teacher:
- View own timetable

Student:
- View class timetable
```

---

# 3. Teacher Attendance Module

## Purpose

The teacher attendance module tracks daily attendance of teachers.

It stores whether a teacher is present, absent, late, on leave, or half day.

---

## Folder to Create

```text
app/api/v1/teacher_attendance/
├── __init__.py
├── router.py
├── schemas.py
└── service.py
```

---

## Database Model

Add this model in `db/models.py`.

```python
class TeacherAttendance(Base):
    __tablename__ = "teacher_attendance"

    id = Column(Integer, primary_key=True, index=True)

    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    date = Column(Date, nullable=False)

    status = Column(String, nullable=False)
    check_in_time = Column(Time, nullable=True)
    check_out_time = Column(Time, nullable=True)

    remarks = Column(String, nullable=True)
    marked_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

Recommended unique rule:

```text
One teacher should have only one attendance record per date.
```

Optional SQLAlchemy constraint:

```python
UniqueConstraint("teacher_id", "date", name="unique_teacher_attendance_per_day")
```

---

## Pydantic Schemas

Create these in:

```text
app/api/v1/teacher_attendance/schemas.py
```

Required schemas:

```text
TeacherAttendanceBase
TeacherAttendanceCreate
TeacherAttendanceUpdate
TeacherAttendanceResponse
TeacherAttendanceReportResponse
```

Suggested fields:

```text
teacher_id: int
date: date
status: str
check_in_time: Optional[time]
check_out_time: Optional[time]
remarks: Optional[str]
marked_by: Optional[int]
```

---

## Service Functions

Create these in:

```text
app/api/v1/teacher_attendance/service.py
```

Required service functions:

```text
mark_teacher_attendance(db, attendance_data)
get_all_teacher_attendance(db)
get_teacher_attendance_by_id(db, attendance_id)
update_teacher_attendance(db, attendance_id, attendance_data)
delete_teacher_attendance(db, attendance_id)
get_attendance_by_teacher(db, teacher_id)
get_attendance_by_date(db, date)
get_monthly_teacher_attendance_report(db, teacher_id, month, year)
```

---

## Teacher Attendance Status Values

Add these in:

```text
core/constants.py
```

```python
TEACHER_ATTENDANCE_STATUS = [
    "present",
    "absent",
    "late",
    "on_leave",
    "half_day"
]
```

Validation rules:

```text
1. status must be one of the allowed values.
2. teacher_id must exist.
3. duplicate attendance for same teacher and same date should not be allowed.
4. check_out_time should not be earlier than check_in_time.
```

---

## API Endpoints

Create these in:

```text
app/api/v1/teacher_attendance/router.py
```

Endpoints:

```text
POST    /api/v1/teacher-attendance/
GET     /api/v1/teacher-attendance/
GET     /api/v1/teacher-attendance/{attendance_id}
PUT     /api/v1/teacher-attendance/{attendance_id}
DELETE  /api/v1/teacher-attendance/{attendance_id}
GET     /api/v1/teacher-attendance/teacher/{teacher_id}
GET     /api/v1/teacher-attendance/date/{date}
GET     /api/v1/teacher-attendance/report/{teacher_id}?month=5&year=2026
```

---

## Monthly Report Logic

The report endpoint should calculate:

```text
present_days
absent_days
late_days
leave_days
half_days
attendance_percentage
```

Suggested attendance percentage formula:

```text
attendance_percentage = present_days / total_marked_days * 100
```

Optional improved formula:

```text
attendance_percentage = (present_days + half_days * 0.5) / total_marked_days * 100
```

Example response:

```json
{
  "teacher_id": 1,
  "month": 5,
  "year": 2026,
  "present_days": 22,
  "absent_days": 2,
  "late_days": 3,
  "leave_days": 1,
  "half_days": 1,
  "attendance_percentage": 78.57
}
```

---

## Role Access

Recommended permissions:

```text
Admin:
- Mark teacher attendance
- Update teacher attendance
- Delete teacher attendance
- View all teacher attendance records
- View teacher attendance reports

Teacher:
- View own attendance
- View own monthly attendance report
```

---

# 4. Router Registration

After creating the new modules, register their routers in:

```text
app/main.py
```

Add imports:

```python
from app.api.v1.subjects.router import router as subjects_router
from app.api.v1.timetable.router import router as timetable_router
from app.api.v1.teacher_attendance.router import router as teacher_attendance_router
```

Add router registration:

```python
app.include_router(subjects_router, prefix="/api/v1/subjects", tags=["Subjects"])
app.include_router(timetable_router, prefix="/api/v1/timetable", tags=["Timetable"])
app.include_router(
    teacher_attendance_router,
    prefix="/api/v1/teacher-attendance",
    tags=["Teacher Attendance"]
)
```

---

# 5. Update db/base.py

If `db/base.py` imports all models, update it after adding the new models.

Example:

```python
from db.models import (
    User,
    Student,
    Teacher,
    Attendance,
    Subject,
    Timetable,
    TeacherAttendance,
)
```

Use the actual model names already present in the project.

---

# 6. Update core/constants.py

Add these constants if not already present:

```python
USER_ROLES = ["admin", "teacher", "student"]

DAYS_OF_WEEK = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
]

TEACHER_ATTENDANCE_STATUS = [
    "present",
    "absent",
    "late",
    "on_leave",
    "half_day"
]
```

Optional student attendance status:

```python
STUDENT_ATTENDANCE_STATUS = [
    "present",
    "absent",
    "late",
    "leave"
]
```

---

# 7. Authentication and Role Dependencies

Use the existing `app/api/deps.py` file for authentication and role-based access.

Expected dependency functions:

```text
get_current_user
get_current_admin
get_current_teacher
get_current_student
```

If these do not exist, create them.

Recommended route protection:

```text
Create/update/delete subjects      -> Admin only
Create/update/delete timetable     -> Admin only
Mark teacher attendance            -> Admin only
View own teacher timetable         -> Teacher
View class timetable               -> Student
View own teacher attendance        -> Teacher
```

---

# 8. Optional Dashboard Module

After the three main modules are complete, add dashboard APIs.

## Folder to Create

```text
app/api/v1/dashboard/
├── __init__.py
├── router.py
├── schemas.py
└── service.py
```

---

## Suggested Endpoints

```text
GET /api/v1/dashboard/admin
GET /api/v1/dashboard/teacher
GET /api/v1/dashboard/student
```

---

## Admin Dashboard Response

```json
{
  "total_students": 120,
  "total_teachers": 15,
  "total_subjects": 8,
  "today_student_attendance_percentage": 87.5,
  "today_teacher_attendance_percentage": 93.3
}
```

---

## Teacher Dashboard Response

```json
{
  "assigned_subjects": 3,
  "today_classes": 4,
  "monthly_attendance_percentage": 91.6
}
```

---

## Student Dashboard Response

```json
{
  "attendance_percentage": 82.5,
  "today_classes": 5,
  "next_class": "Deep Neural Networks"
}
```

---

# 9. Testing Checklist

After implementing the new modules, test in this order.

## Subjects Testing

```text
1. Create subject
2. Try creating duplicate subject_code
3. Get all subjects
4. Get subject by ID
5. Update subject
6. Delete subject
7. Get subjects by teacher_id
```

## Timetable Testing

```text
1. Create timetable entry
2. Try invalid start_time and end_time
3. Try teacher conflict at same time
4. Try class conflict at same time
5. Try room conflict at same time
6. Get timetable by teacher
7. Get timetable by class
8. Get timetable by day
9. Update timetable
10. Delete timetable
```

## Teacher Attendance Testing

```text
1. Mark teacher present
2. Mark teacher absent
3. Try duplicate attendance for same teacher and same date
4. Get attendance by teacher
5. Get attendance by date
6. Update attendance
7. Generate monthly report
8. Delete attendance record
```

---

# 10. Suggested Test Files

If the project currently only has `test_main.py`, new tests can either be added there or split into separate files.

Recommended test structure:

```text
tests/
├── test_subjects.py
├── test_timetable.py
└── test_teacher_attendance.py
```

---

# 11. Final API Summary

## Subjects

```text
POST    /api/v1/subjects/
GET     /api/v1/subjects/
GET     /api/v1/subjects/{subject_id}
PUT     /api/v1/subjects/{subject_id}
DELETE  /api/v1/subjects/{subject_id}
GET     /api/v1/subjects/teacher/{teacher_id}
```

## Timetable

```text
POST    /api/v1/timetable/
GET     /api/v1/timetable/
GET     /api/v1/timetable/{timetable_id}
PUT     /api/v1/timetable/{timetable_id}
DELETE  /api/v1/timetable/{timetable_id}
GET     /api/v1/timetable/teacher/{teacher_id}
GET     /api/v1/timetable/class/{class_name}
GET     /api/v1/timetable/day/{day}
```

## Teacher Attendance

```text
POST    /api/v1/teacher-attendance/
GET     /api/v1/teacher-attendance/
GET     /api/v1/teacher-attendance/{attendance_id}
PUT     /api/v1/teacher-attendance/{attendance_id}
DELETE  /api/v1/teacher-attendance/{attendance_id}
GET     /api/v1/teacher-attendance/teacher/{teacher_id}
GET     /api/v1/teacher-attendance/date/{date}
GET     /api/v1/teacher-attendance/report/{teacher_id}?month=5&year=2026
```

---

# 12. Important Notes for the AI/Developer

Do not change the existing architecture.

Follow the existing pattern:

```text
router.py   -> API routes
schemas.py  -> Pydantic request and response models
service.py  -> Business logic and database queries
```

Keep SQLAlchemy models in:

```text
db/models.py
```

Keep database session dependency in:

```text
db/session.py
```

Keep JWT and role dependencies in:

```text
app/api/deps.py
```

Keep constants in:

```text
core/constants.py
```

The correct implementation order is:

```text
subjects -> timetable -> teacher_attendance -> dashboard -> tests
```

