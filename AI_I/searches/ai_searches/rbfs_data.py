# ai_searches/grid_problem_rbfs.py
from __future__ import annotations
from typing import Iterable, List, Tuple

from ai_searches.recursive_best_first_search import Problem, recursive_best_first_search, print_solution, Node

Coord = Tuple[int, int]

class GridProblem(Problem):
    """
    4-邻接网格；动作 U/D/L/R；可以设置墙（不可通行）
    State: (row, col)
    """
    def __init__(self, rows: int, cols: int, walls: List[Coord], start: Coord, goal: Coord):
        super().__init__(start, goal)
        self.rows = rows
        self.cols = cols
        self.walls = set(walls)

    def in_bounds(self, s: Coord) -> bool:
        r, c = s
        return 0 <= r < self.rows and 0 <= c < self.cols

    def passable(self, s: Coord) -> bool:
        return s not in self.walls

    def actions(self, state: Coord) -> Iterable[str]:
        (r, c) = state
        candidates = {
            'U': (r - 1, c),
            'D': (r + 1, c),
            'L': (r, c - 1),
            'R': (r, c + 1),
        }
        for a, s2 in candidates.items():
            if self.in_bounds(s2) and self.passable(s2):
                yield a

    def result(self, state: Coord, action: str) -> Coord:
        r, c = state
        if action == 'U': return (r - 1, c)
        if action == 'D': return (r + 1, c)
        if action == 'L': return (r, c - 1)
        if action == 'R': return (r, c + 1)
        return state  # shouldn't happen

# ---------- Heuristic ----------
def manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# ---------- Demo for main ----------
def run_rbfs_demo() -> None:
    walls = [(1, 1), (1, 2), (2, 1)]  # 障碍
    start = (0, 0)
    goal = (3, 3)
    problem = GridProblem(rows=4, cols=4, walls=walls, start=start, goal=goal)

    # f(n) = g(n) + h(n)；RBFS 内部会在递归中更新 f 限制
    def h(state: Coord) -> float:
        return float(manhattan(state, goal))

    node = recursive_best_first_search(problem, h)
    print_solution("RBFS (A*-like, linear memory) on 4x4 Grid", node)