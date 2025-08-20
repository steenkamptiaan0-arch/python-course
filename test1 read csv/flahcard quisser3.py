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
#--date Model--
def default_data():
    return {
        'decks': {},
        'meta': {'created': datetime.utcnow().isoformat()}
    }

def load_data():
    if not os.path.exists(DATAFILE):
        return default_data()
    with open(DATAFILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATAFILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def make_card(question, answer):
    return {
        'question': question.strip(),
        'answer': answer.strip(),
        'box': 1,           # Leitner box (1 = new, 2 = learning, 3 = learned)
        'last_reviewed': None,
        'streak': 0
    }

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