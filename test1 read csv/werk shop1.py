# module imports
import os
import csv
import string
import time
import random
import subprocess
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# the code below is a phone number and verification code generator
def numbre(): # Number generation function
    """Generate a SA-style random phone number (10 digits, starting with 0)."""
    return "0" + ''.join(str(random.randint(0, 9)) for _ in range(9))# "0" + "".join() creates a string from the list of characters and str(random.randint(0, 9) for _ in range(9) is how many numbers you want to generate

def generate_otp(length=5): # verification code generation function
    """Generate a numeric OTP of given length."""
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length)) #''.join() creates a string from the list of characters and random.choice(characters) for _ in range(length) is how many characters you want to generate

def verify_otp(expected_otp, attempts=4, ttl_seconds=120): # checking the verification code
    """
    Prompt the user to enter the OTP.
    - attempts: how many tries are allowed
    - ttl_seconds: how long the OTP is valid
    Returns True if verified, False otherwise.
    """
    start_time = time.time()

    while attempts > 0:
        # Check expiry before asking again
        if time.time() - start_time > ttl_seconds:
            print("⏰ The code expired. Please request a new one.")
            return False

        entered = input("Enter the 4-digit verification code: ").strip()

        # Optional: also allow the user to quit early
        if entered.lower() in {"q", "quit", "exit"}:
            print("Exited verification.")
            return False

        if entered == expected_otp:
            print("✅ Verified! Welcome aboard.")
            return True

        attempts -= 1
        # Show how many attempts are left
        if attempts > 0:
            print(f"❌ Incorrect. {attempts} attempt(s) left.")
        else:
            print("🚫 Verification failed. No attempts left.")
    return False

def clear():
     """Clear the console screen."""
os.system('cls' if os.name == 'nt' else 'clear')  # Clear console for Windows or Unix-like systems

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# save_to_csv function ( saveing system)
def save_to_csv(path, row_dict, headers):
    """Append a row to CSV, creating folder and header if needed."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    file_exists = os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_dict)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  

# main interface
def main():
    # 1) Ask name (clean it up nicely)
    name = str.title(input("Enter your name: "))
    print(f"Welcome, {name}!")

    # 2) Generate and show a random phone number
    saved_number = numbre()
    print(f"This is your phone number: {saved_number}")
    print("Your saved random number is:", saved_number)

    # 3) "Send" a 4-digit OTP (for real apps, send via SMS/email)
    otp = generate_otp(4)
    print(f"(DEBUG) Verification code sent to: {otp}")

    # 4) Verify user input
    verified = verify_otp(otp, attempts=4, ttl_seconds=120)

    # If not verified → stop program
    if not verified:
        print("🚫 Verification failed. Exiting program.")
        return  

    # 5) Save result to CSV (same folder name you used)
    csv_path = os.path.join("test1 read csv", "random_number.csv")
    save_to_csv(
        csv_path,
        {
            "name": name,
            "phone": saved_number,
            "verified": verified,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        },
        headers=["name", "phone", "verified", "timestamp"]
    )
    print(f"📝 Saved verification record to: {csv_path}\n") 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Flashcard Quizzer gane

# Fcq = "Flashcard Quizzer"


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # --- Only show menu AFTER verification ---
    while True:
        print("✨ Welcome to the Main Menu ✨")
        print("1. Flashcard Quizzer Game")
        print("2. Logout / Exit")
        choice = input("Choose an option (1 or 2): ").strip()

        if choice == "1":
            print("✅ You chose to play the Flashcard Quizzer Game!\n")
            subprocess.run(["python", "test1 read csv/password generater.py"])
            # You can add more features inside here later
        elif choice == "2":
            print("👋 Logged out. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1 or 2.")


if __name__ == "__main__":
                main()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

