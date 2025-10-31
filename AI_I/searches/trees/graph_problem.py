from __future__ import annotations
from collections import deque
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TreeNode:
    """A simple tree node for a search tree."""
    state: str
    children: List["TreeNode"] = field(default_factory=list)

    def add(self, *kids: "TreeNode") -> "TreeNode":
        self.children.extend(kids)
        return self


def build_demo_tree() -> TreeNode:
    """
    Build a tiny static search tree:

                A
              / | \
             B  C  D
            / \  \
           E   F  G

    """
    A = TreeNode("A")
    B = TreeNode("B")
    C = TreeNode("C")
    D = TreeNode("D")
    E = TreeNode("E")
    F = TreeNode("F")
    G = TreeNode("G")

    B.add(E, F)
    C.add(G)
    A.add(B, C, D)
    return A


# ---------- Traversals ----------
def dfs_preorder(root: Optional[TreeNode]) -> List[str]:
    """Depth-First (preorder): root -> children (left to right)."""
    if not root:
        return []
    result: List[str] = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.state)
        # push right-to-left so left child is processed first
        for child in reversed(node.children):
            stack.append(child)
    return result


def bfs_level_order(root: Optional[TreeNode]) -> List[str]:
    """Breadth-First (level order)."""
    if not root:
        return []
    result: List[str] = []
    q = deque([root])
    while q:
        node = q.popleft()
        result.append(node.state)
        for child in node.children:
            q.append(child)
    return result


# ---------- Pretty print (ASCII) ----------
def print_tree_ascii(root: Optional[TreeNode]) -> None:
    """A tiny ASCII printer for small trees."""
    if not root:
        print("(empty)")
        return

    # BFS to gather levels
    levels: List[List[str]] = []
    q = deque([(root, 0)])
    while q:
        node, d = q.popleft()
        if d == len(levels):
            levels.append([])
        levels[d].append(node.state)
        for c in node.children:
            q.append((c, d + 1))

    print("\n== Search Tree (static) ==")
    for depth, nodes in enumerate(levels):
        print(f"Level {depth}: " + "  ".join(nodes))


# ---------- Runner for main ----------
def run_static_search_tree_demo() -> None:
    root = build_demo_tree()
    print_tree_ascii(root)

    print("\nDFS (preorder): ", dfs_preorder(root))
    print("BFS (level)   : ", bfs_level_order(root))