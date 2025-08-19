import random
while True:
    name = str(input("Enter your name: "))
    print(name.capitalize())
    break

def numbre():
    num = "0" + ''.join(str(random.randint(0, 9)) for _ in range(9)) # "".join() creates a string from the list of characters and str(random.randint(0, 9) for _ in range(9) is how many numbers you want to generate
    return num

print(numbre())