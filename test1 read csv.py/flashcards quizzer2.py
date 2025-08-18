#!/usr/bin/env python3
"""
Flashcard Quizzer — Fun, friendly, and easy to use terminal flashcard app.
Saves decks to a JSON file so your progress persists between runs.
Features:
 - Multiple topics (decks)
 - Add / edit / delete cards
 - Quiz mode with multiple-choice questions
 - Simple spaced-repetition (3-box Leitner-like system)
 - Hints, streaks, score, and celebratory messages
 - Import a small sample deck to get started
"""

import json
import os
import random
import sys
import time
from datetime import datetime, timedelta

DATAFILE = os.path.expanduser('~/flashcard_quizzer_data.json')  # saved in the user's home folder

# --- Utilities ---
def print_slow(text, delay=0.01, end='\\n'):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print(end, end='')

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def read_choice(prompt, choices):
    """Read a user choice from a list of allowed single-character options."""
    choices = [c.lower() for c in choices]
    while True:
        ch = input(prompt).strip().lower()
        if ch in choices:
            return ch
        print("That's not one of the options — try again.")

# --- Data model ---
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

# --- Sample deck ---
SAMPLE = {
    'General Knowledge': [
        ('Capital of France?', 'Paris'),
        ('2 + 2 * 2 = ?', '6'),
        ('H2O is the chemical formula for?', 'Water'),
        ('Largest planet in the Solar System?', 'Jupiter'),
    ]
}

# --- Core features ---
def list_decks(data):
    decks = list(data['decks'].keys())
    if not decks:
        print("You have no decks yet. Try importing the sample deck (option 'i').")
        return []
    for i, name in enumerate(decks, 1):
        print(f"  {i}. {name} ({len(data['decks'][name])} cards)")
    return decks

def create_deck(data):
    name = input("Name your new deck: ").strip()
    if not name:
        print("Can't be empty.")
        return
    if name in data['decks']:
        print("A deck with that name already exists.")
        return
    data['decks'][name] = []
    save_data(data)
    print(f"Deck '{name}' created. Add cards with option 'a'.")

def add_card_to_deck(data, deck_name):
    q = input("Enter the question (front of card): ").strip()
    if not q:
        print("Question can't be empty.")
        return
    a = input("Enter the answer (back of card): ").strip()
    if not a:
        print("Answer can't be empty.")
        return
    data['decks'][deck_name].append(make_card(q, a))
    save_data(data)
    print("Card added! 🎉")

def edit_card(data, deck_name):
    cards = data['decks'][deck_name]
    if not cards:
        print("No cards to edit.")
        return
    for i, c in enumerate(cards, 1):
        print(f"{i}. {c['question']} -> {c['answer']} (box {c['box']}, streak {c.get('streak',0)})")
    try:
        idx = int(input("Pick card number to edit: ")) - 1
        if not (0 <= idx < len(cards)):
            raise ValueError
    except Exception:
        print("Invalid number.")
        return
    q = input(f"New question (enter to keep): ").strip()
    a = input(f"New answer (enter to keep): ").strip()
    if q:
        cards[idx]['question'] = q
    if a:
        cards[idx]['answer'] = a
    save_data(data)
    print("Card updated. ✅")

def delete_card(data, deck_name):
    cards = data['decks'][deck_name]
    if not cards:
        print("No cards to delete.")
        return
    for i, c in enumerate(cards, 1):
        print(f"{i}. {c['question']} -> {c['answer']}")
    try:
        idx = int(input("Pick card number to delete: ")) - 1
        if not (0 <= idx < len(cards)):
            raise ValueError
    except Exception:
        print("Invalid number.")
        return
    confirm = input(f"Type 'yes' to delete card '{cards[idx]['question']}': ").strip().lower()
    if confirm == 'yes':
        cards.pop(idx)
        save_data(data)
        print("Deleted. 💥")
    else:
        print("Not deleted.")

def import_sample(data):
    for deck, cards in SAMPLE.items():
        if deck in data['decks']:
            print(f"Deck '{deck}' already exists — skipping.")
            continue
        data['decks'][deck] = [make_card(q, a) for q, a in cards]
        print(f"Imported sample deck '{deck}' with {len(cards)} cards.")
    save_data(data)

# --- Quiz logic ---
def due_cards(deck):
    """Return cards that are due for review. For simplicity: box 1 always due, box 2 due every 1 day, box 3 due every 3 days."""
    now = datetime.utcnow()
    due = []
    for c in deck:
        last = datetime.fromisoformat(c['last_reviewed']) if c['last_reviewed'] else None
        box = c.get('box', 1)
        if box == 1:
            due.append(c)
        elif box == 2:
            if not last or now - last >= timedelta(days=1):
                due.append(c)
        else:
            if not last or now - last >= timedelta(days=3):
                due.append(c)
    return due

def make_choices(cards, correct_answer, n=3):
    """Make n+1 choices including correct answer. Tries to pick plausible wrong answers."""
    pool = [c['answer'] for c in cards if c['answer'] != correct_answer]
    wrong = random.sample(pool, min(n, len(pool)))
    choices = wrong + [correct_answer]
    random.shuffle(choices)
    return choices

def quiz_deck(data, deck_name):
    deck = data['decks'][deck_name]
    if not deck:
        print("Deck empty — add some cards first.")
        return
    pool = due_cards(deck)
    if not pool:
        print("No cards are due for review right now. Nice! ✅")
        return
    random.shuffle(pool)
    score = 0
    total = len(pool)
    for c in pool:
        clear()
        print_slow("Question: " + c['question'], 0.005)
        choices = make_choices(deck, c['answer'], n=3)
        for i, ch in enumerate(choices, 1):
            print(f"  {i}. {ch}")
        hint = input("Type 'h' for a hint, or press Enter to answer: ").strip().lower()
        if hint == 'h':
            hint_text = c['answer'][0] + ('*' * (max(0, len(c['answer']) - 2))) + (c['answer'][-1] if len(c['answer']) > 1 else '')
            print("Hint:", hint_text)
        try:
            ans = int(input("Your choice number: ").strip())
            picked = choices[ans - 1]
        except Exception:
            print("Invalid choice — counted as incorrect.")
            picked = None
        correct = (picked == c['answer'])
        if correct:
            print("Correct! ✅")
            score += 1
            c['streak'] = c.get('streak', 0) + 1
            # promote box
            if c['box'] < 3 and random.random() < 0.9:  # small randomness to keep it lively
                c['box'] += 1
        else:
            print(f"Wrong — correct answer: {c['answer']}")
            c['streak'] = 0
            # demote box a bit
            if c['box'] > 1:
                c['box'] -= 1
        c['last_reviewed'] = datetime.utcnow().isoformat()
        print(f"Streak: {c.get('streak',0)}  |  Box: {c['box']}")
        input("Press Enter for the next card...")
    # summary
    clear()
    pct = int(score / total * 100) if total else 0
    print_slow(f"Session complete — {score}/{total} correct ({pct}%).", 0.003)
    if pct == 100:
        print(r""" 
  \o/   \o/   \o/
 🎉🎉🎉  CONGRATS! Perfect score!  🎉🎉🎉
        """)
    elif pct >= 70:
        print("Nice work — keep it up! ⭐")
    else:
        print("Good practice — you'll get there! 💪")
    save_data(data)

# --- Stats & utilities ---
def show_stats(data):
    total = sum(len(deck) for deck in data['decks'].values())
    boxes = {1:0,2:0,3:0}
    for deck in data['decks'].values():
        for c in deck:
            boxes[c.get('box',1)] += 1
    print(f"Total cards: {total}  |  Box1: {boxes[1]}  Box2: {boxes[2]}  Box3: {boxes[3]}")

def deck_menu(data, deck_name):
    while True:
        clear()
        print(f"--- Deck: {deck_name} ---")
        print("a) Add card    e) Edit card    d) Delete card")
        print("q) Quiz deck   s) Stats        b) Back to main menu")
        choice = read_choice("Choose an option: ", ['a','e','d','q','s','b'])
        if choice == 'a':
            add_card_to_deck(data, deck_name)
        elif choice == 'e':
            edit_card(data, deck_name)
        elif choice == 'd':
            delete_card(data, deck_name)
        elif choice == 'q':
            quiz_deck(data, deck_name)
        elif choice == 's':
            show_stats(data)
            input("Press Enter to continue...")
        elif choice == 'b':
            break

def main_menu():
    data = load_data()
    while True:
        clear()
        print("✨ Flashcard Quizzer ✨")
        print("Options:")
        print("  l) List decks    c) Create deck    i) Import sample deck")
        print("  o) Open deck     t) Tutorial       x) Exit")
        print()
        list_decks(data)
        choice = read_choice("Pick an option: ", ['l','c','i','o','t','x'])
        if choice == 'l':
            list_decks(data)
            input("Press Enter to continue...")
        elif choice == 'c':
            create_deck(data)
            input("Press Enter to continue...")
        elif choice == 'i':
            import_sample(data)
            input("Press Enter to continue...")
        elif choice == 'o':
            decks = list_decks(data)
            if not decks:
                input("Press Enter to continue...")
                continue
            try:
                idx = int(input("Pick deck number to open: ").strip()) - 1
                deck_name = decks[idx]
            except Exception:
                print("Invalid selection.")
                input("Press Enter to continue...")
                continue
            deck_menu(data, deck_name)
        elif choice == 't':
            run_tutorial(data)
        elif choice == 'x':
            print("Bye! 👋 Keep learning.")
            break

def run_tutorial(data):
    clear()
    print_slow("Welcome to Flashcard Quizzer — a friendly way to learn!", 0.005)
    print_slow("Tip: import the sample deck (option 'i') to try right away.", 0.005)
    print("Quick walkthrough:")
    print(" - Create a deck, add cards, then open the deck and quiz yourself.")
    print(" - Use hints with 'h' during quizzes. The system will promote cards you know and demote those you miss.")
    print("Have fun! 🎈")
    input("Press Enter to return to the main menu...")

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print('\\nInterrupted. Progress saved. Bye!')