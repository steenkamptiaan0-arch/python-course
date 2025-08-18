import random
import time

def roll_dice(sides=12):
    return random.randint(1, sides)

def print_slow(text, delay=0.04):
    """Print text slowly like an RPG narrator"""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def battle():
    print_slow("⚔️ Welcome, brave adventurer, to the Dice Arena! ⚔️")
    player_name = input("\nWhat is your hero's name? 🧙‍♂️: ")
    
    print_slow(f"\nGreetings, {player_name}! You will face the evil Dungeon Monster...")
    time.sleep(1)
    
    player_hp = 50
    monster_hp = 50
    
    while player_hp > 0 and monster_hp > 0:
        input("\n🎲 Press ENTER to roll the dice for your attack...")
        player_roll = roll_dice(12)
        monster_roll = roll_dice(12)
        
        print_slow(f"{player_name} rolls a {player_roll}!")
        print_slow(f"Monster rolls a {monster_roll}!")
        
        if player_roll > monster_roll:
            dmg = player_roll - monster_roll
            monster_hp -= dmg
            print_slow(f"🔥 You strike the monster for {dmg} damage! Monster HP: {monster_hp}")
        elif monster_roll > player_roll:
            dmg = monster_roll - player_roll
            player_hp -= dmg
            print_slow(f"💀 The monster hits YOU for {dmg} damage! Your HP: {player_hp}")
        else:
            print_slow("🤝 It's a draw! Both stand their ground.")
        
        time.sleep(1.5)
    
    if player_hp > 0:
        print_slow("\n🏆 Victory! You have slain the monster and claimed eternal glory!")
    else:
        print_slow("\n☠️ You have been defeated... The monster laughs as darkness falls...")

def main():
    while True:
        battle()
        again = input("\nDo you want to play again? (y/n): ").lower()
        if again != 'y':
            print_slow("\nThanks for playing! Farewell, adventurer. 🌟")
            break

if __name__ == "__main__":
    main()

