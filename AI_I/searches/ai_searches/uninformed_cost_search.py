# ai_searches/ucs.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable, Optional, Dict, List, Callable
import heapq

"""
UCS also called (Dijkstra Algorithm)
Uninformed cost is picking the path with lowest cost without knowing the remain cost or how far from the goal.
g(n)
"""

# --------------------------
# Core data structures
# --------------------------
@dataclass
class Node:
    state: Any
    parent: Optional["Node"] = None
    action: Optional[Any] = None
    path_cost: float = 0.0

    def path(self) -> List["Node"]:
        n, acc = self, []
        while n:
            acc.append(n)
            n = n.parent
        return list(reversed(acc))

class Problem:
    def __init__(self, initial: Any, goal: Any):
        self.initial = initial
        self.goal = goal

    def is_goal(self, state: Any) -> bool:
        return state == self.goal

    def actions(self, state: Any) -> Iterable[Any]:
        raise NotImplementedError

    def result(self, state: Any, action: Any) -> Any:
        raise NotImplementedError

    def action_cost(self, state: Any, action: Any, state2: Any) -> float:
        return 1.0

# --------------------------
# Expand
# --------------------------
def expand(problem: Problem, node: Node) -> Iterable[Node]:
    s = node.state
    for action in problem.actions(s):
        s2 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s2)
        yield Node(state=s2, parent=node, action=action, path_cost=cost)

# --------------------------
# UCS (Dijkstra)
# --------------------------
@dataclass(order=True)
class PrioritizedItem:
    priority: float
    count: int
    node: Node

def uniform_cost_search(problem: Problem) -> Optional[Node]:
    """Uniform-cost search == best-first with f(n) = g(n) = path_cost."""
    start = Node(problem.initial)
    frontier: List[PrioritizedItem] = []
    counter = 0
    heapq.heappush(frontier, PrioritizedItem(start.path_cost, counter, start))
    reached: Dict[Any, Node] = {problem.initial: start}

    while frontier:
        current = heapq.heappop(frontier).node
        if problem.is_goal(current.state):
            return current

        for child in expand(problem, current):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                counter += 1
                heapq.heappush(frontier, PrioritizedItem(child.path_cost, counter, child))
    return None

# --------------------------
# Helpers
# --------------------------
def extract_actions(node: Optional[Node]) -> List[Any]:
    if not node:
        return []
    return [n.action for n in node.path()][1:]  # skip root's None

def extract_states(node: Optional[Node]) -> List[Any]:
    if not node:
        return []
    return [n.state for n in node.path()]