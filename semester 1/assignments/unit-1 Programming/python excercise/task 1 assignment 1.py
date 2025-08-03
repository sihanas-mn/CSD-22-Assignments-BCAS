# Constants
BEGINNER_COST = 2000.00
INTERMEDIATE_COST = 5000.00
EXPERT_COST = 7000.00
PRIVATE_TUITION_COST = 500.00
COMPETITION_ENTRY_FEE = 2500.00

WEIGHT_CATEGORIES = {
    "Heavyweight": float('inf'),  # Above 100kg
    "Light-Heavyweight": 100,
    "Middleweight": 90,
    "Light-Middleweight": 81,
    "Lightweight": 73,
    "Flyweight": 66
}

# Function to collect athlete information
def get_athlete_info():
    while True:
        try:
            name = input("Enter athlete name: ")
            training_plan = input("Enter training plan (beginner, intermediate, expert): ").lower()
            if training_plan not in ["beginner", "intermediate", "expert"]:
                raise ValueError("Invalid training plan")
            
            weight = float(input("Enter current weight in kg: "))
            
            competition_category = input("Enter competition weight category: ")
            if competition_category not in WEIGHT_CATEGORIES:
                raise ValueError("Invalid weight category")
            
            competitions = int(input("Enter number of competitions entered this month: "))
            
            private_hours = int(input("Enter number of hours of private coaching per week (max 5): "))
            if private_hours > 5:
                raise ValueError("Private coaching hours cannot exceed 5 per week")
            
            return {
                "name": name,
                "training_plan": training_plan,
                "weight": weight,
                "competition_category": competition_category,
                "competitions": competitions,
                "private_hours": private_hours
            }
        except ValueError as e:
            print(f"Error: {e}. Please try again.")

# Function to calculate costs
def calculate_costs(athlete):
    training_cost = {
        "beginner": BEGINNER_COST,
        "intermediate": INTERMEDIATE_COST,
        "expert": EXPERT_COST
    }[athlete["training_plan"]] * 4
    
    private_coaching_cost = athlete["private_hours"] * PRIVATE_TUITION_COST * 4
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
    max_weight = WEIGHT_CATEGORIES[competition_weight_category]
    if current_weight > max_weight:
        return f"Current weight ({current_weight} kg) exceeds the limit for {competition_weight_category}."
    elif current_weight < max_weight:
        return f"Current weight ({current_weight} kg) is within the limit for {competition_weight_category}."
    else:
        return f"Current weight ({current_weight} kg) exactly matches the limit for {competition_weight_category}."

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
