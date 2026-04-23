from random import randint
from itertools import combinations

from simpleai.search.models import SearchProblem

from simpleai.search.local import (hill_climbing,
                                   hill_climbing_random_restarts,
                                   hill_climbing_stochastic,
                                   beam)


N_QUEENS = 30


class QueensProblem(SearchProblem):
    def actions(self, state):
        available_actions = []
        possible_rows = list(range(N_QUEENS))

        for queen_col, queen_row in enumerate(state):
            for new_queen_row in possible_rows:
                if new_queen_row != queen_row:
                    available_actions.append((queen_col, new_queen_row))

        return available_actions

    def result(self, state, action):
        queen_col, new_queen_row = action
        state = list(state)
        state[queen_col] = new_queen_row

        return tuple(state)

    def value(self, state):
        queens = list(range(N_QUEENS))
        attacking_pairs = 0

        # por cada par posible de reinas, ver si se atacan
        for queen_col1, queen_col2 in combinations(queens, 2):
            queen_row1 = state[queen_col1]
            queen_row2 = state[queen_col2]

            if queen_row1 == queen_row2:
                # misma fila?
                attacking_pairs += 1
            elif abs(queen_col1 - queen_col2) == abs(queen_row1 - queen_row2):
                # están en diagonal
                attacking_pairs += 1

        return -attacking_pairs

    def generate_random_state(self):
        state = [
            randint(0, N_QUEENS - 1)
            for _ in range(N_QUEENS)
        ]

        return tuple(state)


if __name__ == "__main__":
    p = QueensProblem((0, ) * N_QUEENS)

    # result = hill_climbing(p)
    result = hill_climbing_random_restarts(p, restarts_limit=50)

    print("Board:")
    print(result.state)
    print("Attacks:")
    print(p.value(result.state))
