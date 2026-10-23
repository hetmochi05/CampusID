import zipfile
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, os
import qrcode
import pandas as pd
from PIL import Image
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from reportlab.pdfgen import canvas
import pandas as pd
from io import BytesIO
from flask import send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import openpyxl
import uuid
import shutil
from werkzeug.utils import secure_filename






# ---------------- APP CONFIG ----------------
app = Flask(__name__)
app.secret_key = "student_id_card_secret"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def get_db():
    conn = sqlite3.connect(
        'students.db',
        timeout=30,          # wait for lock
        check_same_thread=False
    )
    conn.execute("PRAGMA journal_mode=WAL;")  # allow concurrent reads
    return conn


# ---------------- LOGIN REQUIRED ----------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

# ---------------- DATABASE INIT ----------------
def get_db():
    return sqlite3.connect('students.db')

conn = get_db()
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS admin(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT UNIQUE,
    name TEXT,
    course TEXT,
    photo TEXT,
    qr TEXT
)
""")

# Default admin
c.execute("SELECT * FROM admin")
if not c.fetchone():
    c.execute(
        "INSERT INTO admin(username,password) VALUES(?,?)",
        ("admin", generate_password_hash("admin123"))
    )

conn.commit()
conn.close() 

# ---------------- ROUTES ----------------
@app.route('/')
def home():
    return redirect('/login')

# ---------- LOGIN ----------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM admin WHERE username=?", (username,))
        admin = c.fetchone()
        conn.close()

        if admin and check_password_hash(admin[2], password):
            session['admin'] = username
            return redirect('/admin')

        return render_template('login.html', error="Invalid login")

    return render_template('login.html')

# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------- ADMIN DASHBOARD (No Pagination) ----------
@app.route('/admin')
@login_required
def admin():
    search = request.args.get('search', '')

    conn = get_db()
    c = conn.cursor()

    if search:
        c.execute("""
            SELECT * FROM students
            WHERE student_id LIKE ?
            OR name LIKE ?
            OR course LIKE ?
            ORDER BY id DESC
        """, (f"%{search}%", f"%{search}%", f"%{search}%"))
    else:
        c.execute("SELECT * FROM students ORDER BY id DESC")

    students = c.fetchall()
    
    # Dashboard stats
    c.execute("SELECT COUNT(*) FROM students")
    total_students = c.fetchone()[0]

    c.execute("SELECT COUNT(DISTINCT course) FROM students")
    total_courses = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM students WHERE status='Active'")
    active_students = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM students WHERE status='Inactive'")
    inactive_students = c.fetchone()[0]

    
    conn.close()

    return render_template(
        'admin.html',
        students=students,
        search=search,
        total_students=total_students,
        total_courses=total_courses,
        active_students=active_students,
        inactive_students=inactive_students

    )

# ---------- REGISTER STUDENT ----------
@app.route('/register', methods=['GET','POST'])
@login_required
def register():
    if request.method == 'POST':
        name = request.form['name']
        course = request.form['course']
        photo = request.files['photo']

        student_id = "STU" + datetime.now().strftime("%Y%m%d") + str(uuid.uuid4().int)[:6]

        photo_name = student_id + "_" + photo.filename
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_name)
        photo.save(photo_path)

        qr_link = f"http://127.0.0.1:5000/verify/{student_id}"
        qr_img = qrcode.make(qr_link)
        qr_name = student_id + "_qr.png"
        qr_img.save(os.path.join(app.config['UPLOAD_FOLDER'], qr_name))
        
        dob = request.form['dob']
        contact = request.form['contact']
        email = request.form['email']
        blood_group = request.form['blood_group']
        address = request.form['address']


        conn = get_db()
        c = conn.cursor()
        c.execute("""
            INSERT INTO students(student_id, name, course, photo, qr, dob, contact, email, blood_group, address) VALUES (?,?,?,?,?,?,?,?,?,?)
            """, (student_id, name, course, photo_name, qr_name,dob, contact, email, blood_group, address))

        conn.commit()
        conn.close()

        # return redirect("/admin")  # No pagination, just go to admin
        return render_template('success.html', student_id=student_id)

    return render_template('register.html')

# ---------- ID CARD ----------
@app.route('/id/<sid>')
def id_card(sid):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE student_id=?", (sid,))
    student = c.fetchone()
    conn.close()

    if not student:
        return "Invalid ID"

    return render_template('id_card.html', student=student)

# ---------- VERIFY ----------
@app.route('/verify/<sid>')
def verify(sid):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE student_id=?", (sid,))
    student = c.fetchone()
    conn.close()

    if not student:
        return "<h2 style='color:red; text-align:center;'>Invalid Student ID</h2>"

    # # student[6] = status column
    # if student[6] == "Inactive":
    #     return """
    #     <h2 style='color:red; text-align:center; margin-top:50px;'>
    #         ❌ This Student ID is no longer valid
    #     </h2>
    #     """

    return render_template('verify.html', student=student)

# ---------- DELETE ----------
@app.route('/delete/<int:id>')
@login_required
def delete_student(id):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/admin')




# ---------- EDIT STUDENT ----------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    conn = get_db()
    c = conn.cursor()
    
    # Fetch student data
    c.execute("SELECT * FROM students WHERE id=?", (id,))
    student = c.fetchone()

    if not student:
        conn.close()
        return "Student not found"

    if request.method == 'POST':
        name = request.form['name']
        course = request.form['course']
        dob = request.form['dob']
        contact = request.form['contact']
        email = request.form['email']
        blood_group = request.form['blood_group']
        address = request.form['address']

        #Update photo if uploaded
        photo = request.files.get('photo')
        if photo:
            photo_name = student[1] + "_" + photo.filename
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_name)
            photo.save(photo_path)
            c.execute("UPDATE students SET name=?, course=?, photo=?, dob=?, contact=?, email=?, blood_group=?, address=? WHERE id=?",
                      (name, course, photo_name, dob, contact, email, blood_group, address, id))
        else:
            c.execute("UPDATE students SET name=?, course=?,dob=?,contact=?,email=?,blood_group=?,address=? WHERE id=?",
                      (name, course, dob, contact, email, blood_group, address, id))

        conn.commit()
        conn.close()
        return redirect('/admin')

    conn.close()
    return render_template('edit.html', student=student)

# ---------- Student Active & InActive Toggle ----------
@app.route('/toggle-status/<int:id>')
@login_required
def toggle_status(id):
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT status FROM students WHERE id=?", (id,))
    current_status = c.fetchone()[0]

    new_status = "Inactive" if current_status == "Active" else "Active"

    c.execute("UPDATE students SET status=? WHERE id=?", (new_status, id))
    conn.commit()
    conn.close()

    return redirect('/admin')

# ---------- EXPORT EXCEL ----------
@app.route('/export/excel')
@login_required
def export_excel():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT student_id, name, course, status, dob, contact, email, blood_group, address FROM students ORDER BY id")
    students = c.fetchall()
    conn.close()

    df = pd.DataFrame(students, columns=['Student ID', 'Name', 'Course', 'status', 'dob', 'contact', 'email', 'blood Group', 'address'])
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Students')

    output.seek(0)
    return send_file(output, download_name="students.xlsx", as_attachment=True)

# ---------- EXPORT PDF  ----------
@app.route('/export/pdf')
@login_required
def export_pdf():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT student_id, name, course, photo, qr, status,
           dob, contact, email, blood_group, address
        FROM students
        ORDER BY id DESC
    """)
    students = c.fetchall()
    conn.close()

    output = BytesIO()
    pdf = canvas.Canvas(output, pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(width / 2, height - 50, "Student Records")

    y = height - 90
    row_height = 210   # increased for full details

    for student in students:

        # --- Images (safe check) ---
        photo_path = f"static/uploads/{student[3]}"
        qr_path = f"static/uploads/{student[4]}"

        if os.path.exists(photo_path):
            pdf.drawImage(photo_path, 40, y - 160, width=90, height=90)

        if os.path.exists(qr_path):
            pdf.drawImage(qr_path, width - 140, y - 160, width=90, height=90)

        # --- Text info ---
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(150, y - 20,  f"Student ID : {student[0]}")
        pdf.drawString(150, y - 40,  f"Name       : {student[1]}")
        pdf.drawString(150, y - 60,  f"Course     : {student[2]}")
        pdf.drawString(150, y - 80,  f"Status     : {student[5]}")

        pdf.setFont("Helvetica", 10)
        pdf.drawString(150, y - 100, f"DOB        : {student[6]}")
        pdf.drawString(150, y - 120, f"Contact    : {student[7]}")
        pdf.drawString(150, y - 140, f"Email      : {student[8]}")
        pdf.drawString(150, y - 160, f"Blood Group: {student[9]}")

        # Address (multi-line safe)
        pdf.drawString(150, y - 180, f"Address    : {student[10][:80]}")

        y -= row_height

        # --- New Page ---
        if y < 250:
            pdf.showPage()
            pdf.setFont("Helvetica-Bold", 18)
            pdf.drawCentredString(width / 2, height - 50, "Student Records")
            y = height - 90

    pdf.save()
    output.seek(0)

    return send_file(
        output,
        download_name="students.pdf",
        as_attachment=True
    )

# ---------- view Student Details ----------
@app.route('/view/<int:id>')
@login_required
def view_student(id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE id=?", (id,))
    student = c.fetchone()
    conn.close()

    if not student:
        return "Student not found"

    return render_template('view_student.html', student=student)

# ---------- Student Login ----------
@app.route('/student-login', methods=['GET', 'POST'])
def student_login():
    error = None

    if request.method == 'POST':
        student_id = request.form['student_id']
        dob = request.form['dob']

        conn = get_db()
        c = conn.cursor()
        c.execute("""
            SELECT * FROM students 
            WHERE student_id=? AND dob=? AND status='Active'
        """, (student_id, dob))
        student = c.fetchone()
        conn.close()

        if student:
            session['student_logged_in'] = True
            session['student_id'] = student_id
            return redirect('/student-dashboard')
        else:
            error = "Account inactive or invalid credentials"

    return render_template('student_login.html', error=error)

# ---------- Student Dashboard ----------
@app.route('/student-dashboard')
def student_dashboard():
    if not session.get('student_logged_in'):
        return redirect('/student-login')

    sid = session.get('student_id')

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE student_id=?", (sid,))
    s = c.fetchone()
    conn.close()

    # 🔒 Double security check
    if not s or s[6] != 'Active':
        session.clear()
        return "<h3 style='color:red;text-align:center'>Your account is inactive. Contact admin.</h3>"

    return render_template('student_profile.html', s=s)

# ---------- Student Logout ----------
@app.route('/student-logout')
def student_logout():
    session.clear()
    return redirect('/student-login')

# ---------- Student I-Card PDF ----------
@app.route('/student-id-pdf')
def student_id_pdf():
    if not session.get('student_logged_in'):
        return redirect('/student-login')

    sid = session.get('student_id')

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE student_id=?", (sid,))
    s = c.fetchone()
    conn.close()

    if not s or s[6] != 'Active':
        return "<h3 style='color:red;text-align:center'>Access Denied</h3>"

    output = BytesIO()
    pdf = canvas.Canvas(output, pagesize=(243, 400))  # ID card size

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(121, 370, "STUDENT ID CARD")

    # Photo
    pdf.drawImage(f"static/uploads/{s[4]}", 70, 240, 100, 100)

    pdf.setFont("Helvetica", 10)
    pdf.drawString(20, 210, f"Name: {s[2]}")
    pdf.drawString(20, 190, f"Course: {s[3]}")
    pdf.drawString(20, 170, f"ID: {s[1]}")
    pdf.drawString(20, 150, f"DOB: {s[7]}")
    pdf.drawString(20, 130, f"Contact: {s[8]}")
    pdf.drawString(20, 110, f"Blood: {s[10]}")

    # QR Code
    pdf.drawImage(f"static/uploads/{s[5]}", 70, 30, 100, 100)

    pdf.save()
    output.seek(0)

    return send_file(
        output,
        download_name=f"{s[1]}_ID_Card.pdf",
        as_attachment=True
    )


# Add these imports at the top of app.py if not already present

# ---------- BULK UPLOAD ROUTE ----------
@app.route('/bulk-upload', methods=['GET', 'POST'])
@login_required
def bulk_upload():
    if request.method == 'GET':
        return render_template('bulk_upload.html')

    excel_file = request.files.get('file')
    photos_file = request.files.get('photos_zip')

    if not excel_file or not excel_file.filename:
        return "Please select an Excel file."

    if not photos_file or not photos_file.filename:
        return "Please select a ZIP file containing student photos."

    upload_dir = os.path.join('static', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)

    saved_files = []

    try:
        # Read Excel
        df = pd.read_excel(excel_file)

        required_columns = [
            'name', 'course', 'dob', 'contact',
            'email', 'blood_group', 'address', 'photo'
        ]

        missing = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing:
            return f"Missing Excel columns: {', '.join(missing)}"

        if df.empty:
            return "The Excel file contains no student records."

        # Read ZIP without extracting arbitrary paths
        if not zipfile.is_zipfile(photos_file):
            return "The photos upload must be a valid ZIP file."

        photos_file.seek(0)
        photo_zip = zipfile.ZipFile(photos_file)

        # Index image files by filename
        photo_entries = {}

        for info in photo_zip.infolist():
            if info.is_dir():
                continue

            filename = os.path.basename(info.filename)
            extension = os.path.splitext(filename)[1].lower()

            if extension in {'.jpg', '.jpeg', '.png', '.webp'}:
                photo_entries[filename.lower()] = info

        conn = get_db()
        c = conn.cursor()

        try:
            conn.execute("BEGIN")

            for _, row in df.iterrows():
                # Generate a student ID
                sid = (
                    "SID"
                    + datetime.now().strftime("%Y%m%d")
                    + str(uuid.uuid4().int)[:6]
                )

                # Find and save the student's photo
                photo_value = row['photo']
                photo_name = None

                if pd.notna(photo_value) and str(photo_value).strip():
                    original_name = secure_filename(
                        os.path.basename(str(photo_value).strip())
                    )

                    info = photo_entries.get(original_name.lower())

                    if not info:
                        raise ValueError(
                            f"Photo '{original_name}' was not found "
                            f"in the ZIP file."
                        )

                    image_bytes = photo_zip.read(info)

                    # Validate that the file is a readable image
                    with Image.open(BytesIO(image_bytes)) as img:
                        img.verify()
                        image_format = img.format

                    extension = {
                        'JPEG': '.jpg',
                        'PNG': '.png',
                        'WEBP': '.webp'
                    }.get(image_format)

                    if not extension:
                        raise ValueError(
                            f"Unsupported image format: {original_name}"
                        )

                    photo_name = sid + extension
                    photo_path = os.path.join(upload_dir, photo_name)

                    with open(photo_path, 'wb') as image_file:
                        image_file.write(image_bytes)

                    saved_files.append(photo_path)

                # Generate QR code linking to verification
                verify_url = (
                    request.host_url.rstrip('/')
                    + f"/verify/{sid}"
                )

                qr_img = qrcode.make(verify_url)
                qr_name = sid + "_qr.png"
                qr_path = os.path.join(upload_dir, qr_name)
                qr_img.save(qr_path)
                saved_files.append(qr_path)

                # Convert Excel dates into database-friendly strings
                dob_value = row['dob']

                if pd.isna(dob_value):
                    dob_value = None
                elif isinstance(dob_value, (datetime, pd.Timestamp)):
                    dob_value = dob_value.strftime('%Y-%m-%d')
                else:
                    dob_value = str(dob_value).strip()

                def clean_value(value):
                    return None if pd.isna(value) else str(value).strip()

                c.execute("""
                    INSERT INTO students
                    (
                        student_id, name, course, dob, contact,
                        email, blood_group, address, photo, qr, status
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    sid,
                    clean_value(row['name']),
                    clean_value(row['course']),
                    dob_value,
                    clean_value(row['contact']),
                    clean_value(row['email']),
                    clean_value(row['blood_group']),
                    clean_value(row['address']),
                    photo_name,
                    qr_name,
                    'Active'
                ))

            conn.commit()

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()
            photo_zip.close()

        # return (
        #     f"Bulk upload completed successfully! "
        #     f"{len(df)} student record(s) imported."
        # )
        
        return redirect(
            url_for(
            'success',
            bulk_upload=1,
            success_count=len(df),
            failed_count=0
            )
        )

    except Exception as e:
        # Remove generated files if the import fails
        for path in saved_files:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except OSError:
                pass

        return f"Bulk upload failed: {e}"

@app.route('/success')
@login_required
def success():
    is_bulk_upload = request.args.get('bulk_upload') == '1'

    success_count = request.args.get(
        'success_count', default=0, type=int
    )
    failed_count = request.args.get(
        'failed_count', default=0, type=int
    )

    return render_template(
        'success.html',
        bulk_upload=is_bulk_upload,
        success_count=success_count,
        failed_count=failed_count
    )

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
