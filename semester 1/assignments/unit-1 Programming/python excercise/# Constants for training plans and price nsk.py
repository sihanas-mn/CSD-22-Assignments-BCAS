# Constants for training plans and prices
TRAINING_PLANS = {
    'Beginner': {'sessions_per_week': 2, 'weekly_fee': 2000},
    'Intermediate': {'sessions_per_week': 3, 'weekly_fee': 5000},
    'Elite': {'sessions_per_week': 5, 'weekly_fee': 7000}
}
PRIVATE_COACHING_RATE = 500
COMPETITION_ENTRY_FEE = 2500

WEIGHT_CATEGORIES = [
    {'category': 'Flyweight', 'limit': 66},
    {'category': 'Lightweight', 'limit': 73},
    {'category': 'Light-Middleweight', 'limit': 81},
    {'category': 'Middleweight', 'limit': 90},
    {'category': 'Light - Heavyweight', 'limit': 100},
    {'category': 'Heavyweight', 'limit': float('inf')}
]

def get_user_input(prompt, valid_choices):
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print(f"Invalid input. Please choose from {valid_choices}.")

def select_training_plan():
    print("Select training plan:")
    for idx, plan in enumerate(TRAINING_PLANS, start=1):
        print(f"{idx}. {plan}")
    plan_choice = get_user_input("Enter your choice: ", map(str, range(1, len(TRAINING_PLANS) + 1)))
    return list(TRAINING_PLANS.keys())[int(plan_choice) - 1]

def determine_weight_category(current_weight):
    for category in WEIGHT_CATEGORIES:
        if current_weight <= category['limit']:
            return category['category'], category['limit']
    return WEIGHT_CATEGORIES[-1]['category'], WEIGHT_CATEGORIES[-1]['limit']

def calculate_cost():
    while True:
        athlete_name = input("Enter athlete's name: ").strip()
        selected_plan = select_training_plan()
        current_weight = float(input("Enter current weight in kilograms (kg): "))
        weight_category, weight_limit = determine_weight_category(current_weight)
        
        if current_weight > weight_limit:
            print(f"Warning: Current weight ({current_weight} kg) exceeds {weight_category} limit ({weight_limit} kg).")
        
        num_competitions = 0
        if selected_plan in ['Intermediate', 'Elite']:
            num_competitions = int(input("Enter number of competitions entered this month: "))

        private_coaching_hours = 0
        add_coaching = get_user_input("Do you want to add private coaching hours? (yes/no): ", ['yes', 'no'])
        if add_coaching == 'yes':
            private_coaching_hours = float(input("Enter number of hours of private coaching: "))

        total_training_fee = TRAINING_PLANS[selected_plan]['weekly_fee'] * 4
        total_private_coaching_cost = private_coaching_hours * PRIVATE_COACHING_RATE
        total_competition_fees = num_competitions * COMPETITION_ENTRY_FEE
        total_cost = total_training_fee + total_private_coaching_cost + total_competition_fees

        print("\nAthlete's Name:", athlete_name)
        print("Breakdown of Costs:")
        print(f"- Training Fees: Rs. {total_training_fee:.2f}")
        print(f"- Private Coaching Cost: Rs. {total_private_coaching_cost:.2f}")
        print(f"- Competition Fees: Rs. {total_competition_fees:.2f}")
        print(f"Total Cost for the Month: Rs. {total_cost:.2f}")
        print(f"Comparison of Current Weight ({current_weight} kg) with {weight_category} Category ({weight_limit} kg):")
        if current_weight <= weight_limit:
            print(f"Current weight is within the {weight_category} category limit.")
        else:
            print(f"Current weight exceeds the {weight_category} category limit.")

        save_to_file(athlete_name, selected_plan, current_weight, weight_category, num_competitions, private_coaching_hours, total_training_fee, total_private_coaching_cost, total_competition_fees, total_cost)

        another = get_user_input("Do you want to register another athlete? (yes/no): ", ['yes', 'no'])
        if another == 'no':
            break



if _name_ == "_main_":
    calculate_cost()