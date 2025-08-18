import random
import string
import time

text_speed = 0.04  # default text speed

def print_slow(text, delay=None):
    """Prints text slowly like a narrator"""
    if delay is None:
        delay = text_speed
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def generate_password(upper_count=0, lower_count=0, number_count=0, symbol_count=0):
    """Generate a password with exact character amounts chosen by the user"""
    characters = []
    characters += random.choices(string.ascii_uppercase, k=upper_count)
    characters += random.choices(string.ascii_lowercase, k=lower_count)
    characters += random.choices(string.digits, k=number_count)
    characters += random.choices(string.punctuation, k=symbol_count)

    if not characters:
        return "(Error: No character sets chosen!)"

    random.shuffle(characters)  # Shuffle to mix randomness
    return ''.join(characters)

def password_game(first_time=True):
    global text_speed

    if first_time:
        print_slow("🔒 Welcome to the Magical Password Forge! 🔒")
        time.sleep(1)

    print_slow("\nNow, brave adventurer, decide how many of each character type your password shall contain:")

    # Ask counts for each character type
    while True:
        try:
            upper_count = int(input("How many UPPERCASE letters? "))
            lower_count = int(input("How many lowercase letters? "))
            number_count = int(input("How many numbers? "))
            symbol_count = int(input("How many symbols? "))
            total = upper_count + lower_count + number_count + symbol_count
            if total < 4:
                print_slow("⚠️ Password too short! Let's try again with at least 4 characters total.")
                continue
            break
        except ValueError:
            print_slow("😅 Oops! Please enter numbers only.")

    print_slow("\n🧙‍♂️ Forging your password in the fires of randomness...")
    time.sleep(1.5)

    password = generate_password(upper_count, lower_count, number_count, symbol_count)

    print_slow(f"\n✨ Your new powerful password is: {password}")
    print(" ")
    print_slow("💡 Tip: Copy it somewhere safe, adventurer!")

    print_slow("\nThanks for using the Password Forge! 🔑")

def main():
    first_time = True
    while True:
        password_game(first_time)
        first_time = False  # Skip welcome on next runs
        again = input("\nDo you want to forge another password? (y/n): ").lower()
        if again != 'y':
            print_slow("\nGoodbye! Stay safe and secure! 🔐")
            break

if __name__ == "__main__":
    main()
