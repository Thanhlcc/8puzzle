from graphviz import Digraph

from tests import Testcases
from node import Node




if __name__ == "__main__":
    test_manager = Testcases(20)
    test_manager.test_astar()
