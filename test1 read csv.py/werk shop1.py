import random
while True:
    name = input("Enter your name: ")
    print(name.capitalize())
    break

def numbre():
    numbre = "0" + ''.join(str(random.randint(0, 9)) for _ in range(9)) # "".join() creates a string from the list of characters and str(random.randint(0, 9) for _ in range(9) is how many numbers you want to generate
    return numbre

print("Number", numbre())