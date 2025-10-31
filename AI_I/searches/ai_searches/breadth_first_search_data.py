from ai_searches.breadth_first_search import Problem

# Define graph-based problem for BFS/UCS
class SimpleGraphProblem(Problem):
    """Undirected weighted graph problem."""
    def __init__(self, graph, start, goal):
        super().__init__(start, goal)
        self.graph = graph

    def actions(self, state):
        return self.graph.get(state, {}).keys()

    def result(self, state, action):
        return action

    def action_cost(self, state, action, state2):
        return self.graph[state][state2]


def build_sample_graph():
    """Return a small test graph."""
    graph = {
        "A": {"B": 1, "C": 4},
        "B": {"A": 1, "D": 2, "E": 5},
        "C": {"A": 4, "F": 3},
        "D": {"B": 2, "G": 1},
        "E": {"B": 5, "G": 2},
        "F": {"C": 3, "G": 2},
        "G": {"D": 1, "E": 2, "F": 2},
    }
    return graph