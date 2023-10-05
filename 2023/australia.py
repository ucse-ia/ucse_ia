from collections import defaultdict
from simpleai.search import (
    SearchProblem,
    hill_climbing,
    hill_climbing_random_restarts,
    hill_climbing_stochastic,
    simulated_annealing,
    beam,
)
from simpleai.search.viewers import BaseViewer, WebViewer
import random


NEIGHBORS = (
    ("WA", "NT"),
    ("WA", "SA"),
    ("NT", "SA"),
    ("NT", "Q"),
    ("SA", "Q"),
    ("SA", "NSW"),
    ("Q", "NSW"),
    ("SA", "V"),
    ("NSW", "V"),
)

ADJACENTS = defaultdict(list)
for province1, province2 in NEIGHBORS:
    ADJACENTS[province1].append(province2)
    ADJACENTS[province2].append(province1)

ADJACENTS["T"] = []


COLORS = "R", "G", "B"


class AustraliaProblem(SearchProblem):
    def actions(self, state):
        available_actions = []

        for province, color in state:
            for new_color in COLORS:
                if new_color != color:
                    available_actions.append((province, new_color))

        return available_actions

    def result(self, state, action):
        province, new_color = action
        current_assigned_colors = dict(state)
        current_assigned_colors[province] = new_color
        return tuple(current_assigned_colors.items())

    def value(self, state):
        conflicts = 0
        current_assigned_colors = dict(state)

        for province, color in state:
            neighbors = ADJACENTS[province]
            neighbor_colors = [
                current_assigned_colors[neighbor]
                for neighbor in neighbors
            ]
            conflicts += neighbor_colors.count(color)

        return -conflicts

    def generate_random_state(self):
        return tuple(
            (province, random.choice(COLORS))
            for province in ADJACENTS.keys()
        )




viewer = BaseViewer()
problem = AustraliaProblem(None)
result = hill_climbing_random_restarts(problem, restarts_limit=10, iterations_limit=1000, viewer=viewer)

print("Result:", result.state)
print("Value:", problem.value(result.state))
print("Stats:", viewer.stats)



