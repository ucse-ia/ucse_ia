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


INITIAL = "ABCDE", "", 0, 300

TIEMPOS = {
    "A": 10,
    "B": 30,
    "C": 60,
    "D": 80,
    "E": 120,
}


class PuenteProblem(SearchProblem):
    def actions(self, state):
        gente_izquierda, gente_derecha, lado_linterna, bateria_restante = state

        available_actions = []
        gente_con_linterna = state[lado_linterna]

        for persona in gente_con_linterna:
            if TIEMPOS[persona] <= bateria_restante:
                available_actions.append((persona, ))

        for persona1, persona2 in combinations(gente_con_linterna, 2):
            if max(TIEMPOS[persona1], TIEMPOS[persona2]) <= bateria_restante:
                available_actions.append((persona1, persona2))

        return available_actions

    def result(self, state, action):
        gente_izquierda, gente_derecha, lado_linterna, bateria_restante = state
        gente_a_cruzar = action

        gente_origen = state[lado_linterna]
        gente_destino = state[int(not lado_linterna)]  # los bools son ints!! :D

        for persona_que_cruza in gente_a_cruzar:
            gente_origen = gente_origen.replace(persona_que_cruza, "")
            gente_destino += persona_que_cruza

        bateria_restante -= max(TIEMPOS[p] for p in gente_a_cruzar)

        if lado_linterna == 0:
            return gente_origen, gente_destino, 1, bateria_restante
        else:
            return gente_destino, gente_origen, 0, bateria_restante

    def cost(self, state, action, state2):
        gente_a_cruzar = action
        return max(TIEMPOS[p] for p in gente_a_cruzar)

    def is_goal(self, state):
        gente_izquierda, gente_derecha, lado_linterna, bateria_restante = state
        return gente_izquierda == ""

    def heuristic(self, state):
        gente_izquierda, gente_derecha, lado_linterna, bateria_restante = state
        if gente_izquierda:
            return max(TIEMPOS[p] for p in gente_izquierda)
        else:
            return 0


v = BaseViewer()
my_problem = PuenteProblem(INITIAL)
result = astar(my_problem)

if result is None:
    print("No solution")
else:
    for action, state in result.path():
        print("A:", action)
        print("S:", state)

    print("Final depth:", len(result.path()))
    print("Final cost:", result.cost)

print("Stats:")
print(v.stats)
