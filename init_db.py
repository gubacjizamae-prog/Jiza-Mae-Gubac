import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Create the students table
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

# Reset the automatic ID counter
cursor.execute(
    "DELETE FROM sqlite_sequence WHERE name = 'students'"
)

# Five fictional sample student records
students = [
    ('2026-00101', 'Alex Santos', 'BSIT', 1, 'A'),
    ('2026-00102', 'Jamie Reyes', 'BSIT', 1, 'B'),
    ('2026-00103', 'Taylor Cruz', 'BSIT', 2, 'A'),
    ('2026-00104', 'Morgan Garcia', 'BSIT', 2, 'B'),
    ('2026-00105', 'Casey Mendoza', 'BSIT', 3, 'A')
]

# Insert records into the database
cursor.executemany('''
    INSERT INTO students (
        student_id, name, program, year, section
    )
    VALUES (?, ?, ?, ?, ?)
''', students)

# Save changes
conn.commit()

# Verify the number of records
total = cursor.execute(
    'SELECT COUNT(*) FROM students'
).fetchone()[0]

conn.close()

print("Database initialized successfully.")
print(f"Total student records: {total}")
