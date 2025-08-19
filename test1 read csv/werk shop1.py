import random
# This code generates a random phone number and asks for the user's name
while True:  
    name = str(input("Enter your name: ")).capitalize()
    print(f" Welkam user = {name}")
    break
# This code generates a random phone number 
def numbre():
    num = "0" + ''.join(str(random.randint(0, 9)) for _ in range(9)) # "".join() creates a string from the list of characters and str(random.randint(0, 9) for _ in range(9) is how many numbers you want to generate
    return num

print(f"This is you phone numbre {numbre()}")# Call the function to generate the number

saved_number = numbre()

# Step 4: Show the saved number
print("Your saved random number is:", saved_number)

# Step 5 (optional): Save to a file
with open("test1 read csv/random_number.txt", "w") as f:
    f.write(saved_number)

print("Number also saved in random_number.txt")
