from typing import List, Tuple

# many scenarios
SCENARIOS: List[Tuple[str, List[Tuple[str, str]]]] = [
    (
        "Scenario 1: Normal cleaning process (A dirty -> suck, then move to B and check)",
        [("A", "Dirty"), ("A", "Clean"), ("B", "Dirty"), ("B", "Clean")],
    ),
    (
        "Scenario 2: Observe B as clean first, then return to A",
        [("B", "Clean"), ("A", "Dirty"), ("A", "Clean"), ("B", "Clean")],
    ),
    (
        "Scenario 3: Demonstrate 'memory' effect (repeated perceptions still follow internal belief)",
        [("A", "Clean"), ("A", "Clean"), ("A", "Clean"), ("B", "Dirty"), ("B", "Clean")],
    ),
]