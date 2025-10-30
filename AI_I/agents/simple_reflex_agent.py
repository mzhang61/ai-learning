from typing import Callable, Any, List, Tuple, Dict


class Rule:
    def __init__(self, condition: Callable[[Any], bool], action: str):
        self.condition = condition
        self.action = action


class SimpleReflexAgent:
    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def interpret_input(self, percept: Tuple[str, str]):
        """
        enter percept, for example ('A', 'Dirty')
        """
        location, status = percept
        return {"location": location, "status": status}

    def rule_match(self, state: Dict[str, Any]) -> Rule:
        """
        match rule based on the current state
        """
        for rule in self.rules:
            if rule.condition(state):
                return rule
        # Does not match any, no operation
        return Rule(lambda _: True, "NoOperation")

    def act(self, percept: Tuple[str, str]) -> str:
       """
       implement the action
       """
       state = self.interpret_input(percept)
       rule = self.rule_match(state)
       return rule.action
