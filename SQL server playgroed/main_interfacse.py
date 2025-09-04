# main_interfaces.py
import Functions

def main_menu():
    while True:
        Functions.clear()
        print("\n--- Main Menu ---")
        print("1. Admin Interface")
        print("2. User Menu")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            admin_interface()
        elif choice == "2":
            user_menu()
        elif choice == "3":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def admin_interface():
    while True:
        Functions.clear()
        print("\n--- Admin Interface ---")
        print("1. Add User")
        print("2. Remove User")
        print("3. View All Users")
        print("4. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username to add: ")
            Functions.add_user(username)
            input("Press Enter to continue...")

        elif choice == "2":
            Functions.clear()
            print("--- Remove User ---")
            users = Functions.get_all_users()
            if not users:
                print("No users available to delete.")
                input("Press Enter to continue...")
                continue

            for i, (uid, uname) in enumerate(users, start=1):
                print(f"{i}. ID: {uid} | Username: {uname}")

            try:
                choice_num = int(input("Enter the number of the user to delete: "))
                if 1 <= choice_num <= len(users):
                    user_id = users[choice_num - 1][0]
                    confirm = input(f"Are you sure you want to delete ID {user_id}? (y/n): ").lower()
                    if confirm == 'y':
                        Functions.remove_user(user_id)
                    else:
                        print("Delete cancelled.")
                else:
                    print("Invalid number selected.")
            except ValueError:
                print("Invalid input. Please enter a number.")

            input("Press Enter to continue...")

        elif choice == "3":
            Functions.view_users()
            input("Press Enter to continue...")

        elif choice == "4":
            break

        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def user_menu():
    while True:
        Functions.clear()
        print("\n--- User Menu ---")
        print("1. View Profile")
        print("2. Update Profile")
        print("3. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            user_id = input("Enter your user ID: ")
            if user_id.isdigit():
                Functions.view_profile(int(user_id))
            else:
                print("Invalid ID. Must be a number.")
            input("Press Enter to continue...")

        elif choice == "2":
            user_id = input("Enter your user ID: ")
            if user_id.isdigit():
                new_data = input("Enter new profile data: ")
                Functions.update_profile(int(user_id), new_data)
            else:
                print("Invalid ID. Must be a number.")
            input("Press Enter to continue...")

        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    Functions.clear()
    print("Welcome to the Playground System")
    Functions.ensure_table_exists()
    input("\nDatabase is ready. Press Enter to continue...")
    main_menu()
