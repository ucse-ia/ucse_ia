from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    iterative_limited_depth_first,
    uniform_cost,
)

from simpleai.search.viewers import WebViewer, BaseViewer


# 3 canibales a la izquierda
# 3 misioneros a la izquierda
# 0 canibales a la izquierda
# 0 misioneros a la izquierda
# bote a la izquierda (0=izquierda, 1=derecha)
INITIAL_STATE = ((3, 3), (0, 0), 0)

GOAL_STATE = ((0, 0), (3, 3), 1)


class MisionerosProblem(SearchProblem):
    def cost(self, state1, action, state2):
        return 1

    def is_goal(self, state):
        return state == GOAL_STATE

    def actions(self, state):
        gente_izquierda, gente_derecha, posicion_bote = state

        gente_origen = state[posicion_bote]
        misioneros_origen, canibales_origen = gente_origen

        acciones_posibles = []

        # las acciones son tuplas con dos números:
        # (cantidad de misioneros a mover, cantidad de caníbales a mover)
        for misioneros_mover in (0, 1, 2):
            for canibales_mover in (0, 1, 2):
                if misioneros_mover + canibales_mover in (1, 2):
                    # estoy moviendo 1 o 2 personas
                    if misioneros_mover <= misioneros_origen and canibales_mover <= canibales_origen:
                        # hay suficiente gente para mover

                        accion = (misioneros_mover, canibales_mover)
                        estado_resultante = self.result(state, accion)

                        # se van a comer a los misioneros?
                        orillas_bien = True
                        for orilla in (estado_resultante[0], estado_resultante[1]):
                            misioneros_resultantes, canibales_resultantes = orilla
                            if misioneros_resultantes > 0 and misioneros_resultantes < canibales_resultantes:
                                # está todo bien en esta orilla
                                orillas_bien = False

                        if orillas_bien:
                            acciones_posibles.append(accion)

        return acciones_posibles

    def result(self, state, action):
        gente_izquierda, gente_derecha, posicion_bote = state
        misioneros_mover, canibales_mover = action

        nuevo_origen = list(state[posicion_bote])
        if posicion_bote == 0:
            nuevo_bote = 1
        else:
            nuevo_bote = 0
        nuevo_destino = list(state[nuevo_bote])

        nuevo_origen[0] -= misioneros_mover
        nuevo_destino[0] += misioneros_mover

        nuevo_origen[1] -= canibales_mover
        nuevo_destino[1] += canibales_mover

        nuevo_origen = tuple(nuevo_origen)
        nuevo_destino = tuple(nuevo_destino)

        if nuevo_bote == 0:
            return (nuevo_destino, nuevo_origen, nuevo_bote)
        else:
            return (nuevo_origen, nuevo_destino, nuevo_bote)


metodos = (
    breadth_first,
    depth_first,
    uniform_cost,
)

for metodo_busqueda in metodos:
    print()
    print('=' * 50)

    print("corriendo:", metodo_busqueda)
    visor = BaseViewer()
    problem = MisionerosProblem(INITIAL_STATE)
    result = metodo_busqueda(problem, graph_search=True, viewer=visor)

    print('estado final:')
    print(result.state)

    print('-' * 50)

    for action, state in result.path():
        print('accion:', action)
        print('estado resultante:', state)

    print('estadísticas:')
    print('cantidad de acciones hasta la meta:', len(result.path()))
    print(visor.stats)
