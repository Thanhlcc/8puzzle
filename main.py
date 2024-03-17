import search
from game import EightPuzzle
from tests import Testcases


def start_test_case():
    test_manager = Testcases(1000)
    results = test_manager.run_concurrently()
    print(results["astar"])
    print(results["bfs"])


if __name__ == "__main__":
    raw_input = input("Enter initial state")
    plat_array = [int(x) for x in raw_input.split(' ')]
    matrix = [list(plat_array[i:i + 3]) for i in range(0, 9, 3)]

    # Get algorithm
    code = input('Choose algorithm: "1" for BFS, "2" for A*: ')
    strategy = search.BFS() if code == "1" else search.AStar(Testcases.heuristic_f)

    game = EightPuzzle(matrix, strategy)
    game.execute()
    game.show()

