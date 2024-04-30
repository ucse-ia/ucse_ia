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


BOARD_SIZE = 20
INITIAL = (0, ) * BOARD_SIZE


class QueensProblem(SearchProblem):
    def actions(self, state):
        available_actions = []
        for queen_number, current_row in enumerate(state):
            for destination_row in range(BOARD_SIZE):
                if destination_row != current_row:
                    available_actions.append((queen_number, destination_row))

        return available_actions

    def result(self, state, action):
        queen_number, destination_row = action
        state = list(state)

        state[queen_number] = destination_row

        return tuple(state)

    def value(self, state):
        attacks = 0
        for queen_number, current_row in enumerate(state):
            for other_queen_number, other_current_row in enumerate(state):
                if queen_number != other_queen_number:
                    if current_row == other_current_row:
                        attacks += 1
                    else:
                        delta_rows = abs(current_row - other_current_row)
                        delta_cols = abs(queen_number - other_queen_number)
                        if delta_cols == delta_rows:
                            attacks += 1

        return -attacks

    def generate_random_state(self):
        board = tuple(
            random.randint(0, BOARD_SIZE - 1)
            for _ in range(BOARD_SIZE)
        )
        return board


problem = QueensProblem(INITIAL)

#result = hill_climbing(problem)
result = hill_climbing_random_restarts(problem, restarts_limit=100)

print("Final state: (value:", problem.value(result.state), ")")
print(result.state)
