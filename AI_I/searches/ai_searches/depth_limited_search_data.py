from __future__ import annotations
from typing import Dict, Iterable, Any
from ai_searches.depth_limited_search import Problem, depth_limited_search, print_dls_result

# A small tree/graph-like problem:
# States are strings. Actions are "moving" to neighbors.
class SimpleTreeProblem(Problem):
    def __init__(self, graph: Dict[str, Dict[str, int]], start: str, goal: str):
        super().__init__(start, goal)
        self.graph = graph

    def actions(self, state: str) -> Iterable[str]:
        # neighbors (action names equal to next state for simplicity)
        return self.graph.get(state, {}).keys()

    def result(self, state: str, action: str) -> Any:
        # action is the next state name
        return action

    def action_cost(self, state: str, action: str, state2: str) -> float:
        return float(self.graph[state][state2])

def build_sample_tree() -> Dict[str, Dict[str, int]]:
    """
        A tiny tree rooted at 'A'. Goal is 'G' at depth 3.
           A
          / \
         B   C
        / \   \
       D  E    F
           \
            G   (goal)
    """
    return {
        "A": {"B": 1, "C": 1},
        "B": {"D": 1, "E": 1},
        "C": {"F": 1},
        "D": {},
        "E": {"G": 1},
        "F": {},
        "G": {},  # goal leaf
    }

def run_depth_limited_demo() -> None:
    graph = build_sample_tree()
    problem = SimpleTreeProblem(graph, start="A", goal="G")  # <-- start, not state

    # Try with a limit that's too small (cutoff expected)
    res1 = depth_limited_search(problem, limit=2)  # G is at depth 3
    print_dls_result("DLS with limit=2 (expect cutoff)", res1)

    # Try with a sufficient limit (success expected)
    res2 = depth_limited_search(problem, limit=3)
    print_dls_result("DLS with limit=3 (expect success)", res2)

    # Try with a larger limit (also success, same path)
    res3 = depth_limited_search(problem, limit=10)
    print_dls_result("DLS with limit=10 (success, same solution)", res3)