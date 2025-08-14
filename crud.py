import sqlite3
from tabulate import tabulate  # type: ignore
import csv
from datetime import datetime
import hashlib
from getpass import getpass
import re
import shutil
import os


def create_student(current_user=None):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    print("\n--- Add New Student ---")

    # First Name
    first_name = input("First Name: ").strip()
    if not first_name:
        print("❌ First name cannot be empty.")
        conn.close()
        return

    # Last Name
    last_name = input("Last Name: ").strip()
    if not last_name:
        print("❌ Last name cannot be empty.")
        conn.close()
        return

    # Date of Birth
    dob = input("Date of Birth (YYYY-MM-DD): ").strip()
    if not validate_date(dob):
        print("❌ Invalid date format. Use YYYY-MM-DD.")
        conn.close()
        return

    # Email
    email = input("Email: ").strip()
    if not validate_email(email):
        print("❌ Invalid email format.")
        conn.close()
        return

    # Phone
    phone = input("Phone: ").strip()
    if not validate_phone(phone):
        print("❌ Phone must be numeric and 7–15 digits long.")
        conn.close()
        return

    # Enrollment Date
    enrollment_date = input("Enrollment Date (YYYY-MM-DD): ").strip()
    if not validate_date(enrollment_date):
        print("❌ Invalid enrollment date format. Use YYYY-MM-DD.")
        conn.close()
        return

    # Grade
    grade = input("Grade: ").strip()
    if not grade:
        print("❌ Grade cannot be empty.")
        conn.close()
        return

    # GPA
    gpa = input("GPA (0.0 – 4.0): ").strip()
    if not validate_gpa(gpa):
        print("❌ GPA must be a number between 0.0 and 4.0.")
        conn.close()
        return

    try:
        cursor.execute('''
        INSERT INTO students (first_name, last_name, dob, email, phone, enrollment_date, grade, gpa)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, dob, email, phone, enrollment_date, grade, float(gpa)))
        conn.commit()
        print("✅ Student added successfully!")
    except sqlite3.IntegrityError:
        print("❌ Error: Email already exists.")
    finally:
        conn.close()



def read_students():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    if rows:
        headers = ["ID", "First Name", "Last Name", "DOB", "Email", "Phone", "Enrollment Date", "Grade", "GPA"]
        print("\n--- Student Records ---")
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        print("⚠ No records found.")



def update_student(current_user=None):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    student_id = input("\nEnter Student ID to update: ").strip()
    if not student_id.isdigit():
        print("❌ Invalid ID.")
        conn.close()
        return

    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    student = cursor.fetchone()
    if not student:
        print("❌ Student not found.")
        conn.close()
        return

    print("\n--- Update Student ---")
    print("Press Enter to skip and keep current value.\n")

    # First Name
    first_name = input(f"First Name [{student[1]}]: ").strip()
    if first_name == "":
        first_name = student[1]

    # Last Name
    last_name = input(f"Last Name [{student[2]}]: ").strip()
    if last_name == "":
        last_name = student[2]

    # Date of Birth
    dob = input(f"Date of Birth (YYYY-MM-DD) [{student[3]}]: ").strip()
    if dob == "":
        dob = student[3]
    elif not validate_date(dob):
        print("❌ Invalid date format. Use YYYY-MM-DD.")
        conn.close()
        return

    # Email
    email = input(f"Email [{student[4]}]: ").strip()
    if email == "":
        email = student[4]
    elif not validate_email(email):
        print("❌ Invalid email format.")
        conn.close()
        return

    # Phone
    phone = input(f"Phone [{student[5]}]: ").strip()
    if phone == "":
        phone = student[5]
    elif not validate_phone(phone):
        print("❌ Phone must be numeric and 7–15 digits long.")
        conn.close()
        return

    # Enrollment Date
    enrollment_date = input(f"Enrollment Date (YYYY-MM-DD) [{student[6]}]: ").strip()
    if enrollment_date == "":
        enrollment_date = student[6]
    elif not validate_date(enrollment_date):
        print("❌ Invalid enrollment date format. Use YYYY-MM-DD.")
        conn.close()
        return

    # Grade
    grade = input(f"Grade [{student[7]}]: ").strip()
    if grade == "":
        grade = student[7]

    # GPA
    gpa = input(f"GPA (0.0 – 4.0) [{student[8]}]: ").strip()
    if gpa == "":
        gpa = student[8]
    elif not validate_gpa(gpa):
        print("❌ GPA must be a number between 0.0 and 4.0.")
        conn.close()
        return
    else:
        gpa = float(gpa)

    try:
        cursor.execute("""
            UPDATE students
            SET first_name=?, last_name=?, dob=?, email=?, phone=?, enrollment_date=?, grade=?, gpa=?
            WHERE id=?
        """, (first_name, last_name, dob, email, phone, enrollment_date, grade, gpa, student_id))
        conn.commit()
        print("✅ Student updated successfully!")
    except sqlite3.IntegrityError:
        print("❌ Error: Email already exists.")
    finally:
        conn.close()



def delete_student():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    student_id = input("\nEnter Student ID to delete: ")

    # Check if student exists
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    record = cursor.fetchone()
    if not record:
        print("❌ Student not found.")
        conn.close()
        return

    confirm = input(f"Are you sure you want to delete {record[1]} {record[2]}? (y/n): ").lower()
    if confirm == "y":
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        print("✅ Student deleted successfully!")
    else:
        print("❌ Deletion cancelled.")

    conn.close()


def search_students():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    print("\n--- Advanced Search ---")
    print("1. Search by First Name")
    print("2. Search by Last Name")
    print("3. Search by Email")
    print("4. Search by Grade")
    print("5. Search by GPA Range")
    print("6. Search by Enrollment Date Range")
    print("7. Search All Columns (Keyword Search)")

    choice = input("Enter choice: ").strip()

    if choice in ["1", "2", "3", "4"]:
        field_map = {
            "1": "first_name",
            "2": "last_name",
            "3": "email",
            "4": "grade"
        }
        field = field_map[choice]
        query = input(f"Enter {field.replace('_', ' ').title()} to search: ").strip()
        cursor.execute(f"SELECT * FROM students WHERE LOWER({field}) LIKE LOWER(?)", ('%' + query + '%',))

    elif choice == "5":  # GPA range
        min_gpa = input("Enter minimum GPA: ").strip()
        max_gpa = input("Enter maximum GPA: ").strip()
        cursor.execute("SELECT * FROM students WHERE gpa BETWEEN ? AND ?", (min_gpa, max_gpa))

    elif choice == "6":  # Enrollment date range
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()
        cursor.execute("SELECT * FROM students WHERE enrollment_date BETWEEN ? AND ?", (start_date, end_date))

    elif choice == "7":  # Search all columns
        keyword = input("Enter keyword to search in all columns: ").strip()
        cursor.execute("""
            SELECT * FROM students
            WHERE LOWER(first_name) LIKE LOWER(?)
               OR LOWER(last_name) LIKE LOWER(?)
               OR LOWER(email) LIKE LOWER(?)
               OR LOWER(phone) LIKE LOWER(?)
               OR LOWER(grade) LIKE LOWER(?)
        """, tuple(['%' + keyword + '%'] * 5))

    else:
        print("❌ Invalid choice.")
        conn.close()
        return

    rows = cursor.fetchall()
    conn.close()

    if rows:
        headers = ["ID", "First Name", "Last Name", "DOB", "Email", "Phone", "Enrollment Date", "Grade", "GPA"]
        print("\n--- Search Results ---")
        print(tabulate(rows, headers=headers, tablefmt="grid"))

        choice = input("\nDo you want to export these results to CSV? (y/n): ").strip().lower()
        if choice == "y":
            export_to_csv(rows, headers)

    else:
        print("⚠ No matching records found.")


    
def export_to_csv(rows=None, headers=None):
    if not rows:
        # If no search results provided, export all data
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        conn.close()
        headers = ["ID", "First Name", "Last Name", "DOB", "Email", "Phone", "Enrollment Date", "Grade", "GPA"]

    if not rows:
        print("⚠ No data to export.")
        return

    filename = f"students_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"✅ Data exported to {filename}")



def import_from_csv():
    print("\t\t Instructions \t\t \n\nYour CSV file should have the following headers in the exact order:")
    print("First Name, Last Name, DOB, Email, Phone, Enrollment Date, Grade, GPA")
    print("Make sure emails are unique, the date format is YYYY-MM-DD and GPA is a number.")
    print("If any of the fields are missing, the import will fail.")
    file_path = input("\nEnter path to CSV file: ").strip()

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            required_fields = ["First Name", "Last Name", "DOB", "Email", "Phone", "Enrollment Date", "Grade", "GPA"]

            # Validate headers
            if not all(field in reader.fieldnames for field in required_fields):
                print("❌ CSV file is missing required columns.")
                print(f"Required columns: {required_fields}")
                return

            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            inserted_count = 0
            skipped_count = 0

            for row in reader:
                try:
                    cursor.execute('''
                        INSERT INTO students (first_name, last_name, dob, email, phone, enrollment_date, grade, gpa)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row["First Name"],
                        row["Last Name"],
                        row["DOB"],
                        row["Email"],
                        row["Phone"],
                        row["Enrollment Date"],
                        row["Grade"],
                        float(row["GPA"]) if row["GPA"] else None
                    ))
                    inserted_count += 1
                except Exception as e:
                    print(f"⚠ Skipping row due to error: {e}")
                    skipped_count += 1

            conn.commit()
            conn.close()

            print(f"✅ Import complete: {inserted_count} records added, {skipped_count} skipped.")

    except FileNotFoundError:
        print("❌ File not found. Please check the path.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")



def register_user(current_role=None):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()

    print("\n--- Register New User ---")
    username = input("Username: ").strip()
    if not username:
        print("❌ Username cannot be empty.")
        conn.close()
        return False

    pw1 = getpass("Password: ").strip()
    pw2 = getpass("Confirm Password: ").strip()

    if not pw1 or len(pw1) < 6:
        print("❌ Password must be at least 6 characters.")
        conn.close()
        return False
    if pw1 != pw2:
        print("❌ Passwords do not match.")
        conn.close()
        return False

    # Role selection: only admins can assign admin role
    if current_role == "admin":
        role = input("Role (admin/viewer): ").strip().lower()
        if role not in ("admin", "viewer"):
            print("❌ Invalid role. Defaulting to viewer.")
            role = "viewer"
    else:
        role = "viewer"  # default for self-registration

    try:
        ph = hashlib.sha256(pw1.encode()).hexdigest()
        cur.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (username, ph, role))
        conn.commit()
        print(f"✅ User '{username}' registered with role '{role}'!")
        return True
    except sqlite3.IntegrityError:
        print("❌ Username already exists.")
        return False
    finally:
        conn.close()




def login():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()

    print("\n--- Login ---")
    username = input("Username: ").strip()
    password = getpass("Password: ").strip()

    ph = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("SELECT role FROM users WHERE username = ? AND password_hash = ?", (username, ph))
    user = cur.fetchone()
    conn.close()

    if user:
        role = user[0]
        print(f"✅ Welcome, {username}! Role: {role}")
        return role
    else:
        print("❌ Invalid username or password.")
        return None




def ensure_first_user():
    """Make sure at least one user exists before showing the app menu."""
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]
    conn.close()

    if count == 0:
        print("\nℹ No users found. Please create the first account.")
        created = register_user()
        if not created:
            print("⚠ Could not create a user. You must register at least one account to proceed.")
            return False
    return True


def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None

def validate_phone(phone):
    return phone.isdigit() and (7 <= len(phone) <= 15)

def validate_gpa(gpa):
    try:
        gpa = float(gpa)
        return 0.0 <= gpa <= 4.0
    except ValueError:
        return False


def backup_database():
    if not os.path.exists("students.db"):
        print("❌ No database found to backup.")
        return
    
    # Create backups folder if it doesn't exist
    os.makedirs("backups", exist_ok=True)
    
    backup_filename = f"backups/students_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    try:
        shutil.copy("students.db", backup_filename)
        print(f"✅ Backup created successfully: {backup_filename}")
    except Exception as e:
        print(f"❌ Backup failed: {e}")



def restore_database():
    backups_folder = "backups"
    
    if not os.path.exists(backups_folder) or not os.listdir(backups_folder):
        print("❌ No backup files found.")
        return
    
    print("\n--- Available Backups ---")
    backups = sorted(os.listdir(backups_folder), reverse=True)
    for i, backup in enumerate(backups, start=1):
        print(f"{i}. {backup}")
    
    choice = input("\nEnter the number of the backup to restore: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(backups)):
        print("❌ Invalid choice.")
        return
    
    selected_backup = backups[int(choice) - 1]
    try:
        shutil.copy(os.path.join(backups_folder, selected_backup), "students.db")
        print(f"✅ Database restored from {selected_backup}")
    except Exception as e:
        print(f"❌ Restore failed: {e}")


