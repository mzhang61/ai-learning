from dataclasses import dataclass
from typing import Any, Optional, List

# ==========================
# Node definition
# ==========================

@dataclass
class Node:
    state: Any
    parent: Optional["Node"] = None
    action: Optional[Any] = None
    path_cost: float = 0.0

    def path(self) -> List["Node"]:
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

class Node1:
    def path(self):
        print("I am self ->", self)

# ==========================
# Example usage
# ==========================
if __name__ == "__main__":
    start = Node(state="A", path_cost=0)
    b = Node(state="B", parent=start, action="move_right", path_cost=1)
    c = Node(state="C", parent =b, action="move_right", path_cost=3)
    d = Node(state="D", parent=c, action="move_down", path_cost=5)

    print("Full path from start to D:")
    for n in d.path():
        print(f"State: {n.state}, action: {n.action}, Cost so far: {n.path_cost}")
    print("\nFinal total cost=", d.path_cost)

    d = Node1()
    d.path()
    Node1.path(d)