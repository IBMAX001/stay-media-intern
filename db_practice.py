import sqlite3

conn = sqlite3.connect("practice.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS interns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

cur.execute("INSERT INTO interns (name, role) VALUES (?, ?)",
            ("Ibelo", "Python Web Dev Intern"))
conn.commit()

cur.execute("SELECT * FROM interns")
print(cur.fetchall())

conn.close()
