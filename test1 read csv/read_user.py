check if file exists
def init_file():
    """Create the CSV file if it doesn’t exist, with headers."""
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()

# ID generator
def get_next_id():
    """Get the next available ID (auto-increment)."""
    try:
        with open(FILENAME, mode="r") as file:
            reader = csv.DictReader(file)
            ids = [int(row["id"]) for row in reader]
            return max(ids) + 1 if ids else 1
    except FileNotFoundError:
        return 1

# adds a new user
def add_user(name, email):
    """Add a new user with auto-generated ID."""
    user_id = get_next_id()
    with open(FILENAME, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writerow({"id": user_id, "name": name, "email": email})
    print(f"User added: {user_id}, {name}, {email}")

# listing users
def list_users():
    """Display all users."""
    with open(FILENAME, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)

# edit user details
def edit_user(user_id, new_name=None, new_email=None):
    """Edit a user’s name/email by ID."""
    rows = []
    with open(FILENAME, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["id"] == str(user_id):
                if new_name:
                    row["name"] = new_name
                if new_email:
                    row["email"] = new_email
            rows.append(row)

    with open(FILENAME, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"User {user_id} updated!")


def delete_user(user_id):
    """Delete a user by ID."""
    rows = []
    with open(FILENAME, mode="r") as file:
        reader = csv.DictReader(file)
        rows = [row for row in reader if row["id"] != str(user_id)]

    with open(FILENAME, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"User {user_id} deleted!")