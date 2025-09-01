import sys
import random
from enum import Enum

def rps():
    game_count = 0
    player_wins = 0
    python_wins = 0

    class RPS(Enum):
        ROCK = 1
        PAPER = 2
        SCISSORS = 3

    while True:
        playerchoice = input(
            "\nEnter... \n1 for Rock,\n2 for Paper, or \n3 for Scissors:\n\n"
        )

        if playerchoice not in ["1", "2", "3"]:
            print("❌ You must enter 1, 2, or 3.")
            continue

        player = int(playerchoice)
        computer = random.randint(1, 3)

        print("\nYou chose " + str(RPS(player)).replace('RPS.', '').title() + ".")
        print("Python chose " + str(RPS(computer)).replace('RPS.', '').title() + ".\n")

        if (player == 1 and computer == 3) or \
           (player == 2 and computer == 1) or \
           (player == 3 and computer == 2):
            player_wins += 1
            result = "🎉 You win!"
        elif player == computer:
            result = "😲 Tie game!"
        else:
            python_wins += 1
            result = "🐍 Python wins!"

        game_count += 1

        print(result)
        print(f"\nGame count: {game_count}")
        print(f"Player wins: {player_wins}")
        print(f"Python wins: {python_wins}")

        playagain = input("\nPlay again? (Y = Yes, Q = Quit): ").strip().lower()
        if playagain == "q":
            print("\n🎉🎉🎉🎉")
            print("Thank you for playing!\n")
            print("Bye! 👋")
            break
            

# Run
if __name__ == "__main__":
    rps()