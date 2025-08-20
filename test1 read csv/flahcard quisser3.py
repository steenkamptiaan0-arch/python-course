import json
import os
import random
import sys
import time
from datetime import datetime, timedelta

DATAFILE = os.path.expanduser('~/flashcard_quizzer_data.json')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#--Utility functions--
def read_choice(prompt, choices):
    choices = [c.lower() for c in choices]  # make all options lowercase
    while True:
        ch = input(prompt).strip().lower()  # get user input
        if ch in choices:
            return ch  # return valid input
        print("That's not one of the options — try again.")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear console for Windows or Unix-like systems
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# --Desplay menu--
def main_menu():
    # data = load_data()
    while True:
        clear()
        print("✨ Flashcard Quizzer ✨")
        print("l) List decks  c) Create deck  i) Import sample deck")
        print("o) Open deck   t) Tutorial      x) Exit")
        list_decks(data)
        choice = read_choice("Pick an option: ", ['l','c','i','o','t','x'])
        if choice=='l': list_decks(data); input("Enter...")
        elif choice=='c': create_deck(data); input("Enter...")
        elif choice=='i': import_sample(data); input("Enter...")
        elif choice=='o':
            decks=list_decks(data)
            idx=int(input("Pick deck number to open: ").strip())-1
            deck_menu(data,decks[idx])
        elif choice=='t': run_tutorial(data)
        elif choice=='x': print("Bye! 👋");
        break
if __name__ == "__main__":
    main_menu()