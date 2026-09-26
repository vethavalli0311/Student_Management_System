# Student Management System (EduTrack Pro)

> **Full Stack Academic Operations & Analytics Platform**  
> Developed using **HTML5, CSS3, JavaScript, Python, Flask, and MySQL**.  
> Inspired by S. Vethavalli's portfolio projects: *Student Performance Tracker* and *Data Insights Dashboard*.

---

## 🌟 Key Highlights & Features

1. **Executive Operations Dashboard**:
   - Live KPI cards: Total Enrolled Students, Overall Pass Rate, Average Attendance, Active Academic Courses.
   - Interactive overview charts: Department Enrollment and Grade Breakdown.
   - Real-time ranking of top academic performers and recent evaluation activities.

2. **Complete Student Records Management (CRUD)**:
   - Full student directory with pagination and live search (by Roll No, Name, Email).
   - Department filtering (Computer Applications, Data Science, IT, Mathematics).
   - Enroll new students, edit existing student profiles, and safely delete records.

3. **Academic Performance & Marks Tracker**:
   - Record internal (max 25) and external examination marks (max 75).
   - Automated grade computation (O, A+, A, B+, B, C, F) and PASS/FAIL classification based on university standards.

4. **Visual Analytics & Insights (Chart.js)**:
   - Grade Distribution curve.
   - Subject-wise Mean Performance benchmark.
   - Department Enrollment share (doughnut chart).
   - Pass vs Fail cohort ratio.

5. **Report Export**:
   - 1-Click export of complete student performance records to `.csv` format for Microsoft Excel or Power BI integration.

6. **Dual Database Architecture (MySQL + Auto-Fallback)**:
   - Out-of-the-box support for MySQL (`student_management_db`).
   - If MySQL credentials have not been configured yet, the system automatically falls back to local SQLite with full seed data so you can test it instantly without setup roadblocks!

---

## 📁 Project Structure

```text
student-management-system/
├── app.py                # Main Flask application with routes and API endpoints
├── config.py             # Database configuration with MySQL auto-connection
├── models.py             # SQLAlchemy models (Student, Course, Mark, Attendance)
├── schema.sql            # Native MySQL schema & seed data SQL script
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation and instructions
├── static/
│   ├── css/
│   │   └── style.css     # Responsive glassmorphism styling & themes
│   └── js/
│       └── main.js       # Dynamic search, modals, and Chart.js integrations
└── templates/
    ├── base.html         # Base template with sidebar, navbar, and theme toggle
    ├── index.html        # Dashboard with KPI cards and overview charts
    ├── students.html     # Student directory with search, filter, and CRUD modals
    ├── performance.html  # Marks entry and grade evaluation table
    └── analytics.html    # Deep-dive interactive data visualization charts
```

---

## 🚀 How to Run the Application

### Step 1: Start the Flask App
Open PowerShell or your terminal in this directory:

```powershell
cd C:\Users\HP\.gemini\antigravity\scratch\student-management-system
python app.py
```

### Step 2: Open in Your Browser
Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 🗄️ Connecting to your MySQL Server

To connect the application directly to your local MySQL database:
1. Open `config.py` (or set environment variables):
   ```python
   MYSQL_HOST = 'localhost'
   MYSQL_USER = 'root'
   MYSQL_PASSWORD = 'YOUR_MYSQL_PASSWORD'  # <--- Enter your MySQL root password here
   MYSQL_DB = 'student_management_db'
   ```
2. You can also import `schema.sql` directly into MySQL Workbench or via command line:
   ```bash
   mysql -u root -p < schema.sql
   ```
3. Restart `python app.py`. The top bar badge will display: **`🟢 Database: MySQL Database (student_management_db)`**.
