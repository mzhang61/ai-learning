from agents.simple_reflex_agent import Rule

def load_rules():
    # Return rule set for the vacuum cleaner environment
    return [
        Rule(lambda s: s["status"] == "Dirty", "Suck"),
        Rule(lambda s: s["location"] == "A", "MoveRight"),
        Rule(lambda s: s["location"] == "B", "MoveLeft"),
    ]

def load_percepts():
    # Return simulated environment percepts
    return [
        ("A", "Dirty"),
        ("A", "Clean"),
        ("B", "Dirty"),
        ("B", "Clean"),
    ]