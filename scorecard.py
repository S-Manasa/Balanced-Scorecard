class Scorecard:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.perspectives = []

class Perspective:
    def __init__(self, name, weight=None):
        self.name = name
        self.weight = weight
        self.objectives = []

class Objective:
    def __init__(self, name, target_value):
        self.name = name
        self.target_value = target_value
        self.measures = []

class Measure:
    def __init__(self, name, data_type="numeric"):
        self.name = name
        self.data_type = data_type
        self.data_points = []

class DataPoint:
    def __init__(self, date, value):
        self.date = date
        self.value = value

def create_scorecard(name, owner):
    """Creates a new scorecard with the given name and owner."""
    return Scorecard(name, owner)

def add_perspective(scorecard, perspective_name, weight=None):
    """Adds a new perspective to the scorecard."""
    perspective = Perspective(perspective_name, weight)
    scorecard.perspectives.append(perspective)
    return perspective

def add_objective(perspective, objective_name, target_value):
    """Adds a new objective to the perspective."""
    objective = Objective(objective_name, target_value)
    perspective.objectives.append(objective)
    return objective

def add_measure(objective, measure_name, data_type="numeric"):
    """Adds a new measure to the objective."""
    measure = Measure(measure_name, data_type)
    objective.measures.append(measure)


    
def print_scorecard(scorecard):
    """Prints the scorecard details to the console."""
    print(f"Scorecard: {scorecard.name}")
    print(f"Owner: {scorecard.owner}")
    for perspective in scorecard.perspectives:
        print(f"Perspective: {perspective.name}")
        for objective in perspective.objectives:
            print(f"  Objective: {objective.name}")
            for measure in objective.measures:
                print(f"    Measure: {measure.name}")


if __name__ == "__main__":
    my_scorecard = create_scorecard("Personal BSC", "John Doe")
    add_perspective(my_scorecard, "Financial")
    add_objective(my_scorecard.perspectives[0], "Increase revenue", 10000)
    add_measure(my_scorecard.perspectives[0].objectives[0], "Monthly sales")
    print_scorecard(my_scorecard)


