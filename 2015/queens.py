import random

from simpleai.search import (SearchProblem, hill_climbing, hill_climbing_stochastic,
                             hill_climbing_random_restarts, beam)
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer


INITIAL = (0, 0, 0, 0, 0, 0, 0, 0)


class QueensProblem(SearchProblem):
    def cost(self, state1, action, state2):
        return 1

    def actions(self, state):
        acciones = []
        for columna, fila in enumerate(state):
            if fila > 0:
                acciones.append((columna, fila - 1))
            if fila < 7:
                acciones.append((columna, fila + 1))

        return acciones

    def result(self, state, action):
        state = list(state)
        columna, fila = action
        state[columna] = fila

        return tuple(state)

    def value(self, state):
        ataques = 0
        for columna, fila in enumerate(state):
            for columna2, fila2 in enumerate(state):
                if columna < columna2:
                    if fila == fila2:
                        ataques += 1
                    elif abs(fila - fila2) == abs(columna - columna2):
                        ataques += 1

        return -ataques

    def generate_random_state(self):
        state = []
        for _ in range(8):
            state.append(random.randint(0, 7))

        return tuple(state)


result = hill_climbing(QueensProblem(INITIAL))
print 'Hill climbing:'
print result.state
print QueensProblem().value(result.state)

result = hill_climbing_stochastic(QueensProblem(INITIAL))
print 'Hill climbing stochastic:'
print result.state
print QueensProblem().value(result.state)

result = beam(QueensProblem(), beam_size=10)
print 'Beam:'
print result.state
print QueensProblem().value(result.state)

result = hill_climbing_random_restarts(QueensProblem(), restarts_limit=100)
print 'Hill climbing random restarts:'
print result.state
print QueensProblem().value(result.state)
