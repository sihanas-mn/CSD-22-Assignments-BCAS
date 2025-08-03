# Constants
BEGINNER_COST = 2000.00
INTERMEDIATE_COST = 5000.00
EXPERT_COST = 7000.00
PRIVATE_TUITION_COST = 500.00
COMPETITION_ENTRY_FEE = 2500.00

# Weight categories based on weight
def get_weight_category(weight):
    if weight > 100:
        return "Heavyweight"
    elif 91 <= weight <= 100:
        return "Light-Heavyweight"
    elif 82 <= weight <= 90:
        return "Middleweight"
    elif 74 <= weight <= 81:
        return "Light-Middleweight"
    elif 67 <= weight <= 73:
        return "Light-Middleweight"
    elif weight < 66:
        return "Flyweight"
    else:
        return "Unknown category"

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

def validate_weight(value):
    weight = float(value)
    if weight <= 0:
        raise ValueError("Weight must be a positive number")
    return weight

def validate_competitions(value, training_plan):
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
    name = input("Enter athlete name: ")
    training_plan = get_valid_input("Enter training plan (beginner, intermediate, expert): ", validate_training_plan)
    weight = get_valid_input("Enter current weight in kg: ", validate_weight)
    
    competition_category = ""
    competitions = 0
    
    if training_plan != "beginner":
        competition_category = get_weight_category(weight)
        competitions = get_valid_input("Enter number of competitions entered this month: ", lambda x: validate_competitions(x, training_plan))
    
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

# Function to compare weights
def compare_weights(current_weight, competition_weight_category):
    if competition_weight_category == "":
        return "Beginners are not allowed to enter competitions."
    
    if current_weight > 100:
        return f"Current weight ({current_weight} kg) is Heavyweight."
    elif 91 <= current_weight <= 100:
        return f"Current weight ({current_weight} kg) is Light-Heavyweight."
    elif 82 <= current_weight <= 90:
        return f"Current weight ({current_weight} kg) is Middleweight."
    elif 74 <= current_weight <= 81:
        return f"Current weight ({current_weight} kg) is Light-Middleweight."
    elif 67 <= current_weight <= 73:
        return f"Current weight ({current_weight} kg) is Light-Middleweight."
    elif current_weight < 66:
        return f"Current weight ({current_weight} kg) is Flyweight."
    else:
        return f"Current weight ({current_weight} kg) does not match any category."

# Function to display athlete summary
def display_athlete_summary(athlete, costs, weight_comparison):
    print(f"\nAthlete Name: {athlete['name']}")
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
    weight_comparison = compare_weights(athlete["weight"], athlete["competition_category"])
    athletes.append((athlete, costs, weight_comparison))
    display_athlete_summary(athlete, costs, weight_comparison)
