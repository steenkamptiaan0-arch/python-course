def hello_world():
    print("Hello world!")


hello_world()


def sum(num1=0, num2=0):# Default perameters in (def)=definition sum=name of function (num1=0, num2=0)= perameters names
    if (type(num1) is not int or type(num2) is not int):
        return 0
    return num1 + num2 # defining the functions

total = sum(7, 2) #total = sum=name of function (7, 2)= velues to be passed to the function
print(total)

 #used for lust and tuple
def multiple_items(*args): # the asterisk * allows to pass multiple items in a tuple
    print(args)
    print(type(args))


multiple_items("Dave", "John", "Sara")

# used for dictionary
def mult_named_items(**kwargs): # the doublle asterisk ** allows to name the items in the dictionary
    print(kwargs)
    print(type(kwargs))


mult_named_items(first="Dave", last="Gray")
