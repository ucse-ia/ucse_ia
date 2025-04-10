from itertools import combinations

from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    limited_depth_first,
    uniform_cost,
    iterative_limited_depth_first,
    greedy,
    astar,
)
from simpleai.search.viewers import BaseViewer, WebViewer


INICIAL = ("m", "m", "m", "c", "c", "c"), (), 0


class MisionerosProblem(SearchProblem):
    def cost(self, state, action, state2):
        return 1

    def is_goal(self, state):
        return len(state[1]) == 6

    def actions(self, state):
        canoa = state[2]
        origen = state[canoa]

        movimientos = []
        for persona in set(origen):
            movimientos.append((persona, ))

        for personas in set(combinations(origen, 2)):
            movimientos.append(personas)

        # cuales son posibles?
        movimientos_validos = []

        for personas_mover in movimientos:
            resultado_mover = self.result(state, personas_mover)
            nueva_izquierda, nueva_derecha, nueva_canoa = resultado_mover

            todas_las_orillas_bien = True
            for orilla in (nueva_izquierda, nueva_derecha):
                misioneros = orilla.count("m")
                canibales = orilla.count("c")

                if canibales > misioneros and misioneros > 0:
                    todas_las_orillas_bien = False
                    break

            if todas_las_orillas_bien:
                movimientos_validos.append(personas_mover)

        return movimientos_validos

    def result(self, state, action):
        izquierda, derecha, canoa = state

        if canoa == 0:
            origen = izquierda
            destino = derecha
        else:
            origen = derecha
            destino = izquierda

        origen = list(origen)
        destino = list(destino)

        # mover personas
        for persona in action:
            origen.remove(persona)
            destino.append(persona)

        origen = tuple(origen)
        destino = tuple(destino)

        if canoa == 0:
            canoa = 1
            izquierda = origen
            derecha = destino
        else:
            canoa = 0
            izquierda = destino
            derecha = origen

        return izquierda, derecha, canoa

    def heuristic(self, state):
        return len(state[0]) / 2


#result = breadth_first(MisionerosProblem(INICIAL))
result = astar(MisionerosProblem(INICIAL))

for action, state in result.path():
    print("action:", action)
    print("state:", state)

print("Depth:", len(list(result.path())))
