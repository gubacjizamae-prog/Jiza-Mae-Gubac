import sqlite3

# Connect to the database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Create the students table if it does not exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        name TEXT NOT NULL,
        program TEXT NOT NULL,
        year INTEGER NOT NULL,
        section TEXT NOT NULL
    )
''')

# Remove existing records
cursor.execute('DELETE FROM students')

# Five sample student records
students = [
    ('2026-00101', 'Alex Santos', 'BSIT', 1, 'A'),
    ('2026-00102', 'Jamie Reyes', 'BSIT', 1, 'B'),
    ('2026-00103', 'Taylor Cruz', 'BSIT', 2, 'A'),
    ('2026-00104', 'Morgan Garcia', 'BSIT', 2, 'B'),
    ('2026-00105', 'Casey Mendoza', 'BSIT', 3, 'A')
]

# Insert student records
cursor.executemany('''
    INSERT INTO students (student_id, name, program, year, section)
    VALUES (?, ?, ?, ?, ?)
''', students)

# Save changes and close the database
conn.commit()
conn.close()

print("Database initialized successfully with five student records.")
