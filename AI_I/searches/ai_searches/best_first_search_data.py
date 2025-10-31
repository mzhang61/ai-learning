from __future__ import annotations
from typing import Iterable, List, Tuple

from .best_first_search import Problem, best_first_search, print_solution, Node

Coord = Tuple[int, int]

class GridProblem(Problem):
    """
    A simple 4-neighbor grid with walls.
    State: (row, col)
    Actions: ('U','D','L','R') if inside bounds and not a wall.
    All moves cost 1 by default.
    """
    def __init__(self, grid_rows: int, grid_cols: int, walls: List[Coord], start: Coord, goal: Coord):
        super().__init__(start, goal)
        self.rows = grid_rows
        self.cols = grid_cols
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
        (r, c) = state
        if action == 'U': return (r - 1, c)
        if action == 'D': return (r + 1, c)
        if action == 'L': return (r, c - 1)
        if action == 'R': return (r, c + 1)
        return state  # should not happen

# ---------- Heuristic ----------
def manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# ---------- Demo runner used by main ----------
def run_best_first_demo() -> None:
    walls = [(1, 1), (1, 2), (2, 1)]  # blocked cells
    start = (0, 0)
    goal = (3, 3)
    problem = GridProblem(grid_rows=4, grid_cols=4, walls=walls, start=start, goal=goal)

    # A* evaluation function: f(n) = g(n) + h(n)
    def f(n: Node) -> float:
        return n.path_cost + manhattan(n.state, goal)

    node = best_first_search(problem, f)
    print_solution("Best-First Search (A*) on 4x4 Grid", node)