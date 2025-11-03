# ai_searches/ucs_data.py
from __future__ import annotations
from typing import Dict, Iterable

from .uninformed_cost_search import Problem, uniform_cost_search, extract_actions, extract_states

class SimpleGraphProblem(Problem):
    """Undirected weighted graph problem (actions == neighbor state name)."""
    def __init__(self, graph: Dict[str, Dict[str, int]], start: str, goal: str):
        super().__init__(start, goal)
        self.graph = graph

    def actions(self, state: str) -> Iterable[str]:
        return self.graph.get(state, {}).keys()

    def result(self, state: str, action: str) -> str:
        return action

    def action_cost(self, state: str, action: str, state2: str) -> float:
        return float(self.graph[state][state2])

def build_sample_graph() -> Dict[str, Dict[str, int]]:
    """
      A --1-- B --2-- D --1-- G
      |       \--5-- E --2--/
      \--4-- C --3-- F --2--/
    Optimal A->B->D->G has total cost 4.
    """
    return {
        "A": {"B": 1, "C": 4},
        "B": {"A": 1, "D": 2, "E": 5},
        "C": {"A": 4, "F": 3},
        "D": {"B": 2, "G": 1},
        "E": {"B": 5, "G": 2},
        "F": {"C": 3, "G": 2},
        "G": {"D": 1, "E": 2, "F": 2},
    }

def run_ucs_demo() -> None:
    graph = build_sample_graph()
    problem = SimpleGraphProblem(graph, start="A", goal="G")

    result = uniform_cost_search(problem)
    if not result:
        print("\n== UCS on weighted graph ==")
        print("No solution.")
        return

    print("\n== UCS on weighted graph ==")
    print("States :", " -> ".join(extract_states(result)))
    print("Actions:", extract_actions(result))
    print("Cost   :", result.path_cost)