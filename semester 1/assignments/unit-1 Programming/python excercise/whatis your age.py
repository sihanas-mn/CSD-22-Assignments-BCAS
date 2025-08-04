try:
    age = int(input("Enter your age: "))
    print("Your are " + str(age) + " years old.")
except ValueError:
    print("Please enter a valid number for age")