# ai_searches/dfs_data.py
from __future__ import annotations
from typing import Dict, List, Any

Graph = Dict[Any, List[Any]]

def build_sample_graph() -> Graph:
    """
    Undirected graph encoded as adjacency lists.
    A -- B -- D -- G
     \   |
      \  C -- F
          \
           E
    """
    return {
        "A": ["B", "C"],
        "B": ["A", "D", "C"],
        "C": ["A", "B", "F", "E"],
        "D": ["B", "G"],
        "E": ["C"],
        "F": ["C", "G"],
        "G": ["D", "F"],
    }