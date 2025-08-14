# 🎓 Student CRUD Management System

A Python-based **command-line application** to manage student records with features like Create, Read, Update, Delete (CRUD), search, backup/restore, and CSV import/export.  
Built with **SQLite** for storage and **Tabulate** for clean, formatted tables.

---

## 📌 Features
- ➕ Add, ✏️ Update, ❌ Delete student records  
- 🔍 Search students by **name, email, grade, or GPA range**  
- 🔐 Role-based access control (**Admin** & **Viewer**)  
- 💾 Backup and restore the database  
- 📤 Import and 📥 export data via CSV  
- ✅ Input validation for **dates, emails, phone numbers, and GPA**

---

## 🛠️ Technologies Used
- **Python 3**
- **SQLite** (database)
- **Tabulate** (table formatting)

---

## 📦 Installation & Setup

1️⃣ **Clone the repository**

git clone https://github.com/your-username/student_crud_app.git

cd student_crud_app

2️⃣ Initialize the database (Run only once)

python setup_db.py
This will create the database and required tables.

3️⃣ Run the application

python main.py

4️⃣ Login with default admin credentials (first-time use only)

Username: admin
Password: admin123
📝 After logging in as admin, you can create other admin or viewer accounts.

---

## 🔐 Roles

Admin:- Full access: CRUD, backup/restore, import/export

Viewer:- Read-only access: Can only view student records

---

## 📂 Sample Data

A sample CSV file named student_import.csv is provided.

To import it:

Run the application

Select "Import from CSV" from the menu

Enter student_import.csv as the filename(or copy filepath)

---

## 📄 License
This project is open-source and available under the MIT License.
