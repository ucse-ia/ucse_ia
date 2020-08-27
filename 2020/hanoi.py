from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    iterative_limited_depth_first,
    uniform_cost,
)

from simpleai.search.viewers import WebViewer, BaseViewer


INITIAL_STATE = ((4, 3, 2, 1), (), (), ())
GOAL_STATE = ((), (), (), (4, 3, 2, 1))


class HanoiProblem(SearchProblem):
    """
    Variante de las torres de hanoi, con las siguientes reglas:
    - solo se puede mover a palitos adyacentes
    - no hay restricción de mover una pieza grande dejándola arriba de otra más chica
    """
    def cost(self, state1, action, state2):
        return 1

    def is_goal(self, state):
        return state == GOAL_STATE

    def actions(self, state):
        acciones_posibles = []

        for indice_palito, cosas_palito in enumerate(state):
            if indice_palito > 0 and cosas_palito:
                # no es el primer palito, puedo mover a la izquierda
                acciones_posibles.append((indice_palito, -1))

            if indice_palito < 3 and cosas_palito:
                # no es el último palito, puedo mover a la derecha
                acciones_posibles.append((indice_palito, 1))

        return acciones_posibles

    def result(self, state, action):
        indice_palito, direccion = action
        state = list(list(palito) for palito in state)

        palito_origen = state[indice_palito]
        palito_destino = state[indice_palito + direccion]

        pieza = palito_origen.pop()
        palito_destino.append(pieza)

        return tuple(tuple(palito) for palito in state)


metodos = (
    # breadth_first,
    # depth_first,
    uniform_cost,
)

for metodo_busqueda in metodos:
    print()
    print('=' * 50)

    print("corriendo:", metodo_busqueda)
    visor = BaseViewer()
    problem = HanoiProblem(INITIAL_STATE)
    result = metodo_busqueda(problem, graph_search=True, viewer=visor)

    # print('estado final:')
    # print(result.state)

    # print('-' * 50)

    for action, state in result.path():
        print('accion:', action)
        print('estado resultante:', state)

    print('estadísticas:')
    print('cantidad de acciones hasta la meta:', len(result.path()))
    print(visor.stats)
