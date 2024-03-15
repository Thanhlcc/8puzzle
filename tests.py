import itertools
import logging
import os
import random

from node import Node
from search import GraphSearch
import search
from game import EightPuzzle

logging.basicConfig(level=logging.DEBUG)


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
                map(lambda goal_ord: abs(cell_ord['x'] - goal_ord['x']) + abs(cell_ord['y'] - goal_ord['y']),
                    goal_ords))
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
                testcase = [list(row) for row in itertools.batched(digits, n=3)]
                Testcases.__test_cases.append(testcase)

    def test_astar(self):
        searcher = search.AStar(Testcases.heuristic_f)
        for i, testcase in enumerate(Testcases.__test_cases):
            try:
                testcase = [[4, 5, 7], [3, 1, 2], [6, 0, 8]]
                actions, overall_cost = EightPuzzle(testcase, searcher).execute()
                if overall_cost > 0:
                    logging.debug(f"TC-{i}: {testcase}")
                    logging.debug(f"Solution {i}:\n{actions}")
                    # GraphSearch.show(Node(testcase), actions, f"TC-{i}")
                    break
                else:
                    logging.info(f"TC-{i} is unsolvable")
                    logging.info(testcase)
            except:
                logging.error(f"Long running testcase TC-{i}:\n{testcase}")