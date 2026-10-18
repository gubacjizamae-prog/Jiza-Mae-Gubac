from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to my first API!"


@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "24-00331",
        "name": "Jiza Mae Gubac",
        "program": "BSIT",
        "year": 3,
        "section": "B-Dijkstra"
    })

@app.route('/profile')
def get_profile():
    return jsonify({
        "student_id": "24-00331",
        "name": "Jiza Mae Gubac",
        "program": "BSIT",
        "year": 3,
        "section": "B-Dijkstra",
        "email":"gubacjizamae@isufst.edu.ph",
        "skills":"python only"
    })

@app.route('/course')
def get_course():
    return jsonify({
        "course_code": "IT 3120",
        "course_title": "System Integration",
        "instructor": "Rene Arduo",
        "semester": "First Semester",
        "academic_year": "2026-2027"
    })

@app.route('/hello')
def get_hello():
    name = request.args.get('name', 'Students')
    return jsonify({
        "message": f"Hello, {name}!"
    })
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
