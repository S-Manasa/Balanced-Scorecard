import sqlite3
import scorecard
from scorecard import Scorecard, Perspective, Objective

def save_scorecard(scorecard):
    """Saves a scorecard to the SQLite database, including perspectives, objectives, and measures."""
    conn = sqlite3.connect("scorecards.db")
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON")

    # Create tables if they don't exist
    c.execute("""
        CREATE TABLE IF NOT EXISTS scorecards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            owner TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS perspectives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scorecard_id INTEGER,
            name TEXT,
            weight REAL,
            FOREIGN KEY (scorecard_id) REFERENCES scorecards(id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS objectives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            perspective_id INTEGER,
            name TEXT,
            target_value REAL,
            FOREIGN KEY (perspective_id) REFERENCES perspectives(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS measures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            objective_id INTEGER,
            name TEXT,
            FOREIGN KEY (objective_id) REFERENCES objectives(id)
        )
    """)

    # Insert scorecard data
    c.execute("INSERT INTO scorecards (name, owner) VALUES (?, ?)", (scorecard.name, scorecard.owner))
    scorecard_id = c.lastrowid

    # Insert perspective data
    for perspective in scorecard.perspectives:
        c.execute("INSERT INTO perspectives (scorecard_id, name, weight) VALUES (?, ?, ?)", (scorecard_id, perspective.name, perspective.weight))
        perspective_id = c.lastrowid

        # Insert objective data
        for objective in perspective.objectives:
            c.execute("INSERT INTO objectives (perspective_id, name, target_value) VALUES (?, ?, ?)", (perspective_id, objective.name, objective.target_value))
            objective_id = c.lastrowid

            # Insert measure data
            for measure in objective.measures:
                c.execute("INSERT INTO measures (objective_id, name) VALUES (?, ?)", (objective_id, measure.name))

    conn.commit()
    conn.close()

def retrieve_scorecards():
    conn = sqlite3.connect("scorecards.db")
    c = conn.cursor()

    c.execute("SELECT * FROM scorecards")
    scorecard_data = c.fetchall()

    scorecards = []
    for scorecard_row in scorecard_data:
        scorecard = Scorecard(scorecard_row[1], scorecard_row[2])
        scorecard.id = scorecard_row[0]

        c.execute("SELECT * FROM perspectives WHERE scorecard_id=?", (scorecard.id,))
        perspective_rows = c.fetchall()
        for perspective_row in perspective_rows:
            perspective = Perspective(perspective_row[2], perspective_row[3])
            scorecard.perspectives.append(perspective)

            c.execute("SELECT * FROM objectives WHERE perspective_id=?", (perspective_row[0],))
            objective_rows = c.fetchall()
            for objective_row in objective_rows:
                objective = Objective(objective_row[2], objective_row[3])
                perspective.objectives.append(objective)

        scorecards.append(scorecard)
    if scorecards:
        scorecards.sort(key=lambda s: s.id, reverse=True)

    conn.close()
    return scorecards

def delete_scorecard(scorecard_id):
    """Deletes a scorecard from the database."""
    conn = sqlite3.connect("scorecards.db")
    c = conn.cursor()

    c.execute("DELETE FROM perspectives WHERE scorecard_id = ?", (scorecard_id,))

    c.execute("DELETE FROM objectives WHERE perspective_id IN (SELECT id FROM perspectives WHERE scorecard_id = ?)", (scorecard_id,))
    c.execute("DELETE FROM measures WHERE objective_id IN (SELECT id FROM objectives WHERE perspective_id IN (SELECT id FROM perspectives WHERE scorecard_id = ?))", (scorecard_id,))

    # Delete the scorecard itself
    c.execute("DELETE FROM scorecards WHERE id = ?", (scorecard_id,))

    conn.commit()
    conn.close()

# Example usage:
#scorecard = create_new_scorecard()  # Assuming you have a function to create a scorecard object
#save_scorecard(scorecard)
#retrieve_scorecards()  # Verify data is saved correctly
