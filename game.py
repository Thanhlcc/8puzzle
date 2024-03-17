import itertools
from copy import deepcopy

from graphviz import Digraph

from node import Node
from search import GraphSearch


class EightPuzzle():
    goals = [
        [[0, 1, 2], [3, 4, 5], [6, 7, 8]],
        [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
    ]

    def __init__(self, initial: list[list[int]], search_strategy: GraphSearch):
        self.initial = initial
        self.searcher = search_strategy
        self.cost = 0
        self.actions = []

    def execute(self) -> tuple:
        if EightPuzzle.checkSolvability(self.initial):
            self.actions, self.cost, no_expanded = self.searcher.search(
                src=Node(self.initial),
                dsts=[Node(goal) for goal in EightPuzzle.goals]
            )
            return self.actions, self.cost
        return [], -1

    def draw(self):
        nodes: list[Node] = self.searcher.reconstruct(Node(self.initial))
        dot = Digraph()
        for node in nodes:
            node.draw(dot)
        return dot

    def show(self):
        if self.cost:
            print("Actions: ", self.actions)
            print("Cost: ", self.cost)
            return self.draw()
        else:
            print("The input state is not SOLVABLE")

    @staticmethod
    def checkSolvability(initial_state: list[list[int]]):
        inversion_num = 0
        it = itertools.chain.from_iterable(initial_state)
        for tile in it:
            if tile == 0:
                continue
            for successor in deepcopy(it):
                if successor != 0 and tile > successor:
                    inversion_num += 1
        return inversion_num % 2 == 0
