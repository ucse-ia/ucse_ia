from itertools import combinations

from simpleai.search import (
    SearchProblem,
    breadth_first,
    uniform_cost,
    depth_first,
    limited_depth_first,
    iterative_limited_depth_first,
    greedy,
    astar,
)
from simpleai.search.viewers import BaseViewer, WebViewer


INITIAL = ((), ("M", "M", "M", "C", "C", "C"), 1)


def orilla_ok(gente):
    cantidad_misioneros = gente.count("M")
    cantidad_canibales = gente.count("C")

    return (cantidad_misioneros >= cantidad_canibales) or not cantidad_misioneros


class MisionerosProblen(SearchProblem):
    def actions(self, state):
        izq, der, canoa = state
        available_actions = []

        origen = state[canoa]

        posibilidades_tripulantes = []
        posibilidades_tripulantes.extend([(p, ) for p in origen])
        posibilidades_tripulantes.extend(combinations(origen, 2))
        posibilidades_tripulantes = set(posibilidades_tripulantes)

        for tripulantes in posibilidades_tripulantes:
            estado_resultante = self.result(state, tripulantes)
            if orilla_ok(estado_resultante[0]) and orilla_ok(estado_resultante[1]):
                available_actions.append(tripulantes)

        return available_actions

    def result(self, state, action):
        izq, der, canoa = state

        origen = list(state[canoa])
        destino = list(state[1 - canoa])

        for persona in action:
            origen.remove(persona)
            destino.append(persona)

        canoa = 1 - canoa

        origen = tuple(origen)
        destino = tuple(destino)

        if canoa == 0:
            return destino, origen, canoa
        else:
            return origen, destino, canoa


    def cost(self, state, action, state2):
        return 1

    def is_goal(self, state):
        izq, der, canoa = state
        return not der

    def heuristic(self, state):
        izq, der, canoa = state
        return len(der) - 1



my_problem = MisionerosProblen(INITIAL)

result = astar(my_problem)

for action, state in result.path():
    print("A:", action)
    print("S:", state)
    print()
