from tests import Testcases


if __name__ == "__main__":
    test_manager = Testcases(1000)
    results = test_manager.run_concurrently()
    print(results["astar"])
    print(results["bfs"])
