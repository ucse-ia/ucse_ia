from simpleai.search import SearchProblem, astar


arboles = ((0, 0), (0, 3), (1, 3), (2, 1), (3, 0))

# mi estado: lista de posiciones de carpas YA puestas (vacia al inicio)

def tiene_vecinos(posicion, posibles_vecinos):
    # recibe una posicion, y una lista de otras posiciones. Devuelve true si
    # alguna de las otras posiciones es vecina a la posicion pasada
    x1, y1 = posicion

    for posible in posibles_vecinos:
        x2, y2 = posible
        if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
            return True

    return False


class ProblemaCarpas(SearchProblem):
    def actions(self, state):
        # devuelvo la lista de posiciones en donde puedo poner la proxima carpa
        return [(x, y)
                for x in range(4)
                for y in range(4)
                if (x, y) not in state and  # asi no pone la carpa donde haya otra
                   (x, y) not in arboles and  # asi no pone la carpa donde haya un arbol
                   tiene_vecinos((x, y), arboles) and  # asi obliga a que la carpa se ponga vecina a algun arbol
                   not tiene_vecinos((x, y), state)]  # asi obliga a que la carpa NO este vecina a las carpas ya puestas

    def result(self, state, action):
        # agrego la carpa a la lista de carpas ya puestas
        return state + (action,)

    def cost(self, state1, action, state2):
        # poner una carpa siempre cuesta lo mismo
        return 1

    def is_goal(self, state):
        # si puse 4 carpas, ya termine
        return len(state) == 4

    def heuristic(self, state):
        # me faltan tantas acciones como carpas me falte ubicar para llegar a 4
        return 4 - len(state)


result = astar(ProblemaCarpas(tuple()), graph_search=True)

print result.state
