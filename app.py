from flask import Flask, jsonify, request, render_template
import os

app = Flask(__name__, template_folder="templates")

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "2024-00331",
        "name": "Jiza Mae Gubac",
        "program": "BSIT",
        "year": 3,
        "section": "B"
    })


@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!"
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
