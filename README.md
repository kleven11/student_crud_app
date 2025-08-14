# Student CRUD Management System

A Python-based command-line application to manage student records with features like create, read, update, delete (CRUD), search, backup/restore, and CSV import/export.  
Built with **SQLite** for storage and **Tabulate** for clean, formatted tables.

---

## 📌 Features
- Add, update, delete student records
- Search students by name, email, grade, or GPA range
- Role-based access control (Admin & Viewer)
- Backup and restore the database
- Import and export data via CSV
- Input validation for dates, emails, phone numbers, and GPA

---

## 🛠️ Technologies Used
- **Python 3**
- **SQLite** (database)
- **Tabulate** (table formatting)

---

## 📦 Installation
1. Clone the repository:
   In your terminal enter

   git clone https://github.com/your-username/student_crud_app.git
   cd student_crud_app

2. Then you need to run setup_db.py only once for the first time. This initializes the database and it's tables.
   
    python setup_db.py
   
4. Run the application:

   python main.py

5. Initially to get admin privileges the default credentials are 

  username = admin
  password = admin123

  Use them to login as admin, then you can add other admin users.

---

## 🔐 Roles

Admin: Full access (CRUD, backup/restore, import/export)

Viewer: Read-only access

---

## 📂 Sample Data

You can import the sample CSV file named "student_import.csv" directly into the database.
