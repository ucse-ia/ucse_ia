from itertools import combinations

from simpleai.search import (
    SearchProblem,
    breadth_first,
    uniform_cost,
    depth_first,
    limited_depth_first,
    iterative_limited_depth_first,
    greedy,
    astar,
)
from simpleai.search.viewers import BaseViewer, WebViewer


INITIAL = ((), ("M", "M", "M", "C", "C", "C"), 1)


class MisionerosProblen(SearchProblem):
    def actions(self, state):
        available_actions = []

        return available_actions

    def result(self, state, action):
        ...

    def cost(self, state, action, state2):
        return 1

    def is_goal(self, state):
        ...

    def heuristic(self, state):
        ...



my_problem = MisionerosProblen(INITIAL)

result = astar(my_problem)

for action, state in result.path():
    print("A:", action)
    print("S:", state)
    print()
