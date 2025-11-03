from __future__ import annotations
from typing import Optional
from ai_searches.depth_limited_search import Problem, Node, depth_limited_search, print_dls_result

def iterative_deepening_search(problem: Problem, max_depth: int = 50) -> Optional[Node]:
    """
        Iterative Deepening Search (IDS)
        Repeatedly applies Depth-Limited Search, increasing the limit until
        a solution is found or the maximum depth is reached.
        """
    for depth in range(max_depth + 1):
        print(f"\n[IDS] Running depth-limited search with limit={depth}")
        result, node = depth_limited_search(problem, limit = depth)
        if result == "success":
            print(f"[IDS] Success found at depth {depth}")
            return node
        elif result == "failure":
            # no more nodes to explore
            print("[IDS] Failure — no nodes left to expand.")
            return None
    # if "cutoff", continue to next iteration
    print("[IDS] Reached max_depth with no solution.")
    return None

def run_iterative_demo(problem: Problem) -> None:
    node = iterative_deepening_search(problem, max_depth=10)
    if node:
        print_dls_result("Iterative Deepening Search (IDS)", ("success", node))
    else:
        print("\nNo solution found by IDS.")