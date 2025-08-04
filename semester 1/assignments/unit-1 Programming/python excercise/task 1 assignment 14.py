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

def validate_private_hours_per_week(value):
    private_hours_per_week = int(value)
    if private_hours_per_week < 0 or private_hours_per_week > 5:
        raise ValueError("Private coaching hours per week must be between 0 and 5")
    return private_hours_per_week

# Function to collect athlete information
def get_athlete_info():
    name = get_valid_input("Enter athlete name: ", validate_name)
    training_plan = get_valid_input("Enter training plan (beginner, intermediate, expert): ", validate_training_plan)
    weight = get_valid_input("Enter current weight in kg: ", validate_weight)
    
    competitions = 0
    
    if training_plan != "beginner":
        competitions = get_valid_input("Enter number of competitions entered this month: ", validate_competitions)
    
    private_hours_per_week = get_valid_input("Enter number of hours of private coaching per week (max 5): ", validate_private_hours_per_week)
    
    return {
        "name": name,
        "training_plan": training_plan,
        "weight": weight,
        "competitions": competitions,
        "private_hours_per_week": private_hours_per_week
    }

# Function to calculate costs
def calculate_costs(athlete):
    training_cost = {
        "beginner": BEGINNER_COST,
        "intermediate": INTERMEDIATE_COST,
        "expert": EXPERT_COST
    }[athlete["training_plan"]] * 4
    
    private_coaching_cost = athlete["private_hours_per_week"] * 4 * PRIVATE_TUITION_COST
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

# Function to check competition eligibility
def check_eligibility(current_weight):
    if 81 <= current_weight <= 100:
        return "You are eligible to participate in competitions."
    else:
        return "You are not eligible to participate in competitions."

# Function to display athlete summary
def display_athlete_summary(athlete, costs, eligibility, weight_category):
    print(f"\nAthlete Name: {athlete['name']}")
    print(f"Current Weight: {athlete['weight']} kg")
    print(f"Weight Category: {weight_category}")
    print(f"Training Cost: ${costs['training_cost']:.2f}")
    print(f"Private Coaching Cost: ${costs['private_coaching_cost']:.2f}")
    print(f"Competition Cost: ${costs['competition_cost']:.2f}")
    print(f"Total Cost: ${costs['total_cost']:.2f}")
    print(eligibility)
    print()

# Main program logic
athletes = []
for i in range(6):
    athlete = get_athlete_info()
    costs = calculate_costs(athlete)
    weight_category = get_weight_category(athlete["weight"])
    eligibility = check_eligibility(athlete["weight"])
    athletes.append((athlete, costs, eligibility, weight_category))
    display_athlete_summary(athlete, costs, eligibility, weight_category)
