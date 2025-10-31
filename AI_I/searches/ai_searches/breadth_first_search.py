from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable, Optional, Dict, List
from collections import deque
import heapq

# ==========================
# Node
# ==========================
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


# ==========================
# Abstract Problem
# ==========================
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


# ==========================
# EXPAND
# ==========================
def expand(problem: Problem, node: Node) -> Iterable[Node]:
    """Generate successors."""
    s = node.state
    for action in problem.actions(s):
        s2 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s2)
        yield Node(state=s2, parent=node, action=action, path_cost=cost)


# ==========================
# Breadth-First Search (BFS)
# ==========================
def breadth_first_search(problem: Problem) -> Optional[Node]:
    node = Node(problem.initial)
    if problem.is_goal(node.state):
        return node

    frontier = deque([node])
    reached = {problem.initial}

    while frontier:
        node = frontier.popleft()
        for child in expand(problem, node):
            s = child.state
            if problem.is_goal(s):
                return child
            if s not in reached:
                reached.add(s)
                frontier.append(child)
    return None


# ==========================
# Uniform-Cost Search (UCS)
# ==========================
@dataclass(order=True)
class PrioritizedItem:
    priority: float
    count: int
    node: Node


def best_first_search(problem: Problem, f) -> Optional[Node]:
    start = Node(problem.initial)
    frontier: List[PrioritizedItem] = []
    counter = 0
    heapq.heappush(frontier, PrioritizedItem(f(start), counter, start))
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
                heapq.heappush(frontier, PrioritizedItem(f(child), counter, child))
    return None


def uniform_cost_search(problem: Problem) -> Optional[Node]:
    """Uniform-cost = best-first with f(n) = path_cost."""
    return best_first_search(problem, lambda n: n.path_cost)


# ==========================
# Utility: path extractor
# ==========================
def extract_path(node: Optional[Node]) -> list[Any]:
    if not node:
        return []
    return [n.state for n in node.path()]