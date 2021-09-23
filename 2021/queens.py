from random import randint

from simpleai.search import SearchProblem
from simpleai.search.viewers import WebViewer
from simpleai.search.local import (
    hill_climbing,
    hill_climbing_random_restarts,
    hill_climbing_stochastic,
    simulated_annealing,
)


# estructura estado:
# tupla donde la posición es la colmna de la reina, y el valor es la fila de esa reina
# (0, 0, 0, 1, 2, 0, 6, 7)

# estructura de acción:
# tupla donde el primer elemento es la reina a mover, y el segundo elemento es -1 o 1, para
# decir si la movemos para arriba o para abajo
# ej: mover la 4ta reina para arriba
#     (3, -1)


class QueensProblem(SearchProblem):
    def actions(self, state):
        available_actions = []

        for queen in range(8):
            queen_row = state[queen]

            if queen_row > 0:
                available_actions.append((queen, -1))

            if queen_row < 7:
                available_actions.append((queen, 1))

        return available_actions

    def result(self, state, action):
        state = list(state)
        queen, movement = action

        state[queen] += movement

        return tuple(state)

    def value(self, state):
        attacks = 0

        for queen in range(8):
            for queen2 in range(8):
                if queen != queen2:
                    queen_row = state[queen]
                    queen2_row = state[queen2]

                    if queen_row == queen2_row:
                        attacks += 1
                    else:
                        cols_diff = abs(queen - queen2)
                        rows_diff = abs(queen_row - queen2_row)

                        if cols_diff == rows_diff:
                            attacks += 1

        return -attacks

    def generate_random_state(self):
        state = []
        for queen in range(8):
            queen_row = randint(0, 7)
            state.append(queen_row)

        return tuple(state)



print("Hill climbing:")
fixed_initial_state = (0, 0, 0, 0, 0, 0, 0, 0)
problem = QueensProblem(fixed_initial_state)
result = hill_climbing(problem, iterations_limit=9999, viewer=WebViewer())
print(result.state, problem.value(result.state))


print("Hill climbing random restarts:")
problem = QueensProblem(None)
result = hill_climbing_random_restarts(problem, restarts_limit=999, iterations_limit=9999)
print(result.state, problem.value(result.state))








