from simpleai.search import breadth_first, SearchProblem, astar, greedy
from simpleai.search.viewers import WebViewer


INICIAL = (
    (2, 0, 5),
    (3, 7, 8),
    (4, 1, 6),
)

META = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
)


def donde_esta(state, numero):
    for indice_fila, fila in enumerate(state):
        for indice_columna, numero_actual in enumerate(fila):
            if numero_actual == numero:
                return indice_fila, indice_columna


def t2l(t):
    return list(list(r) for r in t)


def l2t(l):
    return tuple(tuple(r) for r in l)


class PuzzleProblem(SearchProblem):
    def cost(self, state1, action, state2):
        return 1

    def is_goal(self, state):
        return state == META

    def actions(self, state):
        acciones = []
        fila_cero, col_cero = donde_esta(state, 0)
        if fila_cero > 0:
            acciones.append(state[fila_cero - 1][col_cero])
        if fila_cero < 2:
            acciones.append(state[fila_cero + 1][col_cero])
        if col_cero > 0:
            acciones.append(state[fila_cero][col_cero - 1])
        if col_cero < 2:
            acciones.append(state[fila_cero][col_cero + 1])

        return acciones

    def result(self, state, action):
        fila_cero, col_cero = donde_esta(state, 0)
        fila_otro, col_otro = donde_esta(state, action)

        state = t2l(state)
        state[fila_cero][col_cero] = action
        state[fila_otro][col_otro] = 0
        state = l2t(state)

        return state

    def heuristic(self, state):
        total = 0
        for pieza in range(8):
            pieza += 1
            fila_pieza, col_pieza = donde_esta(state, pieza)
            fila_meta, col_meta = donde_esta(META, pieza)
            distancia = abs(col_pieza - col_meta) + abs(fila_pieza - fila_meta)
            total += distancia

        return total


if __name__ == '__main__':
    problema = PuzzleProblem(INICIAL)

    # resultado = astar(problema, viewer=WebViewer())
    resultado = astar(problema, graph_search=True)

    print 'Estado meta:'
    print resultado.state
    print 'Camino:'
    print len(resultado.path())
    for accion, estado in resultado.path():
        print 'Movi', accion
        print 'Llegue a', estado









