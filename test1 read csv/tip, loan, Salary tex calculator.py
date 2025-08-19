import time
import random

def slow_print(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def calculate_tip():
    slow_print("\n🍽️ Tip Calculator 🍽️")
    bill = float(input("Enter your bill amount: $"))
    percent = float(input("Tip percentage (e.g., 15 for 15%): "))
    tip = bill * percent / 100
    total = bill + tip
    slow_print(f"💰 Tip: ${tip:.2f}")
    slow_print(f"🧾 Total bill: ${total:.2f}")

def calculate_loan():
    slow_print("\n🏦 Loan Calculator 🏦")
    principal = float(input("Enter loan amount: $"))
    rate = float(input("Annual interest rate (%): "))
    years = int(input("Loan term in years: "))
    monthly_rate = rate / 100 / 12
    months = years * 12
    if monthly_rate == 0:
        payment = principal / months
    else:
        payment = principal * monthly_rate * (1 + monthly_rate)**months / ((1 + monthly_rate)**months - 1)
    slow_print(f"💸 Monthly payment: ${payment:.2f}")
    slow_print(f"Total payment: ${payment*months:.2f}")

def calculate_salary_tax():
    slow_print("\n💼 Salary Tax Calculator 💼")
    salary = float(input("Enter your annual salary: $"))
    # Simple progressive tax example
    if salary <= 50000:
        tax_rate = 10
    elif salary <= 100000:
        tax_rate = 20
    else:
        tax_rate = 30
    tax = salary * tax_rate / 100
    net = salary - tax
    slow_print(f"🧾 Tax rate applied: {tax_rate}%")
    slow_print(f"💰 Tax amount: ${tax:.2f}")
    slow_print(f"💵 Net salary: ${net:.2f}")
    
    # Spending budget (50% of net income)
    budget = net * 0.5
    slow_print(f"💸 Suggested spending budget: ${budget:.2f}")
    
    # Money growth projection
    rate = float(input("Enter expected annual growth rate (%) for savings/investment: "))
    years = int(input("How many years do you want to project?: "))
    future_value = net * ((1 + rate/100) ** years)
    slow_print(f"🌱 Your money could grow to: ${future_value:.2f} in {years} years!")

# Main fun loop
slow_print("🎉 Welcome to the Fun Finance Calculator! 🎉")
time.sleep(0.5)

while True:
    slow_print("\nWhat would you like to calculate today?")
    slow_print("1. Tip 🍽️\n2. Loan 🏦\n3. Salary Tax & Budget 💼")
    
    try:
        choice = int(input("Select an option (1-3): "))
    except:
        slow_print("❌ Invalid input, please enter a number 1-3.")
        continue

    if choice == 1:
        calculate_tip()
    elif choice == 2:
        calculate_loan()
    elif choice == 3:
        calculate_salary_tax()
    else:
        slow_print("❌ Invalid choice! Try again.")
        continue
    
    # Fun encouragement
    messages = ["Great job! 🎊", "You're a finance wizard! 🧙‍♂️", "Calculation complete! ✅"]
    slow_print(random.choice(messages))
    
    # Continue?
    cont = input("\nDo you want to do another calculation? (yes/no): ").strip().lower()
    if cont not in ["yes", "y"]:
        slow_print("\n👋 Thanks for using the Fun Finance Calculator! Bye! 🎉")
        break
