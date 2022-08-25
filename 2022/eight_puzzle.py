from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    limited_depth_first,
    iterative_limited_depth_first,
)
from simpleai.search.viewers import WebViewer, BaseViewer


GOAL = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0),
)


def buscar(state, pieza):
    for i_fila, fila in enumerate(state):
        for i_col, pieza_actual in enumerate(fila):
            if pieza_actual == pieza:
                return i_fila, i_col


class EightPuzzleProblem(SearchProblem):
    def cost(self, state1, action, state2):
        return 1

    def is_goal(self, state):
        return state == GOAL

    def actions(self, state):
        acciones_disponibles = []

        fila_cero, col_cero = buscar(state, 0)

        if fila_cero < 2:
            acciones_disponibles.append(state[fila_cero + 1][col_cero])
        if fila_cero > 0:
            acciones_disponibles.append(state[fila_cero - 1][col_cero])
        if col_cero < 2:
            acciones_disponibles.append(state[fila_cero][col_cero + 1])
        if col_cero > 0:
            acciones_disponibles.append(state[fila_cero][col_cero - 1])

        return acciones_disponibles

    def result(self, state, action):
        state_modificable = [list(fila) for fila in state]

        fila_cero, col_cero = buscar(state, 0)
        fila_pieza, col_pieza = buscar(state, action)

        state_modificable[fila_cero][col_cero] = action
        state_modificable[fila_pieza][col_pieza] = 0

        return tuple(tuple(fila) for fila in state_modificable)


INICIAL = (
    (1, 0, 3),
    (4, 2, 6),
    (7, 5, 8),
)

viewer = WebViewer()
#viewer = BaseViewer()
# result = breadth_first(EightPuzzleProblem(INICIAL),
                       # graph_search=True)
result = breadth_first(EightPuzzleProblem(INICIAL),
                       viewer=viewer)
# result = depth_first(EightPuzzleProblem(INICIAL), graph_search=True)
# result = uniform_cost(EightPuzzleProblem(INICIAL))
# result = limited_depth_first(EightPuzzleProblem(INICIAL), 5)
# result = iterative_limited_depth_first(EightPuzzleProblem(INICIAL))

print("Estado meta:")
print(result.state)

for action, state in result.path():
    print("Haciendo", action, "llegué a:")
    print(state)

print("Stats:")
print(viewer.stats)
