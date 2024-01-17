from scorecard import Scorecard,create_scorecard, add_perspective, add_objective, add_measure, print_scorecard
import matplotlib.pyplot as plt
import re
import numpy as np
from database_func import save_scorecard, retrieve_scorecards, delete_scorecard
#from user_input import validate_input

def main():
    while True:
        print("\nBalanced Scorecard Application")
        print("1. Create a new scorecard")
        print("2. View an existing scorecard")
        print("3. Delete an existing scorecard")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            create_new_scorecard()
        elif choice == "2":
            view_existing_scorecard()
        elif choice == "3":
            delete_existing_scorecard()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

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
        elif required_type == "int":
            try:
                int(user_input)
                return user_input
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
        elif required_type is None:
            return user_input
        else:
            print(f"Invalid input type. Please enter a value of type {required_type}.")


def plot_pie_chart(scorecard):
    if not scorecard.perspectives:
        print("No perspectives to plot.")
        return

    labels = [perspective.name.upper() for perspective in scorecard.perspectives]
    sizes = [100 / len(scorecard.perspectives)] * len(scorecard.perspectives)

    pie_chart = plt.pie(sizes, labels=labels, startangle=90)
    plt.axis('equal')
    plt.title(f"Scorecard: {scorecard.name}")

    wedges, texts = pie_chart
    for i, (wedge, text) in enumerate(zip(wedges, texts)):
        perspective = scorecard.perspectives[i]
        objective_text = "\n".join(f"\t- {objective.name}" for objective in perspective.objectives)
        text.set_text(f"{labels[i]}\n{objective_text}")

    plt.show()

def create_new_scorecard():
   
    # Gather scorecard information with input validation
    name = validate_input("Enter scorecard name (letters only): ", allowed_chars="letters")
    owner = validate_input("Enter scorecard owner (letters only): ", allowed_chars="letters")

    # Create the scorecard object
    scorecard = create_scorecard(name, owner)

    # Gather perspectives, objectives, and measures
    while True:
        add_perspective_choice = input("Do you want to add a new perspective? (y/n): ")
        if add_perspective_choice.lower() == "y":
            perspective_name = validate_input("Enter perspective name: ")
            perspective_weight = validate_input("Enter perspective weight (optional, numeric): ", required_type="float")
            perspective = add_perspective(scorecard, perspective_name, perspective_weight)

            while True:
                add_objective_choice = input("Do you want to add a new objective to this perspective? (y/n): ")
                if add_objective_choice.lower() == "y":
                    objective_name = validate_input("Enter objective name: ")
                    objective_target_value = validate_input("Enter objective target value (numeric): ", required_type="float")
                    objective = add_objective(perspective, objective_name, objective_target_value)

                    while True:
                        add_measure_choice = input("Do you want to add a new measure to this objective? (y/n): ")
                        if add_measure_choice.lower() == "y":
                            measure_name = validate_input("Enter measure name: ")
                            add_measure(objective, measure_name)
                        else:
                            break
                else:
                    break
        else:
            break

    # Print the completed scorecard
    save_scorecard(scorecard)
    print_scorecard(scorecard)
    #retrieve_scorecards()

def view_existing_scorecard():
    #print("View")
    scorecards = retrieve_scorecards()
    if not scorecards:
        print("No scorecards found.")
        return

    print("Available Scorecards:")
    for scorecard_data in scorecards:
        print(f"ID: {scorecard_data.id}, Name: {scorecard_data.name}, Owner: {scorecard_data.owner}")

    while True:
        view_choice = input("\nDo you want to view a specific scorecard? (y/n): ")
        if view_choice.lower() == "y":
            try:
                scorecard_id = int(validate_input("Enter the ID of the scorecard to view: ", required_type="int"))
                scorecard_to_view = None
                for scorecard in scorecards:
                    if scorecard.id == int(scorecard_id):
                        scorecard_to_view = scorecard
                        break
                if not scorecard_to_view:
                    print("Invalid scorecard ID. Please try again.")
                    return
                plot_pie_chart(scorecard_to_view)
            except Exception as e:
                print(f"Error retrieving scorecard: {e}")
        else:
            break

def delete_existing_scorecard():
    scorecards = retrieve_scorecards()
    if not scorecards:
        print("No scorecards found to delete.")
        return

    print("Available Scorecards:")
    for scorecard_data in scorecards:
        print(f"ID: {scorecard_data.id}, Name: {scorecard_data.name}, Owner: {scorecard_data.owner}")

    scorecard_id = validate_input("Enter the ID of the scorecard you want to delete: ", required_type="int")

    scorecard_to_delete = None
    for scorecard in scorecards:
        if scorecard.id == int(scorecard_id):
            scorecard_to_delete = scorecard
            break

    if not scorecard_to_delete:
        print("Invalid scorecard ID. Please try again.")
        return

    confirmation = input(
        f"Are you sure you want to delete the scorecard '{scorecard_to_delete.id}'? (y/n): "
    )
    if confirmation.lower() == "y":
        try:
            delete_scorecard(int(scorecard_id)) 
            print("Scorecard deleted successfully!")
        except Exception as e:
            print(f"Error deleting scorecard: {e}")
    else:
        print("Deletion cancelled.")



if __name__ == "__main__":
    main()



