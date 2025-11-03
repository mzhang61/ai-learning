from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple
import heapq

# ==========================
# Core data structures
# ==========================
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
    path_cost: float = 0.0

    def path(self) -> List["Node"]:
        n, acc = self, []
        while n:
            acc.append(n)
            n = n.parent
        return list(reversed(acc))

# ==========================
# Problem interface
# ==========================
class Problem:
    def __init__(self, initial: Any, goal: Any):
        self.initial = initial   # root state for this direction
        self.goal = goal         # target state for this direction

    def is_goal(self, state: Any) -> bool:
        return state == self.goal

    def actions(self, state: Any) -> Iterable[Any]:
        raise NotImplementedError

    def result(self, state: Any, action: Any) -> Any:
        raise NotImplementedError

    def action_cost(self, state: Any, action: Any, state2: Any) -> float:
        return 1.0  # default cost

# ==========================
# Expand
# ==========================
def expand(problem: Problem, node: Node) -> Iterable[Node]:
    s = node.state
    for action in problem.actions(s):
        s2 = problem.result(s, action)
        # g(n) path cost from start to current
        cost = node.path_cost + problem.action_cost(s, action, s2)
        yield Node(state=s2, parent=node, action=action, path_cost=cost)

# ==========================
# Helpers for stitching a solution
# ==========================
def _clone_chain(nodes: List[Node]) -> Node:
    """Clone a list of nodes into a new singly-linked chain and return the tail (last node)."""
    head_copy = Node(state=nodes[0].state, parent=None, action=None, path_cost=0.0)
    prev = head_copy
    for i in range(1, len(nodes)):
        n = nodes[i]
        new_node = Node(state=n.state, parent=prev, action=n.action,
                        path_cost=prev.path_cost + (0.0 if n.action is None else 1.0))
        prev = new_node
    return prev  # tail

def join_nodes(direction: str, meet_child: Node, other_side_node: Node) -> Node:
    """
    Build a full path Node chain by joining the forward and backward partial paths at the meeting state.
    direction: 'F' if we just expanded forward side; 'B' if backward side.
    meet_child: node from the side we just expanded, ending at meeting state s
    other_side_node: node from the opposite frontier, also at state s
    Assumption: costs are symmetric for demo; for asymmetric domains, you must handle costs carefully.
    """
    # Forward partial path: start -> ... -> s
    f_nodes = meet_child.path()

    # Backward partial path: goal -> ... -> s
    b_nodes = other_side_node.path()

    # We need s -> ... -> goal. Reverse the backward chain and drop the meeting s to avoid duplicate.
    b_nodes_rev = list(reversed(b_nodes))  # [s, ..., goal]
    if len(b_nodes_rev) > 0:
        b_nodes_rev = b_nodes_rev[1:]  # drop s

    # Rebuild a single chain by cloning forward nodes, then append the reversed backward chain states.
    # We don't carry over exact actions for backward; we mark action as None for the stitch,
    # then add synthetic actions like '→(state)' just for readability.
    # Build head
    head = Node(state=f_nodes[0].state, parent=None, action=None, path_cost=0.0)
    prev = head
    # attach forward (skip head already added)
    for i in range(1, len(f_nodes)):
        st = f_nodes[i].state
        act = f_nodes[i].action
        cost_step = 1.0 if act is not None else 0.0
        cur = Node(state=st, parent=prev, action=act, path_cost=prev.path_cost + cost_step)
        prev = cur
    # attach backward reversed tail
    for n in b_nodes_rev:
        # synthetic action text for clarity (optional)
        act = f"→{n.state}"
        cur = Node(state=n.state, parent=prev, action=act, path_cost=prev.path_cost + 1.0)
        prev = cur

    return prev  # tail = goal

# ==========================
# Proceed one side
# ==========================
def proceed(direction_label: str,
            problem: Problem,
            frontier: List[PrioritizedItem],
            reached_this: Dict[Any, Node],
            reached_other: Dict[Any, Node],
            f_eval: Callable[[Node], float],
            counter_ref: List[int],
            current_best: Optional[Node]) -> Optional[Node]:
    """
    Expand top node of one frontier; if collision with other side, possibly improve solution.
    """
    if not frontier:
        return current_best

    node = heapq.heappop(frontier).node

    for child in expand(problem, node):
        s = child.state
        if (s not in reached_this) or (child.path_cost < reached_this[s].path_cost):
            reached_this[s] = child
            counter_ref[0] += 1
            heapq.heappush(frontier, PrioritizedItem(f_eval(child), counter_ref[0], child))

        if s in reached_other:
            candidate = join_nodes(direction_label, child, reached_other[s])
            if current_best is None or candidate.path_cost < current_best.path_cost:
                current_best = candidate

    return current_best

# ==========================
# BIBF-SEARCH
# ==========================
def bibf_search(problemF: Problem, fF: Callable[[Node], float],
                problemB: Problem, fB: Callable[[Node], float]) -> Optional[Node]:
    """
    Bi-directional Best-First Search.
    For optimality guarantees you'd also include a tighter termination condition (bounds).
    Here we keep it practical: run until both frontiers are empty, tracking best meeting.
    """
    # init forward
    startF = Node(state=problemF.initial)
    reachedF: Dict[Any, Node] = {problemF.initial: startF}
    frontierF: List[PrioritizedItem] = []
    cF = [0]
    heapq.heappush(frontierF, PrioritizedItem(fF(startF), cF[0], startF))

    # init backward
    startB = Node(state=problemB.initial)  # here, initialB is the goal state of the original problem
    reachedB: Dict[Any, Node] = {problemB.initial: startB}
    frontierB: List[PrioritizedItem] = []
    cB = [0]
    heapq.heappush(frontierB, PrioritizedItem(fB(startB), cB[0], startB))

    solution: Optional[Node] = None

    while frontierF or frontierB:
        # pick direction by comparing current best f-tops (tie: expand backward)
        topF = frontierF[0].priority if frontierF else float("inf")
        topB = frontierB[0].priority if frontierB else float("inf")

        if topF <= topB:
            solution = proceed('F', problemF, frontierF, reachedF, reachedB, fF, cF, solution)
        else:
            solution = proceed('B', problemB, frontierB, reachedB, reachedF, fB, cB, solution)

    return solution

# ==========================
# Helpers for printing
# ==========================
def extract_solution(node: Optional[Node]) -> Tuple[List[Any], float]:
    if not node:
        return ([], float("inf"))
    nodes = node.path()
    actions = [n.action for n in nodes][1:]  # skip root None
    return actions, node.path_cost

def print_solution(label: str, node: Optional[Node]) -> None:
    print(f"\n== {label} ==")
    if node is None:
        print("No solution.")
        return
    actions, cost = extract_solution(node)
    print(f"Actions: {actions}")
    print(f"Path cost: {cost}")