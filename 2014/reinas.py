import random
from simpleai.search import SearchProblem, hill_climbing, beam, hill_climbing_random_restarts
from simpleai.search.viewers import ConsoleViewer, WebViewer, BaseViewer


INICIAL = (0, 0, 0, 0, 0, 0, 0, 0)


class EightQueensProblem(SearchProblem):
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
        atacando = 0

        for columna1, fila1 in enumerate(state):
            for columna2, fila2 in enumerate(state):
                if columna2 > columna1:
                    if fila1 == fila2:
                        atacando += 1
                    else:
                        dif_col = abs(columna1 - columna2)
                        dif_fil = abs(fila1 - fila2)
                        if dif_col == dif_fil:
                            atacando += 1

        return -atacando

    def generate_random_state(self):
        return tuple([random.randint(0, 8)
                      for _ in range(8)])


result = hill_climbing_random_restarts(EightQueensProblem(), 1000)

print result.state
print EightQueensProblem().value(result.state)
