from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    limited_depth_first,
    iterative_limited_depth_first,
    astar,
    greedy,
)
from simpleai.search.viewers import WebViewer, BaseViewer


# (cantidad misioneros, cantidad canibales, orilla canoa)
INICIAL = (3, 3, 0)
GOAL = (0, 0, 1)
# cada accion es una tupla: (misioneros que viajan, canibales que viajan)
ACCIONES = (
    (2, 0),
    (0, 2),
    (1, 1),
    (1, 0),
    (0, 1),
)


class MisionerosProblem(SearchProblem):
    def cost(self, state1, action, state2):
        return 1

    def is_goal(self, state):
        return state == GOAL

    def actions(self, state):
        acciones_disponibles = []

        for accion in ACCIONES:
            mis_izq_result, can_izq_result, _ = self.result(state, accion)

            izq = (mis_izq_result, can_izq_result)
            der = (3 - mis_izq_result, 3 - can_izq_result)

            todo_bien = True
            for mis, can in (izq, der):
                todos_vivos = mis == 0 or can <= mis
                gente_suficiente = mis >= 0 and can >= 0

                if not (todos_vivos and gente_suficiente):
                    todo_bien = False
                    break

            if todo_bien:
                acciones_disponibles.append(accion)

        return acciones_disponibles

    def result(self, state, action):
        mis_izq, can_izq, orilla = state
        mis_mover, can_mover = action

        if orilla == 0:
            orilla = 1

            mis_izq = mis_izq - mis_mover
            can_izq = can_izq - can_mover
        else:
            orilla = 0

            mis_izq = mis_izq + mis_mover
            can_izq = can_izq + can_mover

        return mis_izq, can_izq, orilla

    def heuristic(self, state):
        mis_izq, can_izq, _ = state
        return mis_izq + can_izq - 1


if __name__ == "__main__":
    viewer = BaseViewer()
    #result = depth_first(MisionerosProblem(INICIAL), graph_search=True, viewer=viewer)
    #result = breadth_first(MisionerosProblem(INICIAL), graph_search=True, viewer=viewer)
    result = astar(MisionerosProblem(INICIAL), viewer=viewer)

    for action, state in result.path():
        print("Haciendo", action, "llegué a:")
        print(state)

    print("Profundidad:", len(list(result.path())))
    print("Stats:")
    print(viewer.stats)

