# Functions.py
import pyodbc
import os

# SQL Server connection string
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=.\SQLEXPRESS;" # type: ignore
    "Database=Playground;"
    "Trusted_Connection=yes;"
)

TABLE_NAME = "SQL_test2"

# Helper function to connect to the database
def get_connection():
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# Clear the console
def clear():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Mac/Linux
        os.system('clear')

# Ensure table exists, otherwise create it
def ensure_table_exists():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"""
                IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{TABLE_NAME}')
                BEGIN
                    CREATE TABLE {TABLE_NAME} (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        username VARCHAR(100) UNIQUE NOT NULL,
                        profile_data VARCHAR(MAX)
                    )
                END
            """)
            conn.commit()
            print(f"Table '{TABLE_NAME}' is ready.")
        except Exception as e:
            print(f"Error ensuring table exists: {e}")
        finally:
            conn.close()

# Add a new user
def add_user(username):
    ensure_table_exists()
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {TABLE_NAME} (username) VALUES (?)", username)
            conn.commit()
            print(f"User '{username}' added successfully.")
        except pyodbc.IntegrityError:
            print(f"Error: User '{username}' already exists.")
        except Exception as e:
            print(f"Error adding user: {e}")
        finally:
            conn.close()

# Remove a user by ID
def remove_user(user_id):
    ensure_table_exists()
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = ?", user_id)
            conn.commit()
            if cursor.rowcount == 0:
                print(f"No user found with ID {user_id}.")
            else:
                print(f"User with ID {user_id} removed successfully.")
        except Exception as e:
            print(f"Error removing user: {e}")
        finally:
            conn.close()

# View all users
def view_users():
    ensure_table_exists()
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT id, username FROM {TABLE_NAME}")
            users = cursor.fetchall()
            if users:
                print("All users:")
                for user in users:
                    print(f"ID: {user[0]} | Username: {user[1]}")
            else:
                print("No users found.")
        except Exception as e:
            print(f"Error retrieving users: {e}")
        finally:
            conn.close()

# Get all users as a list of (id, username)
def get_all_users():
    ensure_table_exists()
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT id, username FROM {TABLE_NAME}")
            users = [(row[0], row[1]) for row in cursor.fetchall()]
            return users
        except Exception as e:
            print(f"Error retrieving users: {e}")
            return []
        finally:
            conn.close()
    return []

# View a user's profile by ID
def view_profile(user_id):
    ensure_table_exists()
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT id, username, profile_data FROM {TABLE_NAME} WHERE id = ?", user_id)
            user = cursor.fetchone()
            if user:
                print(f"ID: {user[0]} | Username: {user[1]} | Profile Data: {user[2]}")
            else:
                print(f"User with ID {user_id} not found.")
        except Exception as e:
            print(f"Error retrieving profile: {e}")
        finally:
            conn.close()

# Update a user's profile by ID
def update_profile(user_id, new_data):
    ensure_table_exists()
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {TABLE_NAME} SET profile_data = ? WHERE id = ?", new_data, user_id)
            conn.commit()
            if cursor.rowcount == 0:
                print(f"No user found with ID {user_id}.")
            else:
                print(f"Profile for user ID {user_id} updated successfully.")
        except Exception as e:
            print(f"Error updating profile: {e}")
        finally:
            conn.close()
