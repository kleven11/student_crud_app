import sqlite3, hashlib

# Connect to database (creates file if it doesn't exist)
conn = sqlite3.connect('students.db')
cur = conn.cursor()

# Create table if not exists
cur.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    dob DATE NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    enrollment_date DATE,
    grade TEXT,
    gpa REAL
    )
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
''')

# Create a default admin if no users exist
cur.execute("SELECT COUNT(*) FROM users")
if cur.fetchone()[0] == 0:
    default_user = "admin"
    default_pass = "admin123"  # change after first login
    ph = hashlib.sha256(default_pass.encode()).hexdigest()
    cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (default_user, ph))
    print("✅ Created default admin -> username: admin | password: admin123 ")
    print("✅ Users table ready.")


cur.execute('''
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    action TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Add role column if it doesn't exist
try:
    cur.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'viewer'")
    cur.execute("UPDATE users SET role = 'admin' WHERE username = 'admin'")
    print("✅ Role column added to users table.")
except sqlite3.OperationalError:
    pass

# Save changes
conn.commit()

print("Database connected and table ready to use")

conn.close()