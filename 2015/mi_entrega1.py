from simpleai import search
from simpleai.search import (SearchProblem, breadth_first, depth_first,
                             iterative_limited_depth_first, greedy,
                             astar, limited_depth_first)
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer


INITIAL = (
    (4, 0),
    (2, 2),
    (0, 4),
)


def manhattan(punto_a, punto_b):
    x_a, y_a = punto_a
    x_b, y_b = punto_b

    return abs(x_a - x_b) + abs(y_a - y_b)


class DotaProblem(SearchProblem):
    def cost(self, state1, action, state2):
        return 1

    def is_goal(self, state):
        heroe, enemigo, base = state
        return enemigo is None and base is None

    def actions(self, state):
        heroe, enemigo, base = state
        x_heroe, y_heroe = heroe

        adyacentes = (
            (x_heroe + 1, y_heroe),
            (x_heroe - 1, y_heroe),
            (x_heroe, y_heroe + 1),
            (x_heroe, y_heroe - 1),
        )

        acciones = []
        for adyacente in adyacentes:
            x_adyacente, y_adyacente = adyacente
            if 0 <= x_adyacente <= 4 and 0 <= y_adyacente <= 4:
                acciones.append(adyacente)

        return acciones

    def result(self, state, action):
        heroe, enemigo, base = state
        if action == enemigo:
            enemigo = None
        elif action == base:
            base = None
        else:
            heroe = action

        return heroe, enemigo, base

    def heuristic(self, state):
        heroe, enemigo, base = state

        if enemigo is None and base is None:
            return 0
        elif enemigo is not None and base is not None:
            distancia_enemigo = manhattan(heroe, enemigo)
            distancia_base = manhattan(heroe, base)

            if distancia_enemigo < distancia_base:
                return distancia_enemigo + manhattan(enemigo, base)
            else:
                return distancia_base + manhattan(base, enemigo)
        else:
            if enemigo is not None:
                vivo = enemigo
            else:
                vivo = base

            return manhattan(heroe, vivo)


def resolver(metodo_busqueda):
    metodo = getattr(search, metodo_busqueda)
    if metodo_busqueda == 'limited_depth_first':
        result = metodo(DotaProblem(INITIAL), limit=10, graph_search=True)
    else:
        result = metodo(DotaProblem(INITIAL), graph_search=True)

    return result
