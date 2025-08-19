import random
from enum import Enum


class RPS(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

options = ["1", "2", "3"]

def R_P_S():
    print("Welcome to Rock, Paper, Scissors!")

while True:
    user_choice = input("Enter 1, 2, or 3 (or 'quit' to stop): ").lower()
    # quit option
    if user_choice == "quit":
        print("Thanks for playing!")
        break
    if user_choice not in options:
        print("Invalid choice. Please try again.")
        continue
# Get computer's choice desplay
    computer_choice = random.choice(options)
    print("")
    print("You chose " + str(RPS(int(user_choice))).replace('RPS.', '') + ".")
    print("Python chose " + str(RPS(int(computer_choice))).replace('RPS.', '') + ".")
    print("")
    # Determine the winner
    if user_choice == computer_choice:
        print("It's a tie!")
    elif (
        (user_choice == "1" and computer_choice == "3") or
        (user_choice == "2" and computer_choice == "1") or
        (user_choice == "3" and computer_choice == "2")):
        print("You win!")
    else:
        print("You lose!")

if __name__ == "__main__":
    R_P_S()