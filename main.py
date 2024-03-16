from tests import Testcases


if __name__ == "__main__":
    test_manager = Testcases(10)
    # result1 = test_manager.test_astar()
    result2 = test_manager.test_bfs()
    # print(result1)
    print(result2)
