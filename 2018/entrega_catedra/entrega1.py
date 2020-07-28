from simpleai.search import SearchProblem, breadth_first, depth_first, uniform_cost, greedy, astar
from simpleai.search.viewers import WebViewer, BaseViewer


def en_orilla(posicion):
    fila, columna = posicion
    return fila in (0, 5) or columna in (0, 5)


class ProblemaRobot(SearchProblem):
    def __init__(self, personas_a_rescatar):
        '''
        El estado es una tupla (posicion_robot, personas_a_rescatar, casillas_visitadas)
        '''
        super().__init__(((0, 0), tuple(personas_a_rescatar), tuple()))

    def is_goal(self, state):
        robot, personas_a_rescatar, fragiles_visitadas = state
        return len(personas_a_rescatar) == 0 and en_orilla(robot)

    def cost(self, state1, action, state2):
        return 1

    def actions(self, state):
        acciones = []
        robot, personas_a_rescatar, fragiles_visitadas = state
        fila_robot, columna_robot = robot

        for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            n_fila = fila_robot + df
            n_columna = columna_robot + dc
            n_pos = (n_fila, n_columna)

            if (0 <= n_fila <= 5 and 0 <= n_columna <= 5 and n_pos not in fragiles_visitadas):
                acciones.append(n_pos)

        return acciones

    def result(self, state, action):
        robot, personas_a_rescatar, fragiles_visitadas = state

        if action in personas_a_rescatar:
            personas_a_rescatar = tuple([x for x in personas_a_rescatar if x != action])

        if not en_orilla(action):
            fragiles_visitadas = fragiles_visitadas + (action,)

        return (action, personas_a_rescatar, fragiles_visitadas)

    def heuristic_2(self, state):
        '''
        La maxima de estas distancias:
        Distancia del robot a la orilla mas cercana
        Por cada persona a rescatar:
            distancia entre el robot y la persona a rescatar + desde esa persona a la orilla mas cercana
        '''
        robot, personas_a_rescatar, fragiles_visitadas = state
        distancias = [orilla_mas_cercana(robot)]

        for persona in personas_a_rescatar:
            distancias.append(manhattan(robot, persona) + orilla_mas_cercana(persona))

        return max(distancias)

    def heuristic(self, state):
        robot, personas_a_rescatar, fragiles_visitadas = state
        actual = robot
        distancia = 0

        personas_a_rescatar = list(personas_a_rescatar)
        while personas_a_rescatar:
            distancias_personas = [(manhattan(actual, persona), persona)
                                   for persona in personas_a_rescatar]
            dist, persona = sorted(distancias_personas)[0]
            personas_a_rescatar.remove(persona)
            actual = persona
            distancia += dist

        distancia += orilla_mas_cercana(actual)
        return distancia


def manhattan(pos1, pos2):
    f1, c1 = pos1
    f2, c2 = pos2
    return abs(f2 - f1) + abs(c2 - c1)


def orilla_mas_cercana(posicion):
    f, c = posicion
    return min([f, 5 - f, c, 5 - c])


def resolver(metodo_busqueda, posiciones_personas, mostrar_stats=False):
    problema = ProblemaRobot(posiciones_personas)
    if mostrar_stats:
        viewer = BaseViewer()
    else:
        viewer = None

    funciones = {
        'breadth_first': breadth_first,
        'depth_first': depth_first,
        'greedy': greedy,
        'astar': astar
    }
    funcion_busqueda = funciones[metodo_busqueda]

    resultado = funcion_busqueda(problema, graph_search=True, viewer=viewer)

    if mostrar_stats:
        print("Metodo: {}, Costo: {}, Tamanio maximo frontera: {}, Nodos visitados: {}".format(
            metodo_busqueda, resultado.cost, viewer.stats['max_fringe_size'],
            viewer.stats['visited_nodes']
        ))

    return resultado


if __name__ == '__main__':
    resolver('breadth_first', [(2, 1), (3, 4), (4, 2)], mostrar_stats=True)
    resolver('depth_first', [(2, 1), (3, 4), (4, 2)], mostrar_stats=True)
    resolver('greedy', [(2, 1), (3, 4), (4, 2)], mostrar_stats=True)
    resolver('astar', [(2, 1), (3, 4), (4, 2)], mostrar_stats=True)
