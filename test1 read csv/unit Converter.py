import time
import random

units = ["Celsius", "Fahrenheit", "Kilometers", "Miles", "Kilograms", "Pounds"]

def slow_print(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def convert(value, unit_from, unit_to):
    if unit_from == "Celsius" and unit_to == "Fahrenheit":
        return value * 9/5 + 32
    elif unit_from == "Fahrenheit" and unit_to == "Celsius":
        return (value - 32) * 5/9
    elif unit_from == "Kilometers" and unit_to == "Miles":
        return value * 0.621371
    elif unit_from == "Miles" and unit_to == "Kilometers":
        return value / 0.621371
    elif unit_from == "Kilograms" and unit_to == "Pounds":
        return value * 2.20462
    elif unit_from == "Pounds" and unit_to == "Kilograms":
        return value / 2.20462
    else:
        return None

# Main loop
slow_print("🎉 Welcome to the Fun Unit Converter! 🎉")
time.sleep(0.5)

while True:
    slow_print("\nYou can convert temperature 🌡️, distance 🛣️, and weight ⚖️!\n")
    
    # Show units
    slow_print("Available units:")
    for i, unit in enumerate(units, 1):
        slow_print(f"{i}. {unit}")
    
    # User input
    try:
        value = float(input("\nEnter a number to convert: "))
        from_choice = int(input("Select FROM unit (number between 1 and 6): "))
        to_choice = int(input("Select TO unit (number between 1 and 6): "))
    except:
        slow_print("❌ Invalid input! Please enter numbers only.")
        continue
    
    unit_from = units[from_choice - 1]
    unit_to = units[to_choice - 1]
    
    # Conversion
    result = convert(value, unit_from, unit_to)
    if result is None:
        slow_print("❌ Oops! That conversion isn't possible. Try again!")
    else:
        fun_messages = ["Awesome!", "Great job!", "Conversion complete!", "Boom!"]
        slow_print(f"\n{random.choice(fun_messages)} 🎊")
        slow_print(f"{value} {unit_from} = {result:.2f} {unit_to} 🎯")
    
    # Ask to continue
    cont = input("\nDo you want to convert another value? (y/n): ").strip().lower()
    if cont not in ["y", "yes"]:
        slow_print("\n👋 Thanks for using the Fun Unit Converter! Bye! 🎉")
        break
