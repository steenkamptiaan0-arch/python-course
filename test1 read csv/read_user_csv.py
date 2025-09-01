import csv, os, time, random
from password_generator import password_game
from RPS2 import rps
from Number_guessing_game import number_guessing_game

# ----------------------
# Global Config
# ----------------------
FILENAME = "test1 read csv/users.csv"
FIELDS = ["id", "name", "verify_otp", "timestamp", "games"]  # <-- added 'games'
ADMIN_PASSWORD = "admin123"  # <-- change this to something secure

# numeric codes -> labels for display
GAME_LABELS = {
    "1": "Password Generator Game",
    "2": "RPS Game",
    "3": "Number Guessing Game",
}

# ----------------------
# Helpers
# ----------------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def init_file():
    """Create CSV with headers if missing and migrate older schema."""
    os.makedirs(os.path.dirname(FILENAME), exist_ok=True)
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
    else:
        migrate_file_schema()  # ensure 'games' column exists

def migrate_file_schema():
    """If CSV exists without 'games' column, add it with default '1,2,3'."""
    with open(FILENAME, "r", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames or []
        if "games" in fieldnames:
            return  # already good
        rows = list(reader)

    # add default games to each row and rewrite file with new header
    for row in rows:
        row["games"] = "1,2,3"
    with open(FILENAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def read_all_rows():
    with open(FILENAME, "r", newline="") as file:
        return list(csv.DictReader(file))

def write_all_rows(rows):
    with open(FILENAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def get_all_ids():
    try:
        return [int(r["id"]) for r in read_all_rows() if str(r.get("id", "")).isdigit()]
    except FileNotFoundError:
        return []

def generate_new_id():
    ids = get_all_ids()
    return max(ids) + 1 if ids else 1

def get_user_by_id(user_id: int):
    for row in read_all_rows():
        if row["id"] == str(user_id):
            return row
    return None

def get_user_by_name(name: str):
    for row in read_all_rows():
        if row["name"] == name:
            return row
    return None

def parse_games(value: str) -> set[str]:
    """Parse '1,2,3' -> {'1','2','3'} with validation."""
    if not value:
        return set()
    allowed = {x.strip() for x in value.split(",")}
    return {g for g in allowed if g in {"1","2","3"}}

def games_to_label_list(games_set: set[str]) -> str:
    return ", ".join(GAME_LABELS[g] for g in sorted(games_set))

# ----------------------
# User Functions
# ----------------------

def add_user(name):
    """Add new user to CSV (default: all games allowed)."""
    user_id = generate_new_id()
    row = {
        "id": user_id,
        "name": name,
        "verify_otp": "Not Verified",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "games": "1,2,3",  # default: all games; admin can restrict later
    }
    rows = read_all_rows()
    rows.append({k: str(v) for k, v in row.items()})
    write_all_rows(rows)
    return user_id


def generate_otp(length=4):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def verify_otp_process(user_id, otp, attempts=3, ttl=120):
    """Verify OTP and update CSV with the actual code if success."""
    start_time = time.time()
    while attempts > 0:
        if time.time() - start_time > ttl:
            print("⏰ Code expired.")
            return False
        entered = input("Enter the 4-digit verification code: ").strip()
        if entered == otp:
            print("✅ Verified!\n")
            update_user_verification(user_id, otp)
            return True
        attempts -= 1
        print(f"❌ Wrong. {attempts} tries left.")
    return False

def update_user_verification(user_id, otp):
    """Update CSV row with verified OTP."""
    rows = read_all_rows()
    for row in rows:
        if row["id"] == str(user_id):
            row["verify_otp"] = otp
            row["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
            break
    write_all_rows(rows)

# ----------------------
# Admin Functions
# ----------------------

def verify_admin_password(attempts=3):
    """Prompt for admin password, allow up to `attempts` tries."""
    while attempts > 0:
        pwd = input("Enter admin password: ").strip()
        if pwd == ADMIN_PASSWORD:
            print("✅ Access granted!\n")
            time.sleep(1)
            return True
        else:
            attempts -= 1
            print(f"❌ Wrong password. {attempts} tries left.")
    print("🚫 Access denied.")
    time.sleep(1)
    return False

def show_all_users():
    rows = read_all_rows()
    for row in rows:
        print("─" * 40)
        for key in FIELDS:
            label = key.replace("_", " ").title()
            value = row.get(key, "")
            if key == "games":
                value = games_to_label_list(parse_games(value))
            print(f"{label:<14}: {value}")
    print("─" * 40)

def delete_user(user_id):
    rows = [r for r in read_all_rows() if r["id"] != str(user_id)]
    write_all_rows(rows)

def update_user_games(user_id: int, games_list: list[str]):
    """Persist allowed games (e.g. ['1','3']) for the user."""
    cleaned = ",".join(sorted({g for g in games_list if g in {"1","2","3"}}))
    rows = read_all_rows()
    for row in rows:
        if row["id"] == str(user_id):
            row["games"] = cleaned
            row["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
            break
    write_all_rows(rows)

def admin_set_user_games():
    """Prompt admin to set allowed games for a specific user."""
    try:
        uid = int(input("Enter user ID to update: ").strip())
    except ValueError:
        print("ID must be a number.")
        time.sleep(1)
        return

    user = get_user_by_id(uid)
    if not user:
        print("No such user.")
        time.sleep(1)
        return

    current = parse_games(user.get("games", "1,2,3"))
    print("\nCurrent allowed games:", games_to_label_list(current) or "(none)")
    print("Available codes:")
    for code, label in GAME_LABELS.items():
        print(f"  {code} = {label}")
    raw = input("Enter allowed codes separated by commas (e.g. 1,3): ").strip()
    new_set = parse_games(raw)
    if not new_set:
        print("No valid codes entered; leaving unchanged.")
        time.sleep(1)
        return

    update_user_games(uid, list(new_set))
    print("✅ Updated.")
    time.sleep(1)

# ----------------------
# Interfaces
# ----------------------
def user_interface():
    name = str.title(input("Enter your name: ").strip())
    existing_user = get_user_by_name(name)

    if existing_user:
        print(f"Welcome back, {name}! Your ID is {existing_user['id']}\n")
        otp = generate_otp()
        print(f"(DEBUG) OTP sent: {otp}")
        if verify_otp_process(existing_user['id'], otp):
            # fetch fresh row (verify_otp updated)
            user = get_user_by_id(int(existing_user["id"]))
            allowed = parse_games(user.get("games", "1,2,3"))
            user_game_menu(allowed)
        else:
            print("🚫 Verification failed.")
    else:
        user_id = add_user(name)
        print(f"Welcome, {name}! Your ID is {user_id}")
        otp = generate_otp()
        print(f"(DEBUG) OTP sent: {otp}")
        if verify_otp_process(user_id, otp):
            user = get_user_by_id(user_id)
            allowed = parse_games(user.get("games", "1,2,3"))
            user_game_menu(allowed)
        else:
            print("🚫 Verification failed.")

def admin_interface():
    while True:
        clear()
        print("=== ADMIN MENU ===")
        print("1) Show all users")
        print("2) Delete user")
        print("3) Set user allowed games")  # <-- new
        print("0) Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            show_all_users()
            input("Press Enter to continue...")
        elif choice == "2":
            uid = input("Enter ID to delete: ").strip()
            delete_user(uid)
            print("✅ User deleted")
            time.sleep(1)
        elif choice == "3":
            admin_set_user_games()
        elif choice == "0":
            break
        else:
            print("Invalid choice")
            time.sleep(1)

# ----------------------
# User Games Menu
# ----------------------s
def user_game_menu(allowed: set[str]):
    clear()
    if not allowed:
        print("Your account currently has no games enabled. Please contact an admin.")
        time.sleep(2)
        return

    while True:
        print("\n=== GAME MENU ===")
        if "1" in allowed: print("1. Password Generator Game")
        if "2" in allowed: print("2. RPS Game (rock-paper-scissors)")
        if "3" in allowed: print("3. Number Guessing Game")
        print("0. Logout / Exit")

        choice = input("Choose: ").strip()
        if choice == "0":
            print("👋 Logged out. Goodbye!")
            break

        if choice == "1" and "1" in allowed:
            password_game()
        elif choice == "2" and "2" in allowed:
            rps()
        elif choice == "3" and "3" in allowed:
            number_guessing_game()
        else:
            print("❌ Not allowed or invalid choice.")
            time.sleep(1)

# ----------------------
# Main
# ----------------------
def main():
    init_file()
    while True:
        clear()
        print("=== MAIN MENU ===")
        print("Please select a option 1 to 3")
        print("1) User")
        print("2) Admin")
        print("0) Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            user_interface()
        elif choice == "2":
            if verify_admin_password():
                admin_interface()
        elif choice == "0":
            print("👋 Exiting program. Goodbye!")
            break
        else:
            print("❌ Invalid choice")
            time.sleep(1)


if __name__ == "__main__":
    main()
