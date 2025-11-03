# ai_searches/rbfs.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable, Optional, Callable, List, Tuple

# ==========================
# Core node & problem types
# ==========================
@dataclass
class Node:
    state: Any
    parent: Optional["Node"] = None
    action: Optional[Any] = None
    path_cost: float = 0.0  # g(n)
    depth: int = 0
    f: float = 0.0          # f(n) = g(n) + h(n); RBFS会更新

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

# ==========================
# Utilities
# ==========================
def expand(problem: Problem, node: Node) -> Iterable[Node]:
    """Generate successors with updated (g, depth). f由RBFS计算/更新。"""
    s = node.state
    for action in problem.actions(s):
        s2 = problem.result(s, action)
        g2 = node.path_cost + problem.action_cost(s, action, s2)
        yield Node(state=s2, parent=node, action=action, path_cost=g2, depth=node.depth + 1)

def is_cycle(node: Node) -> bool:
    """Detect cycles along the current path (工程里常见做法，避免陷入环)."""
    s, p = node.state, node.parent
    while p:
        if p.state == s:
            return True
        p = p.parent
    return False

def extract_solution(node: Optional[Node]) -> Tuple[List[Any], float]:
    if not node:
        return [], float("inf")
    p = node.path()
    actions = [n.action for n in p][1:]  # 跳过根的 None action
    return actions, p[-1].path_cost

def print_solution(label: str, node: Optional[Node]) -> None:
    print(f"\n== {label} ==")
    if node is None:
        print("No solution.")
        return
    actions, cost = extract_solution(node)
    print(f"Actions: {actions}")
    print(f"Path cost: {cost}")

# ==========================
# RBFS 核心
# ==========================
def _rbfs(problem: Problem,
          node: Node,
          f_limit: float,
          h: Callable[[Any], float]) -> Tuple[Optional[Node], float]:
    """
    返回：(solution_node 或 None, 新的 f_limit 备份值)
    参考 AIMA 伪代码：对每层维护 best/alternative 的 f 值并回溯。
    """
    # Goal test
    if problem.is_goal(node.state):
        return node, node.f

    # 展开子节点
    successors = []
    for child in expand(problem, node):
        if is_cycle(child):
            continue
        # f(child) = max(g+h, node.f) —— 确保非递减
        child.f = max(child.path_cost + h(child.state), node.f)
        successors.append(child)

    if not successors:
        return None, float("inf")

    while True:
        # 选出 f 最小的 best 与次优 alternative
        successors.sort(key=lambda n: n.f)
        best = successors[0]
        alternative = successors[1].f if len(successors) > 1 else float("inf")

        # 超过当前允许上限，回溯，并把 best 的 f 作为新的限制反馈
        if best.f > f_limit:
            return None, best.f

        # 递归向下，但限制为当前层可选的更小上界
        result, best.f = _rbfs(problem, best, min(f_limit, alternative), h)
        if result is not None:
            return result, best.f
        # 否则继续循环，等价于考虑下一个更好的分支（best.f 已被“备份”更新）
        # 循环会重新排序 successors（best 的 f 可能增大，从而被 alternative 超过）

def recursive_best_first_search(problem: Problem,
                                h: Callable[[Any], float]) -> Optional[Node]:
    """
    RBFS 外层封装：初始化根节点 f，并调用递归。
    """
    start = Node(state=problem.initial, path_cost=0.0, depth=0)
    start.f = h(start.state)
    solution, _ = _rbfs(problem, start, float("inf"), h)
    return solution