import logging
import random
import threading

from node import Node
from search import GraphSearch
import search
from game import EightPuzzle

logging.basicConfig(level=logging.DEBUG)


class Testcases:

    def __init__(self, threshold: int):
        self.THRESHOLD = threshold
        self.__test_cases = []
        self.generate_random_seq(True)

    @staticmethod
    def heuristic_f(current_state: list[list[int]]):
        cell_score = {
            "goal1": [],
            "goal2": []
        }
        for cell in range(9):
            cell_ord = Node.index(current_state, cell)
            goal_ords = [Node.index(goal, cell) for goal in EightPuzzle.goals]
            hs: list[int] = list(
                map(lambda goal_ord: abs(cell_ord['x'] - goal_ord['x']) + abs(cell_ord['y'] - goal_ord['y']),
                    goal_ords))
            cell_score["goal1"].append(hs[0])
            cell_score["goal2"].append(hs[1])
        return min(sum(cell_score['goal1']), sum(cell_score['goal2']))

    def generate_random_seq(self, only_valid_case=False):
        # generate 1000 random sequence of number
        while len(self.__test_cases) < self.THRESHOLD:
            digits = list(range(9))
            random.shuffle(digits)
            if digits not in self.__test_cases:
                testcase = [list(digits[i:i + 3]) for i in range(0, 9, 3)]
                if only_valid_case and not EightPuzzle.checkSolvability(testcase):
                    continue
                self.__test_cases.append(testcase)

    # def test_astar(self):
    #     searcher = search.AStar(Testcases.heuristic_f)
    #     counter = 0
    #     result = dict()
    #     for testcase in self.__test_cases:
    #         actions, overall_cost = EightPuzzle(testcase, searcher).execute()
    #         if overall_cost > 0:
    #             logging.debug(f"TC-{counter}: {testcase}")
    #             logging.debug(f"Solution {counter}:\n{actions}")
    #             GraphSearch.show(Node(testcase), actions, "solutions/astar", f"TC-{counter}")
    #         else:
    #             logging.info(f"TC-{counter} is unsolvable")
    #             logging.info(testcase)
    #         result[counter] = overall_cost
    #         counter += 1
    #     return result
    #
    # def test_bfs(self):
    #     counter = 0
    #     result = dict()
    #     for testcase in self.__test_cases:
    #
    #         # testcase= [[1, 8, 2], [0, 4, 3], [7, 6, 5]]
    #         actions, overall_cost = EightPuzzle(testcase, search.BFS()).execute()
    #         if overall_cost > 0:
    #             logging.debug(f"TC-{counter}: {testcase}")
    #             logging.debug(f"Solution {counter}:\n{actions}")
    #             GraphSearch.show(Node(testcase), actions, "solutions/bfs", f"TC-{counter}")
    #         else:
    #             logging.info(f"TC-{counter} is unsolvable")
    #             logging.info(testcase)
    #         result[counter] = overall_cost
    #         counter += 1
    #         # break
    #     return result

    def run_concurrently(self):
        results_bfs, results_astar = [], []

        def run_test_case_wrapper(test_id, testcase, searcher):
            result = Testcases.run_testcase(test_id, testcase, searcher)
            if isinstance(searcher, search.AStar):
                results_astar.append(result)
            if isinstance(searcher, search.BFS):
                results_bfs.append(result)

        counter = 0
        threads = []
        for testcase in self.__test_cases:
            thread1 = threading.Thread(target=run_test_case_wrapper, args=(counter, testcase, search.AStar(Testcases.heuristic_f)))
            # thread2 = threading.Thread(target=run_test_case_wrapper, args=(counter, testcase, search.BFS()))
            counter += 1
            thread1.start()
            # thread2.start()
            threads.append(thread1)
            # threads.append(thread2)

        for thread in threads:
            thread.join()
        return {
            "astar": results_astar,
            "bfs": results_bfs
        }

    @staticmethod
    def run_testcase(test_id, testcase, searcher):
        actions, overall_cost = EightPuzzle(testcase, searcher).execute()
        if overall_cost > 0:
            # logging.debug(f"TC-{counter}: {testcase}")
            # logging.debug(f"Solution {counter}:\n{actions}")
            GraphSearch.show(Node(testcase), actions, "solutions/bfs" if isinstance(searcher, search.BFS) else "solutions/astar", f"TC-{test_id}")
            return overall_cost
        else:
            logging.info(f"TC-{test_id} is unsolvable")
            logging.info(testcase)
