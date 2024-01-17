import re
from scorecard import create_scorecard, add_perspective, add_objective, add_measure, print_scorecard

def validate_input(prompt, allowed_chars=None, required_type=None):
    while True:
        user_input = input(prompt)

        # Basic validation using string methods
        if not user_input.strip():
            print("Invalid input. Please enter a non-empty value.")
            continue

        if allowed_chars and not all(char.isalpha() for char in user_input):
            print("Invalid input. Only letters are allowed.")
            continue

        # Advanced validation using regular expressions (optional)
        if allowed_chars and not re.match(r"^[a-zA-Z]+$", user_input):
            print("Invalid input. Only letters are allowed.")
            continue

        if required_type == "float":
            try:
                float(user_input)
                return user_input
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
        elif required_type is None:
            return user_input
        else:
            print(f"Invalid input type. Please enter a value of type {required_type}.")



# Get scorecard name and owner
name = validate_input("Enter scorecard name: ", allowed_chars="letters")
owner = validate_input("Enter scorecard owner: ", allowed_chars="letters")

# Create the scorecard
scorecard = create_scorecard(name.title(), owner.title())

# Add perspectives, objectives, and measures based on user input
while True:
    perspective_name = input("Enter perspective name (or 'done' to finish): ")
    if perspective_name.lower() == "done":
        break
    try:
        perspective_weight = float(input("Enter perspective weight (optional): "))
    except ValueError:
        perspective_weight = None
    perspective = add_perspective(scorecard, perspective_name, perspective_weight)
    print("Perspective:", perspective_name)

    while True:
        objective_name = input("Enter objective name (or 'back' to return to perspectives): ")
        if objective_name.lower() == "back":
            break
        target_value = float(input("Enter target value for the objective: "))
        objective = add_objective(perspective, objective_name, target_value)

        while True:
            measure_name = input("Enter measure name (or 'back' to return to objectives): ")
            if measure_name.lower() == "back":
                break
            data_type = input("Enter measure data type (numeric, percentage, etc.): ")
            add_measure(objective, measure_name, data_type)
            
print_scorecard(scorecard)

# Example of using a list comprehension to get measure names
measure_names = [measure.name for measure in scorecard.get_all_measures()]
print("Measure names:", measure_names)

# Example of using a dictionary to access a perspective by name
perspective_to_view = input("Enter the name of the perspective to view: ")
perspective = scorecard.get_perspective_by_name(perspective_to_view)
if perspective:
    print("Perspective details:")
    print(f"Name: {perspective.name}")
    for objective in perspective.objectives:
        print(f"  Objective: {objective.name}")
else:
    print("Perspective not found.")
 
