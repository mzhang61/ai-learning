from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable, Optional, List

# ==========================
# Core node
# ==========================
@dataclass
class Node:
    state: Any
    parent: Optional["Node"] = None
    action: Optional[Any] = None
    path_cost: float = 0.0
    depth: int = 0

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
# EXPAND (generate successors)
# ==========================
def expand(problem: Problem, node: Node) -> Iterable[Node]:
    s = node.state
    for action in problem.actions(s):
        s2 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s2)
        yield Node(state=s2, parent=node, action=action, path_cost=cost, depth=node.depth + 1)

# ==========================
# Cycle check (on current path)
# ==========================
def is_cycle(node: Node) -> bool:
    s = node.state
    p = node.parent
    while p:
        if p.state == s:
            return True
        p = p.parent
    return False

# ==========================
# Depth-Limited Search (DLS)
# Returns: ("success", node) | ("cutoff", None) | ("failure", None)
# ==========================
def depth_limited_search(problem: Problem, limit: int) -> tuple[str, Optional[Node]]:
    stack: List[Node] = [Node(state=problem.initial, depth=0)]
    result: str = "failure"  # will flip to "cutoff" if we ever exceed the limit

    while stack:
        node = stack.pop()

        if problem.is_goal(node.state):
            return "success", node

        if node.depth > limit:
            result = "cutoff"
            # don't expand beyond the limit
            continue

        if not is_cycle(node):
            for child in expand(problem, node):
                stack.append(child)

    return result, None

# ==========================
# Helpers
# ==========================
def extract_actions(node: Optional[Node]) -> List[Any]:
    if not node:
        return []
    p = node.path()
    return [n.action for n in p][1:]  # skip root's None action

def print_dls_result(label: str, res: tuple[str, Optional[Node]]) -> None:
    status, node = res
    print(f"\n== {label} ==")
    if status == "success":
        print("Status : success")
        print("Actions:", extract_actions(node))
        print("Cost   :", node.path_cost)
        print("Depth  :", node.depth)
    elif status == "cutoff":
        print("Status : cutoff (depth limit reached, try a larger limit)")
    else:
        print("Status : failure (no solution in the searched space)")