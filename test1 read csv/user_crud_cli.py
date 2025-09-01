#!/usr/bin/env python3
"""
User CRUD Database (CLI) — with Admin & User roles
==================================================

What this script does
---------------------
- Uses SQLite (built into Python) to store users in file: users.db
- Auto-allocates a unique integer ID for each user (PRIMARY KEY AUTOINCREMENT)
- Supports two roles:
    * admin — can Create, Read, Update, Delete any user
    * user  — can view and update ONLY their own profile, and change password
- Hashes passwords with sha256 + a unique random salt (demo-level security)
  (For production, use a real password hasher like bcrypt/argon2.)

How to run
----------
1) Save this file as: user_crud_cli.py
2) In a terminal, run:  python user_crud_cli.py
3) On first start, the database is created and a default admin user is added:
       username: admin
       password: admin123
   **Change this password immediately** after you log in.

Notes
-----
- The database file (users.db) is created in the same folder as this script.
- All input is text-based; follow the on-screen menus.
"""

import os
import sqlite3
import getpass
import hashlib
import secrets
from typing import Optional, Tuple, Dict, Any
from openai import OpenAI

DB_NAME = "users.db"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": "Hello, how are you?"}]
)

print(response.choices[0].message.content)
# ---------- Password Utilities ----------

def hash_password(plain_password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    """
    Hash a password with SHA-256 and a random per-user salt.
    Returns (salt, password_hash) as hex strings.
    NOTE: For real apps, use bcrypt/argon2 instead of sha256.
    """
    if salt is None:
        # 16 random bytes -> 32 hex chars
        salt = secrets.token_hex(16)
    # Combine salt + password; encode to bytes; hash with sha256; return hex digest
    digest = hashlib.sha256((salt + plain_password).encode("utf-8")).hexdigest()
    return salt, digest


def verify_password(plain_password: str, salt: str, expected_hash: str) -> bool:
    """Check a plaintext password against a stored (salt, hash)."""
    _, digest = hash_password(plain_password, salt=salt)
    return secrets.compare_digest(digest, expected_hash)


# ---------- Database Helpers ----------

def get_connection() -> sqlite3.Connection:
    """Open a SQLite connection with sensible defaults."""
    conn = sqlite3.connect(DB_NAME)
    # Make rows behave like dicts: row["column_name"]
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """
    Create tables if they don't exist.
    Also seed a default admin (admin/admin123) if no admin exists yet.
    """
    with get_connection() as conn:
        cur = conn.cursor()
        # Create a "users" table. The 'id' column auto-increments for each row.
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                full_name TEXT,
                email TEXT UNIQUE,
                role TEXT NOT NULL CHECK(role IN ('admin', 'user')),
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.commit()

        # If no admin exists, create a default one.
        cur.execute("SELECT COUNT(*) AS c FROM users WHERE role = 'admin';")
        count_admin = cur.fetchone()["c"]
        if count_admin == 0:
            # Seed default admin account
            username = "admin"
            full_name = "Default Admin"
            email = "admin@example.com"
            role = "admin"
            salt, password_hash = hash_password("admin123")
            try:
                cur.execute(
                    """
                    INSERT INTO users (username, full_name, email, role, salt, password_hash)
                    VALUES (?, ?, ?, ?, ?, ?);
                    """,
                    (username, full_name, email, role, salt, password_hash),
                )
                conn.commit()
                print("\n[SETUP] Created default admin: username='admin', password='admin123'")
                print("        Please change this password after logging in.\n")
            except sqlite3.IntegrityError:
                # In case a race condition or a previous partial setup happened
                pass


# ---------- CRUD Operations (Admin) ----------

def create_user(username: str, full_name: str, email: str, role: str, password: str) -> int:
    """Create a new user and return the new user's ID."""
    if role not in ("admin", "user"):
        raise ValueError("Role must be 'admin' or 'user'.")

    salt, password_hash = hash_password(password)
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO users (username, full_name, email, role, salt, password_hash)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            (username.strip(), full_name.strip(), email.strip(), role, salt, password_hash),
        )
        conn.commit()
        return cur.lastrowid  # The auto-allocated ID
from typing import Any, Optional

def read_user_by_username(username: str) -> Optional[sqlite3.Row]:
    """Fetch a user by username (or return None if missing)."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?;", (username.strip(),))
        row = cur.fetchone()
        return row


def read_user_by_id(user_id: int) -> Optional[sqlite3.Row]:
    """Fetch a user by ID (or return None if missing)."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?;", (user_id,))
        return cur.fetchone()


def list_users() -> list[sqlite3.Row]:
    """Return all users sorted by ID."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, username, full_name, email, role, created_at FROM users ORDER BY id;")
        return cur.fetchall()


def update_user(
    user_id: int,
    full_name: Optional[str] = None,
    email: Optional[str] = None,
    role: Optional[str] = None,
    new_password: Optional[str] = None,
) -> None:
    """
    Update user fields. Only non-None fields are applied.
    If new_password is set, the salt/hash are regenerated.
    """
    updates = []
    params: list[Any] = []

    if full_name is not None:
        updates.append("full_name = ?")
        params.append(full_name.strip())
    if email is not None:
        updates.append("email = ?")
        params.append(email.strip())
    if role is not None:
        if role not in ("admin", "user"):
            raise ValueError("Role must be 'admin' or 'user'.")
        updates.append("role = ?")
        params.append(role)
    if new_password is not None:
        salt, password_hash = hash_password(new_password)
        updates.append("salt = ?")
        params.append(salt)
        updates.append("password_hash = ?")
        params.append(password_hash)

    if not updates:
        return  # Nothing to do

    params.append(user_id)
    with get_connection() as conn:
        cur = conn.cursor()
        sql = f"UPDATE users SET {', '.join(updates)} WHERE id = ?;"
        cur.execute(sql, tuple(params))
        conn.commit()


def delete_user(user_id: int) -> None:
    """Delete a user by ID."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = ?;", (user_id,))
        conn.commit()


# ---------- Authentication & Menus ----------

def login() -> Optional[sqlite3.Row]:
    """Prompt for username & password and return the user row if valid."""
    print("\n=== Login ===")
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ").strip()

    user = read_user_by_username(username)
    if user is None:
        print("Invalid username or password.\n")
        return None

    if verify_password(password, user["salt"], user["password_hash"]):
        print(f"\nWelcome, {user['username']}! (role: {user['role']})\n")
        return user

    print("Invalid username or password.\n")
    return None


def prompt_nonempty(prompt: str, allow_skip: bool = False) -> Optional[str]:
    """
    Ask for a non-empty string. If allow_skip=True, empty input returns None.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        if allow_skip:
            return None
        print("Please enter a value.")


def admin_menu() -> None:
    """Display the admin menu loop."""
    while True:
        print("""
==== Admin Menu ====
1) Create user
2) List users
3) View user by ID
4) Update user by ID
5) Delete user by ID
6) Change my admin password
0) Logout
""")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            print("\n-- Create User --")
            username = prompt_nonempty("Username: ")
            full_name = prompt_nonempty("Full name: ")
            email = prompt_nonempty("Email: ")
            role = ""
            while role not in ("admin", "user"):
                role = input("Role ('admin' or 'user'): ").strip().lower()
            password = getpass.getpass("Temporary password: ").strip()

            try:
                new_id = create_user(username, full_name, email, role, password)
                print(f"Created user with ID: {new_id}")
            except sqlite3.IntegrityError as e:
                # likely UNIQUE constraint failed for username or email
                print(f"Error: {e}\n(Username and Email must be unique.)")

        elif choice == "2":
            print("\n-- All Users --")
            for row in list_users():
                print(f"ID={row['id']} | {row['username']} | {row['full_name']} | {row['email']} | role={row['role']} | created={row['created_at']}")

        elif choice == "3":
            try:
                user_id = int(prompt_nonempty("Enter user ID: "))
            except ValueError:
                print("ID must be a number.")
                continue
            row = read_user_by_id(user_id)
            if row:
                print(f"\nID: {row['id']}\nUsername: {row['username']}\nFull name: {row['full_name']}\nEmail: {row['email']}\nRole: {row['role']}\nCreated: {row['created_at']}\n")
            else:
                print("No user found with that ID.")

        elif choice == "4":
            print("\n-- Update User --")
            try:
                user_id = int(prompt_nonempty("User ID to update: "))
            except ValueError:
                print("ID must be a number.")
                continue

            # Optional fields (press Enter to skip)
            full_name = prompt_nonempty("New full name (Enter to skip): ", allow_skip=True)
            email = prompt_nonempty("New email (Enter to skip): ", allow_skip=True)

            role = None
            role_input = input("New role 'admin'/'user' (Enter to skip): ").strip().lower()
            if role_input in ("admin", "user"):
                role = role_input

            change_pw = input("Change password? (y/N): ").strip().lower() == "y"
            new_password = None
            if change_pw:
                new_password = getpass.getpass("New password: ").strip()

            try:
                update_user(user_id, full_name=full_name, email=email, role=role, new_password=new_password)
                print("User updated.\n")
            except sqlite3.IntegrityError as e:
                print(f"Error: {e}\n(Username and Email must be unique.)")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "5":
            print("\n-- Delete User --")
            try:
                user_id = int(prompt_nonempty("User ID to delete: "))
            except ValueError:
                print("ID must be a number.")
                continue

            confirm = input(f"Are you sure you want to DELETE user #{user_id}? (type 'DELETE' to confirm): ").strip()
            if confirm == "DELETE":
                delete_user(user_id)
                print("User deleted (if it existed).")
            else:
                print("Delete cancelled.")

        elif choice == "6":
            print("\n-- Change My Admin Password --")
            current_username = "admin"  # Minimal demo: assume admin is changing own password
            # If you have multiple admins, you can ask for username here or track the logged-in admin name.
            user = read_user_by_username(current_username)
            if user is None:
                print("Admin user not found.")
                continue
            old_pw = getpass.getpass("Current password: ").strip()
            if not verify_password(old_pw, user["salt"], user["password_hash"]):
                print("Current password incorrect.")
                continue
            new_pw = getpass.getpass("New password: ").strip()
            update_user(user["id"], new_password=new_pw)
            print("Password changed.")

        elif choice == "0":
            print("Logging out...\n")
            break
        else:
            print("Invalid option.")


def user_menu(logged_in_user: sqlite3.Row) -> None:
    """Display the normal user menu loop (view/update own profile, change password)."""
    while True:
        print(f"""
==== User Menu (you are: {logged_in_user['username']}) ====
1) View my profile
2) Update my profile (name/email)
3) Change my password
0) Logout
""")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            me = read_user_by_id(logged_in_user["id"])
            print(f"\nID: {me['id']}\nUsername: {me['username']}\nFull name: {me['full_name']}\nEmail: {me['email']}\nRole: {me['role']}\nCreated: {me['created_at']}\n")

        elif choice == "2":
            full_name = prompt_nonempty("New full name (Enter to skip): ", allow_skip=True)
            email = prompt_nonempty("New email (Enter to skip): ", allow_skip=True)
            try:
                update_user(logged_in_user["id"], full_name=full_name, email=email)
                print("Profile updated.\n")
            except sqlite3.IntegrityError as e:
                print(f"Error: {e}\n(Email must be unique.)")

        elif choice == "3":
            old_pw = getpass.getpass("Current password: ").strip()
            if not verify_password(old_pw, logged_in_user["salt"], logged_in_user["password_hash"]):
                print("Current password incorrect.")
                continue
            new_pw = getpass.getpass("New password: ").strip()
            update_user(logged_in_user["id"], new_password=new_pw)
            print("Password changed.\n")

        elif choice == "0":
            print("Logging out...\n")
            break
        else:
            print("Invalid option.")


# ---------- Main Program ----------

def main() -> None:
    """Entry-point: initialize DB, then show login, then role-specific menus."""
    init_db()
    while True:
        user = login()
        if user is None:
            continue

        # Refresh row after login in case user was changed elsewhere
        user = read_user_by_username(user["username"])
        if user["role"] == "admin":
            admin_menu()
        else:
            user_menu(user)


if __name__ == "__main__":
    main()
