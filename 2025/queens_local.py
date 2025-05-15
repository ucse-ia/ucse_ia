from random import randint

from simpleai.search.models import SearchProblem

from simpleai.search.local import (hill_climbing,
                                   hill_climbing_random_restarts,
                                   hill_climbing_stochastic,
                                   beam,
                                   simulated_annealing)

N_QUEENS = 1000


class QueensProblem(SearchProblem):
    def actions(self, state):
        available_actions = []
        for queen in range(N_QUEENS):
            current_row = state[queen]
            possible_rows = list(range(N_QUEENS))
            possible_rows.remove(current_row)

            for new_row in possible_rows:
                action = (queen, new_row)
                available_actions.append(action)

        return available_actions

    def result(self, state, action):
        queen, new_row = action
        state = list(state)
        state[queen] = new_row
        return tuple(state)

    def value(self, state):
        attacks = 0
        for col_1, row_1 in enumerate(state):
            for col_2, row_2 in enumerate(state):
                if col_1 < col_2:
                    # se atacan horizontalmente?
                    if row_1 == row_2:
                        attacks += 1
                    # se atacan diagonal?
                    if abs(row_1 - row_2) == abs(col_1 - col_2):
                        attacks += 1
        return -attacks

    def generate_random_state(self):
        state = tuple([
            randint(0, N_QUEENS - 1)
            for _ in range(N_QUEENS)
        ])

        return state


problem = QueensProblem(None)

result = hill_climbing_random_restarts(
    problem, restarts_limit=1, iterations_limit=99999,
)

print(result.state)
print("Attacks:", -problem.value(result.state))
