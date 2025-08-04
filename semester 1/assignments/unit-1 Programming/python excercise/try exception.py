while True:
    user_input=input("Enter a number (or 'q' to quit): ")
    if user_input.lower() == 'q':
        print("Good Bye!")
        break
    try:
        number = int(user_input)
        print("You entered: " + str(number))
    except ValueError:
        print("Invalid input! please try again.")