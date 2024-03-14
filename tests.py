import logging
import random

from node import Node
from search import GraphSearch
import search
from game import EightPuzzle


class Testcases:
    __test_cases = []
    THRESHOLD = 1000

    def __init__(self, threshold: int):
        Testcases.THRESHOLD = threshold
        Testcases.generate_random_seq()

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
                map(lambda goal_ord: abs(cell_ord['x'] - goal_ord['x']) + abs(cell_ord['y'] - goal_ord['y']), goal_ords))
            # print(f"Cell {cell}: curr(x:{cell_ord['x']}, y:{cell_ord['y']} ==== distance {hs})")
            cell_score["goal1"].append(hs[0])
            cell_score["goal2"].append(hs[1])
        return min(sum(cell_score['goal1']), sum(cell_score['goal2']))

    @staticmethod
    def generate_random_seq():
        # generate 1000 random sequence of number
        while len(Testcases.__test_cases) < Testcases.THRESHOLD:
            digits = list(range(9))
            random.shuffle(digits)
            if digits not in Testcases.__test_cases:
                testcase = []
                for i in range(0,9,3):
                    testcase.append(digits[i:i+3])
                Testcases.__test_cases.append(testcase)

    def test_astar(self):
        searcher = search.AStar(Testcases.heuristic_f)
        testcase = [[2, 5, 7], [4, 0, 8], [3, 6, 1]]
        # for i, testcase in enumerate(Testcases.__test_cases):
        # try:
        actions, overall_cost = EightPuzzle(Node(testcase), searcher).execute()
        if len(actions) == 0:
            logging.log(f"Test case {1} is unsolvable")
        # except:
        #     print(f"Long running test cases: \n{testcase}")

        # print(f"TC-{i}: {testcase}")

        # print(f"Solution {i}:\n{actions}")
        # GraphSearch.show(Node(testcase), actions, f"tc_{i}")
