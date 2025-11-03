# ai_searches/dfs.py
from __future__ import annotations
from typing import Dict, List, Any, Optional, Set

Graph = Dict[Any, List[Any]]

def dfs_recursive(graph: Graph, start: Any, goal: Optional[Any] = None):
    """
    Practical DFS (recursive) for graphs.
    - Uses a global visited set (no cycle on re-visits)
    - Keeps a parent map for path reconstruction to goal
    Returns: {"order": [...], "path": [...], "visited": set(...)}
    """
    visited: Set[Any] = set()
    parent: Dict[Any, Optional[Any]] = {start: None}
    order: List[Any] = []
    found_goal = False

    def visit(u: Any) -> bool:
        nonlocal found_goal
        visited.add(u)
        order.append(u)
        if goal is not None and u == goal:
            found_goal = True
            return True
        # iterate neighbors in the given order (stable, predictable)
        for v in graph.get(u, []):
            if v not in visited:
                parent[v] = u
                if visit(v):
                    return True
        return False

    visit(start)

    path: List[Any] = []
    if goal is not None and found_goal:
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
        path.reverse()
    else:
        # No goal specified or not found -> path = [start] for consistency
        path = [start]

    return {"order": order, "path": path, "visited": visited}


def dfs_iterative(graph: Graph, start: Any, goal: Optional[Any] = None):
    """
    Practical DFS (iterative, stack-based) for graphs.
    - Uses a global visited set
    - Keeps parent for path reconstruction
    NOTE: To mimic recursive order, push neighbors in reverse order.
    """
    visited: Set[Any] = set()
    parent: Dict[Any, Optional[Any]] = {start: None}
    order: List[Any] = []

    stack: List[Any] = [start]
    found_goal = False

    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        order.append(u)

        if goal is not None and u == goal:
            found_goal = True
            break

        neighbors = graph.get(u, [])
        # push reversed to simulate the same LIFO exploration order as recursion
        for v in reversed(neighbors):
            if v not in visited:
                if v not in parent:
                    parent[v] = u
                stack.append(v)

    path: List[Any] = []
    if goal is not None and found_goal:
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
        path.reverse()
    else:
        path = [start]

    return {"order": order, "path": path, "visited": visited}