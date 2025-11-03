from __future__ import annotations
from typing import Iterable, List, Tuple

from ai_searches.a_star import Problem, a_star_search, print_solution, Node

Coord = Tuple[int, int]

class GridProblem(Problem):
    """
    4 adjacent squares + wall
    State: (row, col)
    Action: 'U','D','L','R'
    Move cost: 1
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

    def action_cost(self, state: Coord, action: str, state2: Coord) -> float:
        return 1.0

# -------- Heuristic: Manhattan distance (admissible & consistent in 4-neighbor grids) --------
def manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# -------- Demo used by main --------
def run_a_star_demo() -> None:
    walls = [(1, 1), (1, 2), (2, 1)]  # blocked cells
    start = (0, 0)
    goal = (3, 3)
    problem = GridProblem(grid_rows=4, grid_cols=4, walls=walls, start=start, goal=goal)

    def h(state: Coord) -> float:
        return float(manhattan(state, goal))

    node = a_star_search(problem, h_provider=h)
    print_solution("A* on 4x4 Grid", node)