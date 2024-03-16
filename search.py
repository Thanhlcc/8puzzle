import heapq
from abc import abstractmethod, ABC
from copy import deepcopy

import timeout_decorator
from graphviz import Digraph

from node import Node
from typing import Callable


class GraphSearch(ABC):
    @abstractmethod
    def search(self, src: Node, dsts: list[Node]) -> list[str]:
        pass

    @staticmethod
    def reconstruct(src: Node) -> list[Node]:
        """
        Back tracking the path
        :param src: the starting node to trace back
        :return: the path generated by tracing from src node along the parent ref in the expanded to reach the root
        """
        path = list()
        curr = src
        while curr is not None:
            path.append(curr)
            curr = curr.parent
        return path[::-1]

    @staticmethod
    def show(initial: Node, actions: list[str], directory="solutions", filename=None):
        dot = Digraph()
        curr = initial
        curr.draw(dot)
        for action in actions:
            tmp = curr.get_successor(action, deepcopy(curr.state))
            if tmp is None: break
            curr = Node(state=tmp, parent=curr, action=action)
            curr.draw(dot)
        dot.render(filename=filename, directory=directory, cleanup=True)


class BFS(GraphSearch):
    def search(self, src: Node, dsts: list[Node]):
        explored = list()
        frontier = [src]

        while True:
            if len(frontier) == 0:
                return [], -1

            current = frontier.pop(0)
            # explored.add(current.get_id())
            explored.append(current.get_id())
            for successor in current.get_successors():
                if successor.get_id() not in explored and successor not in frontier:
                    if successor in dsts:
                        path = GraphSearch.reconstruct(successor)
                        return [node.action for node in path if node.action], len(path) - 1
                    frontier.append(successor)

    def goal_test(self, node: Node, dsts: list[Node]):
        return node.get_id() in [dst.get_id() for dst in dsts]


class AStar(GraphSearch):
    heuristic_f = lambda node: 0

    def __init__(self, heuristic_f: Callable[[list[list]], int]):
        self.frontier = []
        AStar.heuristic_f = heuristic_f

    # @timeout_decorator.timeout(10)
    def search(self, src: Node, dsts: list[Node]):
        """
        @Return: (actions, cost)
        - On failure, actions = [] and cost = -1
        - Otherwise, the actions contains the action sequence leading to goal state and cost is the result of summing the path
        """
        src = AStar.Node(state=src.state, cost=0)
        dsts = [self.Node(state=goal.state) for goal in dsts]
        expanded = set()
        self.frontier = [src]
        while len(self.frontier) != 0:
            curr = heapq.heappop(self.frontier)
            expanded.add(curr)
            if curr in dsts:
                path = GraphSearch.reconstruct(curr)
                return [node.action for node in path if node.action], curr.cost
            for succ in curr.get_successors():
                if succ not in expanded and succ not in self.frontier:
                    heapq.heappush(self.frontier, succ)
                elif succ in self.frontier:
                    # node = [node for node in self.frontier if node.state == succ.state][0]
                    idx = self.frontier.index(succ)
                    if succ.f < self.frontier[idx].f:
                        self.frontier[idx] = succ
                        heapq.heapify(self.frontier)
        return [], -1

    class Node(Node):
        # shortcut for accessing the evaluation value
        f = property(
            fget=lambda self: self.cost + self.h if self.cost and self.h else -1,
            fset=None
        )

        def __init__(self, state, action=None, parent=None, cost: int = 1, heuristic=None):
            super().__init__(state, action, parent, cost)
            self.h: int = heuristic(state) if isinstance(heuristic, Callable) else None

        def __lt__(self, other):
            return self.f < other.f

        def get_successors(self):
            result = [AStar.Node(node.state, node.action, node.parent, node.cost) for node in super().get_successors()]
            for node in result:
                node.h = AStar.heuristic_f(node.state)
            return result
