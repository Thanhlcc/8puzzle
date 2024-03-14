

from node import Node
from search import GraphSearch


class EightPuzzle():
    goals = [
        [[0, 1, 2], [3, 4, 5], [6, 7, 8]],
        [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
    ]

    def __init__(self, initial: Node, search_strategy: GraphSearch):
        self.initial = initial
        self.searcher = search_strategy
        self.cost = 0
        self.actions = []

    def execute(self) -> tuple:
        self.actions, self.cost = self.searcher.search(self.initial, [Node(goal) for goal in EightPuzzle.goals])
        return self.actions, self.cost

    def draw(self):
        nodes: list[Node] = self.searcher.reconstruct(self.initial, self.actions)
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
