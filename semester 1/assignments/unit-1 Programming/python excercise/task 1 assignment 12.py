# Constants
BEGINNER_COST = 2000.00
INTERMEDIATE_COST = 5000.00
EXPERT_COST = 7000.00
PRIVATE_TUITION_COST = 500.00
COMPETITION_ENTRY_FEE = 2500.00

# Function to get valid input from the user
def get_valid_input(prompt, validation_func):
    while True:
        try:
            value = input(prompt)
            validated_value = validation_func(value)
            return validated_value
        except ValueError as e:
            print(f"Error: {e}. Please try again.")

# Validation functions
def validate_training_plan(value):
    value = value.lower()
    if value not in ["beginner", "intermediate", "expert"]:
        raise ValueError("Invalid training plan")
    return value

def validate_name(value):
    if not value.replace(" ", "").isalpha():
        raise ValueError("Name must be a string without numbers")
    return value

def validate_weight(value):
    weight = int(value)
    if weight <= 0:
        raise ValueError("Weight must be a positive number")
    return weight

def validate_competitions(value):
    competitions = int(value)
    if competitions < 0:
        raise ValueError("Number of competitions cannot be negative")
    return competitions

def validate_private_hours(value):
    private_hours = int(value)
    if private_hours < 0 or private_hours > 20:
        raise ValueError("Private coaching hours must be between 0 and 20 per month")
    return private_hours

# Function to collect athlete information
def get_athlete_info():
    name = get_valid_input("Enter athlete name: ", validate_name)
    training_plan = get_valid_input("Enter training plan (beginner, intermediate, expert): ", validate_training_plan)
    weight = get_valid_input("Enter current weight in kg: ", validate_weight)
    
    competition_category = ""
    competitions = 0
    
    if training_plan != "beginner":
        competition_category = get_valid_input("Enter competition weight category: ", lambda x: x)  # Temporary validation as a placeholder
        competitions = get_valid_input("Enter number of competitions entered this month: ", validate_competitions)
    
    private_hours = get_valid_input("Enter number of hours of private coaching per month (max 20): ", validate_private_hours)
    
    return {
        "name": name,
        "training_plan": training_plan,
        "weight": weight,
        "competition_category": competition_category,
        "competitions": competitions,
        "private_hours": private_hours
    }

# Function to calculate costs
def calculate_costs(athlete):
    training_cost = {
        "beginner": BEGINNER_COST,
        "intermediate": INTERMEDIATE_COST,
        "expert": EXPERT_COST
    }[athlete["training_plan"]] * 4
    
    private_coaching_cost = athlete["private_hours"] * PRIVATE_TUITION_COST
    competition_cost = athlete["competitions"] * COMPETITION_ENTRY_FEE
    
    total_cost = training_cost + private_coaching_cost + competition_cost
    
    return {
        "training_cost": training_cost,
        "private_coaching_cost": private_coaching_cost,
        "competition_cost": competition_cost,
        "total_cost": total_cost
    }

# Function to get weight category based on current weight
def get_weight_category(current_weight):
    if current_weight > 100:
        return "Heavyweight"
    elif current_weight == 100:
        return "Light-Heavyweight"
    elif 90 <= current_weight <= 99:
        return "Middleweight"
    elif 81 <= current_weight <= 89:
        return "Light-Middleweight"
    elif 73 <= current_weight <= 80:
        return "Lightweight"
    elif 66 <= current_weight <= 72:
        return "Flyweight"
    else:
        return "You are not eligible for a training plan."

# Function to compare weights
def compare_weights(current_weight, competition_weight_category):
    if competition_weight_category == "":
        return "Note: Beginners cannot participate in competitions."
    
    weight_categories = {
        "Heavyweight": 100,
        "Light-Heavyweight": 100,
        "Middleweight": 90,
        "Light-Middleweight": 81,
        "Lightweight": 73,
        "Flyweight": 66
    }
    
    max_weight = weight_categories[competition_weight_category]
    if current_weight > max_weight:
        return f"Current weight ({current_weight} kg) exceeds the limit for {competition_weight_category}."
    elif current_weight <= max_weight:
        return f"Current weight ({current_weight} kg) is within the limit for {competition_weight_category}."
    else:
        return f"Current weight ({current_weight} kg) exactly matches the limit for {competition_weight_category}."

# Function to display athlete summary
def display_athlete_summary(athlete, costs, weight_comparison, weight_category):
    print(f"\nAthlete Name: {athlete['name']}")
    print(f"Current Weight: {athlete['weight']} kg")
    print(f"Weight Category: {weight_category}")
    print(f"Training Cost: ${costs['training_cost']:.2f}")
    print(f"Private Coaching Cost: ${costs['private_coaching_cost']:.2f}")
    print(f"Competition Cost: ${costs['competition_cost']:.2f}")
    print(f"Total Cost: ${costs['total_cost']:.2f}")
    print(weight_comparison)
    print()

# Main program logic
athletes = []
for i in range(6):
    athlete = get_athlete_info()
    costs = calculate_costs(athlete)
    weight_category = get_weight_category(athlete["weight"])
    weight_comparison = compare_weights(athlete["weight"], athlete["competition_category"])
    athletes.append((athlete, costs, weight_comparison, weight_category))
    display_athlete_summary(athlete, costs, weight_comparison, weight_category)
