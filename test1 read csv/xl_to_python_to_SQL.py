import os
import time
import threading
import pandas as pd
import pyodbc

# Excel file path
FILENAME = "test1 read csv/users2.xlsx"

# ----------------------------------
# Database and table setup 
# ----------------------------------
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=.\SQLEXPRESS;"
    "Database=Playground;"
    "Trusted_Connection=yes;"
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Ensure Users table exists
cursor.execute("""
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Users' AND xtype='U')
CREATE TABLE Users (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(100),
    surname NVARCHAR(100),
    password NVARCHAR(100),
    email NVARCHAR(255)
)
""")
conn.commit()

# ----------------------------------
# Helpers
# ----------------------------------
def read_excel():
    return pd.read_excel(FILENAME)

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicates and clean up data before sync"""
    required_cols = ["Name", "Surname", "Password", "Email"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = ""

    # Convert to string and trim spaces
    df = df.astype(str).fillna("")
    df["Name"] = df["Name"].str.strip().str.title()
    df["Surname"] = df["Surname"].str.strip().str.title()
    df["Password"] = df["Password"].str.strip()
    df["Email"] = df["Email"].str.strip().str.lower()

    # Remove duplicates based on (Name, Surname, Email)
    df = df.drop_duplicates(subset=["Name", "Surname", "Email"], keep="first")

    # Save cleaned file back to Excel
    df.to_excel(FILENAME, index=False)
    return df

def update_sql():
    """Push Excel data to SQL Server"""
    df = read_excel()
    df = clean_dataframe(df)

    for _, row in df.iterrows():
        cursor.execute(
            "SELECT COUNT(*) FROM Users WHERE username = ? AND surname = ? AND email = ?",
            row['Name'], row['Surname'], row['Email']
        )
        result = cursor.fetchone()
        if result is None or result[0] == 0:
            try:
                cursor.execute(
                    "INSERT INTO Users (username, surname, password, email) VALUES (?, ?, ?, ?)",
                    row['Name'], row['Surname'], row['Password'], row['Email']
                )
                print(f"Inserted new user: {row['Name']} {row['Surname']}")
            except Exception as e:
                print(f"Skipping row due to error: {e}")
    conn.commit()

def auto_sync(interval=5):
    """Automatically sync Excel to SQL Server every X seconds and detect changes"""
    last_modified = os.path.getmtime(FILENAME)
    while True:
        try:
            current_modified = os.path.getmtime(FILENAME)
            if current_modified != last_modified:
                update_sql()
                last_modified = current_modified
        except FileNotFoundError:
            # File might be deleted or not exist yet
            pass
        time.sleep(interval)

def add_user():
    """Add a new user via CLI"""
    print("Enter new user details:")
    name = input("Name: ").strip()
    surname = input("Surname: ").strip()
    password = input("Password: ").strip()
    email = input("Email: ").strip()

    df = read_excel()
    new_row = {"Name": name, "Surname": surname, "Password": password, "Email": email}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df = clean_dataframe(df)
    print(f"✅ User {name} added to Excel file.")
    update_sql()

def read_all_rows():
    """Fetch all users from SQL Server as list of dicts"""
    cursor.execute("SELECT username, surname, password, email FROM Users")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    return [dict(zip(columns, row)) for row in rows]

def show_all_users():
    """Print all users in SQL Server"""
    rows = read_all_rows()
    if not rows:
        print("No users found in the database.")
        return
    for row in rows:
        print("─" * 40)
        for key, value in row.items():
            label = key.replace("_", " ").title()
            print(f"{label:<14}: {value}")
    print("─" * 40)

# ----------------------------------
# Ensure Excel file exists
# ----------------------------------
os.makedirs(os.path.dirname(FILENAME), exist_ok=True)
if not os.path.isfile(FILENAME):
    df = pd.DataFrame(columns=["Name", "Surname", "Password", "Email"])
    df.to_excel(FILENAME, index=False)
    print(f"📄 Created new Excel file: {FILENAME}")

# ----------------------------------
# Start auto-sync in background
# ----------------------------------
threading.Thread(target=auto_sync, daemon=True).start()
print("🚀 Auto-Sync started in the background (checks every 5 seconds)")

# ----------------------------------
# Menu
# ----------------------------------
while True:
    print("\nMenu:")
    print("1. Add new user")
    print("2. Sync Excel to SQL Server (manual)")
    print("3. Show all users")
    print("0. Exit")
    choice = input("Enter choice (0-3): ").strip()

    if choice == "1":
        add_user()
    elif choice == "2":
        print("🔄 Syncing Excel to SQL Server...")
        update_sql()
    elif choice == "3":
        print("📋 Showing all users in SQL Server:")
        show_all_users()
    elif choice == "0":
        print("👋 Exiting...")
        break
    else:
        print("⚠️ Invalid choice!")
