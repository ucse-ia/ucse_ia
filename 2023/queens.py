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


INITIAL = (0, 0, 0, 0, 0, 0, 0, 0)


class QueensProblem(SearchProblem):
    def actions(self, state):
        available_actions = []
        for queen, queen_row in enumerate(state):
            for other_row in range(8):
                if other_row != queen_row:
                    available_actions.append((queen, other_row))

        return available_actions

    def result(self, state, action):
        queen, new_row = action
        state = list(state)
        state[queen] = new_row
        return tuple(state)

    def value(self, state):
        attacks = 0
        for queen, queen_row in enumerate(state):
            how_many_in_this_row = state.count(queen_row)
            attacks += how_many_in_this_row - 1

            for other_queen, other_queen_row in enumerate(state):
                if queen != other_queen:
                    diff_rows = abs(queen_row - other_queen_row)
                    diff_cols = abs(queen - other_queen)
                    if diff_rows == diff_cols:
                        attacks += 1

        return -attacks

    def generate_random_state(self):
        return tuple(
            random.randint(0, 7)
            for _ in range(8)
        )



viewer = BaseViewer()
problem = QueensProblem(INITIAL)
#result = hill_climbing(problem, iterations_limit=1000, viewer=viewer)
#result = beam(problem, beam_size=10, iterations_limit=1000, viewer=viewer)
result = hill_climbing_random_restarts(problem, restarts_limit=10, iterations_limit=1000, viewer=viewer)

print("Result:", result.state)
print("Value:", problem.value(result.state))
print("Stats:", viewer.stats)


