import sqlite3

conn = sqlite3.connect('students.db')
cur = conn.cursor()

cur.execute("UPDATE users SET role = 'admin' WHERE username = 'admin'")
conn.commit()
conn.close()

print("✅ Updated admin role for user 'admin'")
