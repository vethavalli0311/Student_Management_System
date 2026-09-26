from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def compute_grade(total):
    if total >= 90:
        return 'O', 'PASS'
    elif total >= 80:
        return 'A+', 'PASS'
    elif total >= 70:
        return 'A', 'PASS'
    elif total >= 60:
        return 'B+', 'PASS'
    elif total >= 50:
        return 'B', 'PASS'
    elif total >= 40:
        return 'C', 'PASS'
    else:
        return 'F', 'FAIL'

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String(20), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.Integer, default=1, nullable=False)
    gender = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    marks = db.relationship('Mark', backref='student', cascade='all, delete-orphan', lazy=True)
    attendance = db.relationship('Attendance', backref='student', uselist=False, cascade='all, delete-orphan', lazy=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def average_score(self):
        if not self.marks:
            return 0.0
        return round(sum(m.total_marks for m in self.marks) / len(self.marks), 2)

    @property
    def overall_status(self):
        if not self.marks:
            return 'ENROLLED'
        has_failed = any(m.status == 'FAIL' for m in self.marks)
        return 'FAIL' if has_failed else 'PASS'

    def to_dict(self):
        return {
            'id': self.id,
            'roll_no': self.roll_no,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'department': self.department,
            'semester': self.semester,
            'gender': self.gender,
            'average_score': self.average_score,
            'overall_status': self.overall_status,
            'attendance_pct': self.attendance.percentage if self.attendance else None
        }


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    course_name = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, default=3, nullable=False)
    department = db.Column(db.String(50), nullable=False)

    marks = db.relationship('Mark', backref='course', cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'course_code': self.course_code,
            'course_name': self.course_name,
            'credits': self.credits,
            'department': self.department
        }


class Mark(db.Model):
    __tablename__ = 'marks'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    course_code = db.Column(db.String(20), db.ForeignKey('courses.course_code', ondelete='CASCADE'), nullable=False)
    semester = db.Column(db.Integer, default=1, nullable=False)
    internal_marks = db.Column(db.Float, default=0.0, nullable=False)
    external_marks = db.Column(db.Float, default=0.0, nullable=False)
    total_marks = db.Column(db.Float, default=0.0, nullable=False)
    grade = db.Column(db.String(5))
    status = db.Column(db.String(10), default='PASS')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def calculate_results(self):
        self.total_marks = round(self.internal_marks + self.external_marks, 2)
        self.grade, self.status = compute_grade(self.total_marks)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student.full_name if self.student else None,
            'student_roll': self.student.roll_no if self.student else None,
            'course_code': self.course_code,
            'course_name': self.course.course_name if self.course else None,
            'semester': self.semester,
            'internal_marks': self.internal_marks,
            'external_marks': self.external_marks,
            'total_marks': self.total_marks,
            'grade': self.grade,
            'status': self.status
        }


class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), unique=True, nullable=False)
    total_classes = db.Column(db.Integer, default=100, nullable=False)
    attended_classes = db.Column(db.Integer, default=85, nullable=False)
    percentage = db.Column(db.Float, default=85.0, nullable=False)

    def calculate_percentage(self):
        if self.total_classes > 0:
            self.percentage = round((self.attended_classes / self.total_classes) * 100, 2)
        else:
            self.percentage = 0.0

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'total_classes': self.total_classes,
            'attended_classes': self.attended_classes,
            'percentage': self.percentage
        }
