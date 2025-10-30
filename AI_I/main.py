from agents.simple_reflex_agent import SimpleReflexAgent
from agents.vacuum_data import load_rules, load_percepts

# simple reflex agent
def run_simple_reflex_agent():
    rules = load_rules()
    percepts = load_percepts()
    agent = SimpleReflexAgent(rules)

    print("=== Running Simple Reflex Agent ===")
    for percept in percepts:
        action = agent.act(percept)
        print(f"Percept: {percept} -> Action: {action}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_simple_reflex_agent()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
