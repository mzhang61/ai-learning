from agents.simple_reflex_agent import SimpleReflexAgent
from agents.vacuum_data import load_rules, load_percepts
from agents.model_based_reflex_agent import build_default_model_based_agent
from agents.percept_scenarios_data import SCENARIOS

# simple reflex agent
def run_simple_reflex_agent():
    rules = load_rules()
    percepts = load_percepts()
    agent = SimpleReflexAgent(rules)

    print("=== Running Simple Reflex Agent ===")
    for percept in percepts:
        action = agent.act(percept)
        print(f"Percept: {percept} -> Action: {action}")

def run_model_based_reflex_agent() -> None:
    for title, percepts in SCENARIOS:
        agent = build_default_model_based_agent()
        print(f"=== {title} ===")
        for p in percepts:
            action = agent.act(p)
            print(f"Percept: {p} -> Action: {action} | Belief: {agent.state}")
        print()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # run_simple_reflex_agent()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
    run_model_based_reflex_agent()