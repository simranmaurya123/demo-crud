from sqlalchemy import Boolean, Column, DateTime, Integer, String, func, Date, ForeignKey, Time
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(100), unique=True)
    age = Column(Integer)
    password_hash = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Teacher(Base):
    __tablename__ = "teachers"
    
    teacher_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(100), unique=True)
    age = Column(Integer)
    password_hash = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Student(Base):
    __tablename__ = "students"
    
    student_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(100), unique=True)
    age = Column(Integer)
    password_hash = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Attendance(Base):
    __tablename__ = "attendance"
    
    attendance_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.teacher_id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)  # "present" or "absent"
    remarks = Column(String(255), nullable=True)  # Optional notes
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Subject(Base):
    __tablename__ = "subjects"
    
    subject_id = Column(Integer, primary_key=True, index=True)
    subject_code = Column(String(50), unique=True, nullable=False)
    subject_name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    teacher_id = Column(Integer, ForeignKey("teachers.teacher_id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Class(Base):
    """Represents a class/section (e.g., 10A, 10B)"""
    __tablename__ = "classes"
    
    class_id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String(50), nullable=False)  # e.g., "10A"
    section = Column(String(50), nullable=True)  # Optional: "Science", "Commerce"
    grade_level = Column(Integer, nullable=False)  # 10, 11, 12, etc.
    room_number = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class StudentEnrollment(Base):
    """Links students to their class"""
    __tablename__ = "student_enrollment"
    
    enrollment_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.class_id"), nullable=False)
    enrollment_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class ClassTimetable(Base):
    """Main timetable - one entry per class subject slot per week"""
    __tablename__ = "class_timetable"
    
    timetable_id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.class_id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.subject_id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.teacher_id"), nullable=False)
    day_of_week = Column(String(20), nullable=False)  # "Monday", "Tuesday", etc.
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    room_number = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
