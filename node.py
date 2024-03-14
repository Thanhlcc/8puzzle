from copy import deepcopy
from functools import reduce
from typing import Any


class Node:
    def __init__(self, state, action=None, parent=None, cost: int = 1):
        self.state = state  # 2D list (3x3)
        self.cost = cost
        self.action = action
        self.parent = parent
        self.id = str(self)

    def __str__(self):
        def refine_one_row(row):
            return ''.join([str(ele) if ele != 0 else '_' for ele in row])

        return '\n'.join(list(map(lambda x: refine_one_row(x), self.state)))

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(self.id)

    def get_successors(self):
        pi, pj = self.get_blank_pos(self.state)
        actions = []
        if 0 <= pj < 2: actions.append('L')
        if 0 < pj < 3: actions.append('R')
        if 0 <= pi < 2: actions.append('U')
        if 0 < pi < 3: actions.append('D')
        return [Node(
            state=self.get_successor(action, deepcopy(self.state)),
            action=action,
            parent=self,
            cost=self.cost + 1
        ) for action in actions]

    def get_successor(self, action, state):
        pi, pj = self.get_blank_pos(state)
        pi, pj = self.get_dest_pos(action, pi, pj)
        if 0 <= pi < 3 and 0 <= pj < 3:
            if action == 'L':
                state[pi][pj - 1] = state[pi][pj]
            if action == 'R':
                state[pi][pj + 1] = state[pi][pj]
            if action == 'U':
                state[pi - 1][pj] = state[pi][pj]
            if action == 'D':
                state[pi + 1][pj] = state[pi][pj]
            state[pi][pj] = 0
            return state
        return None

    def get_dest_pos(self, action, pi, pj):
        if action == 'L':
            pj += 1
        if action == 'R':
            pj -= 1
        if action == 'U':
            pi += 1
        if action == 'D':
            pi -= 1
        return pi, pj

    def get_blank_pos(self, state):
        return [(i, j) for i, val_i in enumerate(self.state) for j, val_j in enumerate(val_i) if val_j == 0][0]

    @staticmethod
    def index(matrix_2, cell) -> dict[str, int | Any] | dict[Any, Any]:
        """
        @Return the coordination of the ele in the given 2d-matrix
        If the element is not included, empty dictionary returned
        """
        try:
            flattened = reduce(lambda acc, ele: acc + ele, matrix_2)
            idx = flattened.index(cell)
            return {
                'x': idx % 3,
                'y': (idx - idx % 3) // 3
            }
        except ValueError:
            return {}

    def get_id(self):
        return self.id

    def get_action(self):
        return self.action

    def draw(self, dot):
        dot.node(self.get_id(), str(self))
        if self.parent:
            dot.edge(self.parent.id, self.id, self.action)