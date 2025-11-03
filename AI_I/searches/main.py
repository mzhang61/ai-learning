from ai_searches.best_first_search_data import run_best_first_demo
from trees.graph_problem import run_static_search_tree_demo
from ai_searches.breadth_first_search_data import SimpleGraphProblem, build_sample_graph
from ai_searches.breadth_first_search import breadth_first_search, uniform_cost_search, extract_path
from ai_searches.depth_limited_search_data import run_depth_limited_demo, SimpleTreeProblem, build_sample_tree
from ai_searches.iterative_deepening_search import run_iterative_demo
from ai_searches.bidirectional_search_data import run_bibf_demo
from ai_searches.ucs_data import run_ucs_demo
from ai_searches.dfs import dfs_recursive, dfs_iterative
from ai_searches.dfs_data import build_sample_graph
from ai_searches.a_star_data import run_a_star_demo
from ai_searches.rbfs_data import run_rbfs_demo
# Press the green button in the gutter to run the script.


def run_dfs_demo():
    graph = build_sample_graph()
    start, goal = "A", "G"

    print("=== DFS Recursive (with goal) ===")
    res1 = dfs_recursive(graph, start=start, goal=goal)
    print("Visit order:", res1["order"])
    print("Path to goal:", res1["path"])
    print("Visited size:", len(res1["visited"]))

    print("\n=== DFS Iterative (with goal) ===")
    res2 = dfs_iterative(graph, start=start, goal=goal)
    print("Visit order:", res2["order"])
    print("Path to goal:", res2["path"])
    print("Visited size:", len(res2["visited"]))

    print("\n=== DFS Iterative (traversal only, no goal) ===")
    res3 = dfs_iterative(graph, start=start, goal=None)
    print("Visit order:", res3["order"])
    print("Path (no goal, returns [start]):", res3["path"])
def run_bfs_search_demo():
    graph = build_sample_graph()
    problem = SimpleGraphProblem(graph, start="A", goal="G")

    print("=== Breadth-First Search ===")
    bfs_result = breadth_first_search(problem)
    print("Path:", extract_path(bfs_result))

    print("\n=== Uniform-Cost Search ===")
    ucs_result = uniform_cost_search(problem)
    print("Path:", extract_path(ucs_result))

if __name__ == '__main__':
    # run_best_first_demo()

    # run_static_search_tree_demo()

    # run_bfs_search_demo()

    #run_depth_limited_demo()

    # run iterative-deepening-search below
    #graph = build_sample_tree()
    #problem = SimpleTreeProblem(graph, start="A", goal="G")
    #run_iterative_demo(problem)

    # run bidirectional search
    #run_bibf_demo()

    # uniformed cost search
    #run_ucs_demo()

    #run dfs
    #run_dfs_demo()

    # run a star search
    # run_a_star_demo()

    # run recursive best first search
    run_rbfs_demo()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
