import random

from simpleai.search import SearchProblem, hill_climbing, hill_climbing_random_restarts, beam, simulated_annealing

N = 20


INITIAL = tuple([0, ] * N)

class QueensProblem(SearchProblem):
    def actions(self, state):
        available_actions = []
        for queen in range(N):
            for new_row in range(N):
                if new_row != state[queen]:
                    available_actions.append((queen, new_row))

        return available_actions

    def result(self, state, action):
        state = list(state)
        queen, new_row = action
        state[queen] = new_row
        return tuple(state)

    def value(self, state):
        attacks = 0

        for queen_col, queen_row in enumerate(state):
            for queen2_col, queen2_row in enumerate(state):
                if queen_col != queen2_col:
                    same_row = queen_row == queen2_row
                    diagonal = abs(queen_row - queen2_row) == abs(queen_col - queen2_col)
                    if same_row or diagonal:
                        attacks += 1

        return -attacks

    def generate_random_state(self):
        state = list(range(N))
        random.shuffle(state)
        return tuple(state)


# problem = QueensProblem(INITIAL)
# result = hill_climbing(problem)

problem = QueensProblem(None)
result = hill_climbing_random_restarts(problem, restarts_limit=50)

print(result.state)
print('value:', problem.value(result.state))

