import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# Database connection
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Student Information API
@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "2024=00331",
        "name": "Jiza Mae Gubac",
        "program": "BSIT",
        "year": 3,
        "section": "B"
    })


# Greeting API
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')

    return jsonify({
        "message": f"Hello, {name}!"
    })


# Get all students from the database
@app.route('/students')
def get_students():
    conn = get_db_connection()

    try:
        students = conn.execute(
            'SELECT * FROM students ORDER BY id'
        ).fetchall()
    finally:
        conn.close()

    return jsonify([dict(student) for student in students])


# Get one student by database ID
@app.route('/students/<int:id>')
def get_student_by_id(id):
    conn = get_db_connection()

    try:
        student = conn.execute(
            'SELECT * FROM students WHERE id = ?',
            (id,)
        ).fetchone()
    finally:
        conn.close()

    if student is None:
        return jsonify({
            "error": "Student not found"
        }), 404

    return jsonify(dict(student))


# Get students by year level
@app.route('/students/year/<int:year>')
def get_students_by_year(year):
    conn = get_db_connection()

    try:
        students = conn.execute(
            'SELECT * FROM students WHERE year = ? ORDER BY id',
            (year,)
        ).fetchall()
    finally:
        conn.close()

    return jsonify([dict(student) for student in students])


if __name__ == '__main__':
    app.run(debug=True)