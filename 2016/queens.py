import random
from simpleai.search import (SearchProblem, hill_climbing,
                             hill_climbing_random_restarts,
                             beam)
from simpleai.search.viewers import WebViewer


INICIAL = (0, ) * 8


class QueensProblem(SearchProblem):
    def actions(self, state):
        acciones = []
        for reina in range(8):
            for fila in range(8):
                if state[reina] != fila:
                    acciones.append((reina, fila))
        return acciones

    def result(self, state, action):
        state = list(state)
        reina, fila = action
        state[reina] = fila

        return tuple(state)

    def value(self, state):
        ataques = 0

        for reina in range(8):
            for reina2 in range(8):
                if reina != reina2:
                    misma_fila = state[reina] == state[reina2]
                    en_diagonal = abs(reina - reina2) == abs(state[reina] - state[reina2])
                    if misma_fila or en_diagonal:
                        ataques += 1

        ataques = ataques / 2

        return -ataques

    def generate_random_state(self):
        estado = []
        for reina in range(8):
            estado.append(random.randint(0, 7))

        return tuple(estado)


if __name__ == '__main__':
    result = globals()[metodo_busqueda](Problema...)
    result = hill_climbing_random_restarts(QueensProblem(None), restarts_limit=100)

    for fila in range(8):
        for columna in range(8):
            if result.state[columna] == fila:
                print '|*',
            else:
                print '| ',
        print
        print '-' * 40

    print result.value




















