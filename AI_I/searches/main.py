from ai_searches.best_first_search_data import run_best_first_demo
from trees.graph_problem import run_static_search_tree_demo
from ai_searches.breadth_first_search_data import SimpleGraphProblem, build_sample_graph
from ai_searches.breadth_first_search import breadth_first_search, uniform_cost_search, extract_path

# Press the green button in the gutter to run the script.

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
    run_bfs_search_demo()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
