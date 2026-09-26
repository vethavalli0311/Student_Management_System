import csv
import io
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
from config import Config
from models import db, Student, Course, Mark, Attendance, compute_grade

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# ------------------------------------------------------------------------------
# Database Initialization & Sample Data Seeder
# ------------------------------------------------------------------------------
def seed_initial_data():
    with app.app_context():
        db.create_all()
        # Check if courses already exist
        if Course.query.count() == 0:
            sample_courses = [
                Course(course_code='CS101', course_name='Python Programming & Scripting', credits=4, department='Computer Applications'),
                Course(course_code='CS102', course_name='Relational Database Systems & MySQL', credits=4, department='Computer Applications'),
                Course(course_code='CS103', course_name='Web Technologies (HTML, CSS, JS)', credits=3, department='Computer Applications'),
                Course(course_code='CS104', course_name='C Language & Data Structures', credits=4, department='Computer Applications'),
                Course(course_code='DS201', course_name='Data Analytics & Power BI', credits=3, department='Data Science')
            ]
            db.session.add_all(sample_courses)
            db.session.commit()

        # Check if students already exist
        if Student.query.count() == 0:
            sample_students = [
                Student(roll_no='2025MCA001', first_name='Aarav', last_name='Sharma', email='aarav.sharma@example.com', phone='+91 9876543210', department='Computer Applications', semester=1, gender='Male'),
                Student(roll_no='2025MCA002', first_name='Priya', last_name='Sundaram', email='priya.sundaram@example.com', phone='+91 9876543211', department='Computer Applications', semester=1, gender='Female'),
                Student(roll_no='2025MCA003', first_name='Karthik', last_name='Raman', email='karthik.raman@example.com', phone='+91 9876543212', department='Computer Applications', semester=1, gender='Male'),
                Student(roll_no='2025MCA004', first_name='Deepika', last_name='Natarajan', email='deepika.n@example.com', phone='+91 9876543213', department='Data Science', semester=1, gender='Female'),
                Student(roll_no='2025MCA005', first_name='Vikram', last_name='Aditya', email='vikram.aditya@example.com', phone='+91 9876543214', department='Computer Applications', semester=1, gender='Male'),
                Student(roll_no='2025MCA006', first_name='Ananya', last_name='Iyer', email='ananya.iyer@example.com', phone='+91 9876543215', department='Data Science', semester=1, gender='Female')
            ]
            db.session.add_all(sample_students)
            db.session.commit()

            # Seed Marks
            marks_data = [
                (1, 'CS101', 1, 23.0, 68.0),
                (1, 'CS102', 1, 24.0, 70.0),
                (2, 'CS101', 1, 25.0, 72.0),
                (2, 'CS102', 1, 22.0, 65.0),
                (3, 'CS101', 1, 18.0, 50.0),
                (3, 'CS102', 1, 19.0, 54.0),
                (4, 'DS201', 1, 24.0, 71.0),
                (5, 'CS101', 1, 12.0, 24.0),
                (6, 'DS201', 1, 22.0, 64.0),
            ]
            for sid, code, sem, internal, external in marks_data:
                m = Mark(student_id=sid, course_code=code, semester=sem, internal_marks=internal, external_marks=external)
                m.calculate_results()
                db.session.add(m)

            # Seed Attendance
            attendance_data = [
                (1, 100, 94),
                (2, 100, 96),
                (3, 100, 84),
                (4, 100, 95),
                (5, 100, 68),
                (6, 100, 90),
            ]
            for sid, tot, att in attendance_data:
                a = Attendance(student_id=sid, total_classes=tot, attended_classes=att)
                a.calculate_percentage()
                db.session.add(a)

            db.session.commit()

# ------------------------------------------------------------------------------
# Context Processors
# ------------------------------------------------------------------------------
@app.context_processor
def inject_global_data():
    return {
        'db_status': Config.DB_STATUS_LABEL,
        'is_mysql': Config.DB_CONNECTED_MYSQL
    }

# ------------------------------------------------------------------------------
# Web Routes: Dashboard
# ------------------------------------------------------------------------------
@app.route('/')
def dashboard():
    total_students = Student.query.count()
    total_courses = Course.query.count()
    all_marks = Mark.query.all()
    
    pass_count = sum(1 for m in all_marks if m.status == 'PASS')
    total_evals = len(all_marks)
    pass_rate = round((pass_count / total_evals * 100), 1) if total_evals > 0 else 0.0

    all_attendances = Attendance.query.all()
    avg_attendance = round(sum(a.percentage for a in all_attendances) / len(all_attendances), 1) if all_attendances else 0.0

    # Top performing students
    students = Student.query.all()
    top_students = sorted(students, key=lambda s: s.average_score, reverse=True)[:5]
    
    # Recent performance entries
    recent_marks = Mark.query.order_by(Mark.id.desc()).limit(6).all()

    return render_template(
        'index.html',
        total_students=total_students,
        total_courses=total_courses,
        pass_rate=pass_rate,
        avg_attendance=avg_attendance,
        top_students=top_students,
        recent_marks=recent_marks
    )

# ------------------------------------------------------------------------------
# Web Routes: Students Directory (CRUD)
# ------------------------------------------------------------------------------
@app.route('/students')
def students():
    search = request.args.get('search', '').strip()
    dept = request.args.get('dept', '').strip()

    query = Student.query
    if search:
        query = query.filter(
            (Student.roll_no.ilike(f"%{search}%")) |
            (Student.first_name.ilike(f"%{search}%")) |
            (Student.last_name.ilike(f"%{search}%")) |
            (Student.email.ilike(f"%{search}%"))
        )
    if dept:
        query = query.filter(Student.department == dept)

    students_list = query.order_by(Student.roll_no).all()
    departments = [d[0] for d in db.session.query(Student.department).distinct().all()]

    return render_template(
        'students.html',
        students=students_list,
        departments=departments,
        search=search,
        selected_dept=dept
    )

@app.route('/students/add', methods=['POST'])
def add_student():
    roll_no = request.form.get('roll_no', '').strip()
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    department = request.form.get('department', '').strip()
    semester = int(request.form.get('semester', 1))
    gender = request.form.get('gender', 'Other')

    if not roll_no or not first_name or not email or not department:
        flash('Roll No, First Name, Email, and Department are required.', 'error')
        return redirect(url_for('students'))

    # Check for duplicate roll_no or email
    if Student.query.filter_by(roll_no=roll_no).first():
        flash(f'Student with Roll No {roll_no} already exists.', 'error')
        return redirect(url_for('students'))

    if Student.query.filter_by(email=email).first():
        flash(f'Student with Email {email} already exists.', 'error')
        return redirect(url_for('students'))

    try:
        new_student = Student(
            roll_no=roll_no,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            department=department,
            semester=semester,
            gender=gender
        )
        db.session.add(new_student)
        db.session.flush()

        # Create default attendance record
        att = Attendance(student_id=new_student.id, total_classes=100, attended_classes=85)
        att.calculate_percentage()
        db.session.add(att)

        db.session.commit()
        flash(f'Student {first_name} {last_name} ({roll_no}) enrolled successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding student: {str(e)}', 'error')

    return redirect(url_for('students'))

@app.route('/students/edit/<int:id>', methods=['POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    student.first_name = request.form.get('first_name', student.first_name).strip()
    student.last_name = request.form.get('last_name', student.last_name).strip()
    student.phone = request.form.get('phone', student.phone).strip()
    student.department = request.form.get('department', student.department).strip()
    student.semester = int(request.form.get('semester', student.semester))
    student.gender = request.form.get('gender', student.gender)

    try:
        db.session.commit()
        flash(f'Updated details for {student.full_name} ({student.roll_no})', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating student: {str(e)}', 'error')

    return redirect(url_for('students'))

@app.route('/students/delete/<int:id>', methods=['POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    roll = student.roll_no
    name = student.full_name
    try:
        db.session.delete(student)
        db.session.commit()
        flash(f'Student {name} ({roll}) removed from the system.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting student: {str(e)}', 'error')

    return redirect(url_for('students'))

# ------------------------------------------------------------------------------
# Web Routes: Performance & Marks Management
# ------------------------------------------------------------------------------
@app.route('/performance')
def performance():
    selected_course = request.args.get('course', '').strip()
    query = Mark.query

    if selected_course:
        query = query.filter(Mark.course_code == selected_course)

    marks_list = query.order_by(Mark.id.desc()).all()
    courses = Course.query.order_by(Course.course_code).all()
    students = Student.query.order_by(Student.first_name).all()

    return render_template(
        'performance.html',
        marks=marks_list,
        courses=courses,
        students=students,
        selected_course=selected_course
    )

@app.route('/performance/add', methods=['POST'])
def add_mark():
    student_id = int(request.form.get('student_id'))
    course_code = request.form.get('course_code')
    semester = int(request.form.get('semester', 1))
    internal = float(request.form.get('internal_marks', 0.0))
    external = float(request.form.get('external_marks', 0.0))

    if internal > 25 or internal < 0 or external > 75 or external < 0:
        flash('Invalid marks! Internal max: 25, External max: 75.', 'error')
        return redirect(url_for('performance'))

    try:
        # Check if mark record already exists for this student & course
        existing = Mark.query.filter_by(student_id=student_id, course_code=course_code, semester=semester).first()
        if existing:
            existing.internal_marks = internal
            existing.external_marks = external
            existing.calculate_results()
            flash('Updated existing marks record for student.', 'success')
        else:
            m = Mark(
                student_id=student_id,
                course_code=course_code,
                semester=semester,
                internal_marks=internal,
                external_marks=external
            )
            m.calculate_results()
            db.session.add(m)
            flash('Recorded new marks and calculated grade.', 'success')

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f'Error saving performance record: {str(e)}', 'error')

    return redirect(url_for('performance'))

@app.route('/performance/delete/<int:id>', methods=['POST'])
def delete_mark(id):
    mark = Mark.query.get_or_404(id)
    try:
        db.session.delete(mark)
        db.session.commit()
        flash('Performance evaluation record deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting record: {str(e)}', 'error')
    return redirect(url_for('performance'))

# ------------------------------------------------------------------------------
# Web Routes: Analytics & Insights Dashboard
# ------------------------------------------------------------------------------
@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/api/analytics-data')
def analytics_data():
    # 1. Department Distribution
    dept_counts = {}
    for s in Student.query.all():
        dept_counts[s.department] = dept_counts.get(s.department, 0) + 1

    # 2. Grade Distribution
    grade_counts = {'O': 0, 'A+': 0, 'A': 0, 'B+': 0, 'B': 0, 'C': 0, 'F': 0}
    for m in Mark.query.all():
        if m.grade in grade_counts:
            grade_counts[m.grade] += 1

    # 3. Subject-wise Average Scores
    courses = Course.query.all()
    subject_averages = {}
    for c in courses:
        course_marks = [m.total_marks for m in c.marks]
        avg = round(sum(course_marks) / len(course_marks), 2) if course_marks else 0.0
        subject_averages[c.course_name] = avg

    # 4. Pass vs Fail Ratio
    all_marks = Mark.query.all()
    pass_cnt = sum(1 for m in all_marks if m.status == 'PASS')
    fail_cnt = sum(1 for m in all_marks if m.status == 'FAIL')

    return jsonify({
        'departments': {
            'labels': list(dept_counts.keys()),
            'data': list(dept_counts.values())
        },
        'grades': {
            'labels': list(grade_counts.keys()),
            'data': list(grade_counts.values())
        },
        'subjects': {
            'labels': list(subject_averages.keys()),
            'data': list(subject_averages.values())
        },
        'pass_fail': {
            'labels': ['Passed Evaluations', 'Failed Evaluations'],
            'data': [pass_cnt, fail_cnt]
        }
    })

# ------------------------------------------------------------------------------
# Web Routes: Report Export (CSV)
# ------------------------------------------------------------------------------
@app.route('/export/csv')
def export_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'Student ID', 'Roll No', 'Full Name', 'Department', 'Semester',
        'Course Code', 'Course Name', 'Internal (25)', 'External (75)', 'Total (100)', 'Grade', 'Status'
    ])

    marks = Mark.query.join(Student).order_by(Student.roll_no).all()
    for m in marks:
        writer.writerow([
            m.student.id,
            m.student.roll_no,
            m.student.full_name,
            m.student.department,
            m.semester,
            m.course_code,
            m.course.course_name if m.course else '',
            m.internal_marks,
            m.external_marks,
            m.total_marks,
            m.grade,
            m.status
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=student_performance_report.csv"}
    )

# ------------------------------------------------------------------------------
# Main Entry Point
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    seed_initial_data()
    print("\n" + "=" * 60)
    print(" S. VETHAVALLI - STUDENT MANAGEMENT SYSTEM")
    print(f" Database: {Config.DB_STATUS_LABEL}")
    print(" Access Web App: http://127.0.0.1:5000")
    print("=" * 60 + "\n")
    app.run(debug=True, port=5000)
