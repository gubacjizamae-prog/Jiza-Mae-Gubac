import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# ==========================================
# DATABASE CONNECTION
# ==========================================
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# HOME PAGE
# ==========================================
@app.route('/')
def home():
    return render_template('index.html')


# ==========================================
# STUDENT INFORMATION
# ==========================================
@app.route('/student', methods=['GET'])
def get_student():
    return jsonify({
        "student_id": "2024-00331",
        "name": "Jiza Mae Gubac",
        "program": "BSIT",
        "year": 3,
        "section": "B"
    })


# ==========================================
# GREETING API
# ==========================================
@app.route('/hello', methods=['GET'])
def hello():
    name = request.args.get('name', 'World')
    return jsonify({"message": f"Hello, {name}!"})


# ==========================================
# READ - GET ALL STUDENTS
# ==========================================
@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()

    rows = conn.execute(
        'SELECT * FROM students'
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


# ==========================================
# READ - GET STUDENT BY DATABASE ID
# ==========================================
@app.route('/students/<int:id>', methods=['GET'])
def get_student_by_id(id):
    conn = get_db_connection()

    student = conn.execute(
        'SELECT * FROM students WHERE id = ?',
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# ==========================================
# READ - GET STUDENTS BY YEAR LEVEL
# ==========================================
@app.route('/students/year/<int:year>', methods=['GET'])
def get_students_by_year(year):
    conn = get_db_connection()

    rows = conn.execute(
        'SELECT * FROM students WHERE year = ?',
        (year,)
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


# ==========================================
# STEP 6: READ-ONLY API FOR CLASSMATES
# GET /api/students
# ==========================================
@app.route('/api/students', methods=['GET'])
def api_students():
    conn = get_db_connection()

    rows = conn.execute(
        'SELECT * FROM students'
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


# ==========================================
# CREATE - ADD A STUDENT
# POST /api/students
# ==========================================
@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Valid JSON data is required"}), 400

    required_fields = [
        'student_id', 'name', 'program', 'year', 'section'
    ]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "All student fields are required"}), 400

    try:
        year = int(data['year'])
    except (ValueError, TypeError):
        return jsonify({"error": "Year must be a number"}), 400

    conn = get_db_connection()

    try:
        cursor = conn.execute(
            """
            INSERT INTO students
            (student_id, name, program, year, section)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                data['student_id'],
                data['name'],
                data['program'],
                year,
                data['section']
            )
        )

        conn.commit()
        new_id = cursor.lastrowid

    finally:
        conn.close()

    return jsonify({
        "message": "Student added",
        "id": new_id
    }), 201


# ==========================================
# READ - GET ONE STUDENT THROUGH THE API
# GET /api/students/<id>
# ==========================================
@app.route('/api/students/<int:id>', methods=['GET'])
def api_get_student(id):
    conn = get_db_connection()

    student = conn.execute(
        'SELECT * FROM students WHERE id = ?',
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# ==========================================
# UPDATE - EDIT A STUDENT
# PUT /api/students/<id>
# ==========================================
@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Valid JSON data is required"}), 400

    required_fields = [
        'student_id', 'name', 'program', 'year', 'section'
    ]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "All student fields are required"}), 400

    try:
        year = int(data['year'])
    except (ValueError, TypeError):
        return jsonify({"error": "Year must be a number"}), 400

    conn = get_db_connection()

    try:
        cursor = conn.execute(
            """
            UPDATE students
            SET student_id = ?, name = ?, program = ?, year = ?, section = ?
            WHERE id = ?
            """,
            (
                data['student_id'],
                data['name'],
                data['program'],
                year,
                data['section'],
                id
            )
        )

        conn.commit()
        updated = cursor.rowcount

    finally:
        conn.close()

    if updated == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student updated"})


# ==========================================
# DELETE - REMOVE A STUDENT
# DELETE /api/students/<id>
# ==========================================
@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()

    try:
        cursor = conn.execute(
            'DELETE FROM students WHERE id = ?',
            (id,)
        )

        conn.commit()
        deleted = cursor.rowcount

    finally:
        conn.close()

    if deleted == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student deleted"})


# ==========================================
# RUN APPLICATION
# ==========================================
if __name__ == '__main__':
    app.run(debug=True)