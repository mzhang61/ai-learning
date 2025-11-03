from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Optional
import heapq

# --------------------------
# Core data structures
# --------------------------
@dataclass(order=True)
class PrioritizedItem:
    priority: float
    count: int
    node: "Node"

@dataclass
class Node:
    state: Any
    parent: Optional["Node"] = None
    action: Optional[Any] = None
    path_cost: float = 0.0  # g(n)

    def path(self) -> List["Node"]:
        n, acc = self, []
        while n:
            acc.append(n)
            n = n.parent
        return list(reversed(acc))

# --------------------------
# Problem interface
# --------------------------
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
        return 1.0  # default cost

# --------------------------
# Expand
# --------------------------
def expand(problem: Problem, node: Node) -> Iterable[Node]:
    s = node.state
    for action in problem.actions(s):
        s2 = problem.result(s, action)
        g2 = node.path_cost + problem.action_cost(s, action, s2)
        yield Node(state=s2, parent=node, action=action, path_cost=g2)

# --------------------------
# A* Search
# f(n) = g(n) + h(n)
#   g_provider: lambda node -> node.path_cost（通常就是 node.path_cost）
#   h_provider: lambda state -> 估价到目标的启发式
# --------------------------
def a_star_search(
    problem: Problem,
    h_provider: Callable[[Any], float],
) -> Optional[Node]:
    start = Node(state=problem.initial, parent=None, action=None, path_cost=0.0)

    def f(n: Node) -> float:
        # g(n) + h(n)
        return n.path_cost + h_provider(n.state)

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

# --------------------------
# Helpers
# --------------------------
def extract_solution(node: Optional[Node]) -> tuple[List[Any], float]:
    if not node:
        return ([], float("inf"))
    path_nodes = node.path()
    actions = [n.action for n in path_nodes][1:]  # skip root (action=None)
    return actions, node.path_cost

def print_solution(label: str, node: Optional[Node]) -> None:
    print(f"\n== {label} ==")
    if node is None:
        print("No solution.")
        return
    actions, cost = extract_solution(node)
    print(f"Actions: {actions}")
    print(f"Path cost: {cost}")