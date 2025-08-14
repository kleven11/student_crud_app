from crud import (
    create_student, read_students, update_student, delete_student,
    search_students, export_to_csv, import_from_csv,
    register_user, login, ensure_first_user, backup_database, restore_database
)

def app_menu(role):
    while True:
        print("\n--- Student Management System ---")
        print("1. View Students")
        print("2. Search Students")
        print("3. Export All Data to CSV")
        if role == "admin":
            print("4. Add Student")
            print("5. Update Student")
            print("6. Delete Student")
            print("7. Import Students from CSV")
            print("8. Register New User")
            print("9. Backup Database")
            print("10. Restore Database")
        print("0. Logout")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            read_students()
        elif choice == "2":
            search_students()
        elif choice == "3":
            export_to_csv()
        elif choice == "4" and role == "admin":
            create_student()
        elif choice == "5" and role == "admin":
            update_student()
        elif choice == "6" and role == "admin":
            delete_student()
        elif choice == "7" and role == "admin":
            import_from_csv()
        elif choice == "8" and role == "admin":
            register_user(current_role=role)
        elif choice == "9" and role == "admin":
            backup_database()
        elif choice == "10" and role == "admin":
            restore_database()
        elif choice == "0":
            print("👋 Logging out...")
            break
        else:
            print("❌ Invalid choice or insufficient permissions.")


if __name__ == "__main__":
    if not ensure_first_user():
        raise SystemExit(1)

    while True:
        print("\n--- Authentication ---")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        auth = input("Choose: ").strip()

        if auth == "1":
            role = login()
            if role:
                app_menu(role)
        elif auth == "2":
            register_user(current_role=None)
        elif auth == "3":
            print("Bye!")
            break
        else:
            print("❌ Invalid choice.")
