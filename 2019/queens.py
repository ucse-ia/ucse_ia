import random

from simpleai.search import SearchProblem, hill_climbing, hill_climbing_random_restarts, simulated_annealing


N = 20


INITIAL = (0, ) * N


class QueensProblem(SearchProblem):
    def actions(self, state):
        available_actions = []
        for queen, current_row in enumerate(state):
            rows_can_move = [row for row in range(N)
                             if row != current_row]
            for row in rows_can_move:
                available_actions.append((queen, row))

        return available_actions

    def result(self, state, action):
        queen, row = action
        state = list(state)

        state[queen] = row

        return tuple(state)

    def value(self, state):
        attacks = 0

        for queen, current_row in enumerate(state):
            for queen2, current_row2 in enumerate(state):
                if queen < queen2:
                    # same row
                    if current_row == current_row2:
                        attacks += 1
                    else:
                        # diagonal
                        diff_col = abs(queen - queen2)
                        diff_row = abs(current_row - current_row2)
                        if diff_col == diff_row:
                            attacks += 1

        return -attacks

    def generate_random_state(self):
        state = []
        for queen in range(N):
            row = random.randint(0, N - 1)
            state.append(row)

        return tuple(state)


if __name__ == '__main__':
    problem = QueensProblem(INITIAL)
    result = hill_climbing_random_restarts(problem, restarts_limit=10)

    print(result.state)
    print('Attacks:', -problem.value(result.state))
