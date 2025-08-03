while True:
    try:
        value= int(input("Enter Positive Number: ")) 
        if value > 0: 
           print(value)
        else:
            print("Please enter a positive integer.")
    except ValueError:
        print("Invalid input! Please enter a number.")

