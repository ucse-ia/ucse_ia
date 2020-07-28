# -*- coding: utf-8 -*-
from simpleai.search import SearchProblem, uniform_cost
from simpleai.search.viewers import WebViewer


def cross(side):
    return 'I' if side == 'D' else 'D'


class BridgeProblem(SearchProblem):

    def is_goal(self, state):
        return state == ('D', 'D', 'D', 'D')

    def cost(self, state1, action, state2):
        if action[2]:
            return 10
        elif action[1]:
            return 5
        return 2

    def actions(self, state):
        movements = [
            (True, False, False, True),
            (True, True, False, True),
            (True, False, True, True),
            (False, True, False, True),
            (False, True, True, True),
            (False, False, True, True),
        ]

        current = [x == state[3] for x in state[:3]] + [True]
        actions = []

        for mov in movements:
            if not any([m and not c for m, c in zip(mov, current)]):
                actions.append(mov)
        return actions

    def result(self, state, action):
        return tuple([cross(x) if a else x for x, a in zip(state, action)])


result = uniform_cost(BridgeProblem(('I', 'I', 'I', 'I')), viewer=WebViewer(), graph_search=True)
