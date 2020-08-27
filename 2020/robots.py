from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    iterative_limited_depth_first,
    uniform_cost,
)

from simpleai.search.viewers import WebViewer, BaseViewer


INITIAL_STATE = ((0, 1), (0, 1))
OBSTACULOS = (
    (0, 2),
    (1, 3),
    (2, 1),
)
PUERTAS = (
    (0, 4),
    (3, 2),
)

class RobotsProblem(SearchProblem):
    def cost(self, state1, action, state2):
        return 1

    def is_goal(self, state):
        # sin importar el orden, tiene que ser la misma bolsa
        # de posiciones en los dos lados
        return set(PUERTAS) == set(state)

    def actions(self, state):
        acciones_posibles = []

        for indice_robot, robot in enumerate(state):
            movimientos = (
                (-1, 0),  # arriba
                (1, 0),  # abajo
                (0, -1),  # izquierda
                (0, 1),  # derecha
            )

            for movimiento in movimientos:
                fila_robot, columna_robot = robot
                cambio_fila, cambio_columna = movimiento
                nueva_posicion = (
                    fila_robot + cambio_fila,
                    columna_robot + cambio_columna,
                )

                puedo = (
                    (nueva_posicion not in OBSTACULOS)
                    and (0 <= nueva_posicion[0] <= 3)
                    and (0 <= nueva_posicion[1] <= 4)
                )

                if puedo:
                    acciones_posibles.append(
                        (indice_robot, nueva_posicion)
                    )

        return acciones_posibles

    def result(self, state, action):
        indice_robot, nueva_posicion = action

        state = list(state)
        state[indice_robot] = nueva_posicion

        return tuple(state)


metodos = (
    breadth_first,
    depth_first,
    iterative_limited_depth_first,
    uniform_cost,
)

for metodo_busqueda in metodos:
    print()
    print('=' * 50)

    print("corriendo:", metodo_busqueda)
    visor = BaseViewer()
    problem = RobotsProblem(INITIAL_STATE)
    result = metodo_busqueda(problem, graph_search=False, viewer=visor)

    # print('estado final:')
    # print(result.state)

    # print('-' * 50)

    for action, state in result.path():
        print('accion:', action)
        print('estado resultante:', state)

    print('estadísticas:')
    print('cantidad de acciones hasta la meta:', len(result.path()))
    print(visor.stats)
