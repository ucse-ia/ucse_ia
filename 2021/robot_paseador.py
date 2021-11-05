from simpleai.search import SearchProblem, astar
# from simpleai.search.viewers import BaseViewer, WebViewer

ARBOLES = [(0, 2), (1, 0), (3, 1), (3, 4), (4, 2)]
TERO = (2, 2)
RAMA = (1, 1)
CANCHA = (3, 3)
ENTRADA = (0, 4)
DE_INTERES = set(ARBOLES + [CANCHA, RAMA])

# El estado es una tupla que tiene la posicion del robot <fila, columna>
# y las posiciones que restan visitar
ESTADO_INICIAL = (ENTRADA, tuple(DE_INTERES))


def en_grilla(posicion):
    return all(0 <= c <= 4 for c in posicion)


class AlectoProblem(SearchProblem):

    def is_goal(self, state):
        "Es meta si no quedan cosas por visitar"
        _, por_visitar = state
        return len(por_visitar) == 0

    def actions(self, state):
        """Las acciones son moverse a cada una de las casillas adyacentes,
        evitando el tero y las casillas de interes ya visitadas
        """
        (fila_robot, columna_robot), por_visitar = state
        posiciones_visitadas = DE_INTERES - set(por_visitar)
        acciones_posibles = []
        for d_f, d_c in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nueva_fila = fila_robot + d_f
            nueva_columna = columna_robot + d_c
            nueva_posicion = (nueva_fila, nueva_columna)

            if (en_grilla(nueva_posicion)
                    and (nueva_posicion != TERO)
                    and nueva_posicion not in posiciones_visitadas):
                acciones_posibles.append(nueva_posicion)

        return acciones_posibles

    def result(self, state, action):
        nueva_posicion = action
        _, por_visitar = state

        # Filtro de por_visitar la posicion que acabo de visitar,
        # siempre y cuando no sea la cancha y aun no tenga la rama
        por_visitar = tuple([
            posicion
            for posicion in por_visitar
            if (posicion != nueva_posicion
                or posicion == CANCHA and RAMA in por_visitar)
        ])
        return (nueva_posicion, por_visitar)

    def cost(self, state1, action, state2):
        _, por_visitar = state1
        nueva_posicion = action
        cost = 10
        if nueva_posicion in ARBOLES:
            cost = 20
        elif nueva_posicion == CANCHA and RAMA not in por_visitar:
            cost = 120
        elif nueva_posicion == RAMA:
            cost = 60
        return cost

    def heuristic(self, state):
        "Sumamos los tiempos de los sitios de interes por visitar"
        costo_faltante = 0
        _, por_visitar = state
        for sitio in por_visitar:
            if sitio in ARBOLES:
                costo_faltante += 20
            elif sitio == CANCHA:
                costo_faltante += 120
            elif sitio == RAMA:
                costo_faltante += 60
        return costo_faltante


problema = AlectoProblem(ESTADO_INICIAL)
solucion = astar(problema, graph_search=True)

for accion, estado in solucion.path():
    print("Action:", accion, "Pendientes:", estado[1])
