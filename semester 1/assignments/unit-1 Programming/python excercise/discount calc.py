# Take the purchase amount as input from the user
purchase_amount = float(input("Enter the purchase amount: "))

# Check if the purchase amount exceeds 5000
if purchase_amount > 5000:
    discount = 0.15  # 15% discount
else:
    discount = 0.10  # 10% discount

# Calculate the discount amount
discount_amount = purchase_amount * discount

# Calculate the final amount to be paid
final_amount = purchase_amount - discount_amount

# Print the final amount to be paid
print(f"The amount to be paid after discount is: {final_amount:.2f}")
