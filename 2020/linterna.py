from math import ceil
from itertools import combinations

from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    greedy,
    astar,
)
from simpleai.search.viewers import WebViewer, BaseViewer


# es una tupla de 4 posiciones:
# - la gente del lado izquierdo del puente (cada uno con su tiempo de caminata)
# - la gente del lado derecho del puente (cada uno con su tiempo de caminata)
# - tiempo restante de la linterna
# - lado del puente en el que está la linterna (0=izqueirda, 1=derecha)
INITIAL_STATE = (10, 30, 60, 80, 120), (), 300, 0


class LinternaProblem(SearchProblem):
    def is_goal(self, state):
        return len(state[1]) == 5

    def actions(self, state):
        personas_izq, personas_der, segundos_linterna, lado_linterna = state

        acciones = []
        for persona in state[lado_linterna]:
            if persona <= segundos_linterna:
                acciones.append((persona, ))
        for persona1, persona2 in combinations(state[lado_linterna], 2):
            if max(persona1, persona2) <= segundos_linterna:
                acciones.append((persona1, persona2))

        return acciones

    def result(self, state, action):
        personas_izq, personas_der, segundos_linterna, lado_linterna = state
        personas_izq = list(personas_izq)
        personas_der = list(personas_der)

        for persona in action:
            if lado_linterna == 0:
                personas_izq.remove(persona)
                personas_der.append(persona)
            else:
                personas_der.remove(persona)
                personas_izq.append(persona)

        if lado_linterna == 0:
            lado_linterna = 1
        else:
            lado_linterna = 0

        segundos_linterna -= max(action)

        return tuple(personas_izq), tuple(personas_der), segundos_linterna, lado_linterna

    def cost(self, state1, action, state2):
        return max(action)

    def heuristic(self, state):
        personas_izq, personas_der, segundos_linterna, lado_linterna = state

        if personas_izq:
            cantidad_viajes = ceil(len(personas_izq) / 2)
            persona_mas_veloz = min(personas_izq)
            return persona_mas_veloz * cantidad_viajes
        else:
            return 0


result = astar(LinternaProblem(INITIAL_STATE), graph_search=True)

print('Final state:', result.state)
for action, state in result.path():
    print('Action:', action)
    print('State:', state)
