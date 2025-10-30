from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple, Optional

from agents.simple_reflex_agent import Rule

# ==========================================================
#  Model-Based Reflex Agent
# ==========================================================
@dataclass
class ModelBasedReflexAgent:
    rules: List[Rule]
    # default_factory=lambda:
    # ensures each instance gets its own dict
    state: Dict[str, Any] = field(default_factory=lambda: {
        "location": "A",
        "clean": {"A": None, "B": None}  # None = unknown, True = clean, False = dirty
    })
    last_action: Optional[str] = None

    # SENSOR MODEL
    def sensor_model(self, state: Dict[str, Any], percept: Tuple[str, str]) -> None:
        location, status = percept
        state["location"] = location
        is_clean = True if status == "Clean" else False
        state["clean"][location] = is_clean

    # TRANSITION MODEL
    def transition_model(self, state: Dict[str, Any], last_action: Optional[str]) -> None:
        if last_action is None:
            return
        loc = state["location"]
        if last_action == "MoveRight" and loc == "A":
            state["location"] = "B"
        elif last_action == "MoveLeft" and loc == "B":
            state["location"] = "A"
        # Suck / NoOperation do not change location

    # UPDATE-STATE(state, action, percept, transition model, sensor model)
    def update_state(self, percept: Tuple[str, str]) -> None:
        self.transition_model(self.state, self.last_action)
        self.sensor_model(self.state, percept)

    # RULE-MATCH
    def rule_match(self) -> Rule:
        for rule in self.rules:
            if rule.condition(self.state):
                return rule
        return Rule(lambda _: True, "NoOperation")

    # ACT
    def act(self, percept: Tuple[str, str]) -> str:
        self.update_state(percept)
        rule = self.rule_match()
        action = rule.action
        self.last_action = action
        return action


# ==========================================================
#  Helper: Default rule set
# ==========================================================
def build_default_model_based_agent() -> ModelBasedReflexAgent:
    """
    Build a default model-based agent with basic rules:
      - If current room is dirty, suck
      - If the other room is known dirty, move there
      - Otherwise move back and forth between rooms
    """
    rules = [
        Rule(lambda s: s["clean"].get(s["location"]) is False, "Suck"),
        Rule(lambda s: s["location"] == "A" and s["clean"].get("B") is False, "MoveRight"),
        Rule(lambda s: s["location"] == "B" and s["clean"].get("A") is False, "MoveLeft"),
        Rule(lambda s: s["location"] == "A", "MoveRight"),
        Rule(lambda s: s["location"] == "B", "MoveLeft"),
    ]
    return ModelBasedReflexAgent(rules=rules)