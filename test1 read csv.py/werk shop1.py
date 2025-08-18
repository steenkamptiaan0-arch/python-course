import random

def pheno_no(nomber_count=0):
    characters = []
    characters += random.choices("0123456789", k=nomber_count)
    
    if not characters:
        return "(Error: No character sets chosen!)"

    random.shuffle(characters)  # Shuffle to mix randomness
    return ''.join(characters)
def pheno_game(first_time=True):
    if first_time:
        print("New Pheno Nomber")

        print("\nNow, brave adventurer, decide how many of each character type your password shall contain:")

        while True:
            try:
                nomber_count = int(input("Please enter ..."))
                if nomber_count < 1:
                    print("⚠️ Password too short! Let's try again with at least 1 character.")
                    continue
            except ValueError:
                print("😅 Oops! Please enter numbers only.")