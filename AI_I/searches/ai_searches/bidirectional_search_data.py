from __future__ import annotations
from typing import Iterable, List, Tuple, Set

from ai_searches.bidirectional_search import (
    Problem, Node,
    bibf_search, print_solution
)

Coord = Tuple[int, int]

class GridProblem(Problem):
    """
    4-neighbor grid with walls. Undirected moves: U/D/L/R (unit cost).
    """
    def __init__(self, rows: int, cols: int, walls: List[Coord], start: Coord, goal: Coord):
        super().__init__(initial=start, goal=goal)
        self.rows = rows
        self.cols = cols
        self.walls: Set[Coord] = set(walls)

    def in_bounds(self, s: Coord) -> bool:
        r, c = s
        return 0 <= r < self.rows and 0 <= c < self.cols

    def passable(self, s: Coord) -> bool:
        return s not in self.walls

    def actions(self, state: Coord) -> Iterable[str]:
        r, c = state
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
        return state

    def action_cost(self, state: Coord, action: str, state2: Coord) -> float:
        return 1.0

# ---------- Heuristic ----------
# h(n)
def manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# ---------- Demo runner (exported to main) ----------
def run_bibf_demo() -> None:
    rows, cols = 6, 6
    walls = [(1,1), (1,2), (2,1), (3,3), (2,4)]
    start = (0, 0)
    goal  = (5, 5)

    # Forward problem: start -> goal
    problemF = GridProblem(rows, cols, walls, start=start, goal=goal)
    # Backward problem: goal -> start (same dynamics because grid is undirected)
    problemB = GridProblem(rows, cols, walls, start=goal, goal=start)

    # fF(n) = g(n) + h(n) with h = Manhattan to goal
    def fF(n: Node) -> float:
        return n.path_cost + manhattan(n.state, goal)

    # fB(n) = g_b(n) + h_b(n) with h_b = Manhattan to start
    def fB(n: Node) -> float:
        return n.path_cost + manhattan(n.state, start)

    node = bibf_search(problemF, fF, problemB, fB)
    print_solution("Bi-directional Best-First (A* on both ends)", node)