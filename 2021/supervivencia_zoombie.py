from simpleai.search import SearchProblem, astar

ZONA_SEGURA = (4, 4)
OBSTACULOS = [(0, 1), (0, 2), (1, 4), (2, 1), (3, 1), (3, 3), (4, 3)]

# El estado es una tupla que tiene:
# * la posicion de la protagonista
# * los zombies (si, en el estado, porque los podemos eliminar)
# * la cantidad de vida del personaje
# * la cantidad de balas disponibles

ESTADO_INICIAL = (
    (0, 0),
    ((1, 0), (1, 1), (1, 2), (1, 3), (2, 3)),
    100,
    3,
)


def en_grilla(posicion):
    return all(0 <= c <= 4 for c in posicion)


def adyacentes(posicion):
    posiciones_adyacentes = []
    fila, columna = posicion
    for d_f, d_c in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nueva_posicion = (fila + d_f, columna + d_c)
        if en_grilla(nueva_posicion):
            posiciones_adyacentes.append(nueva_posicion)
    return posiciones_adyacentes


class AlectoProblem(SearchProblem):

    def is_goal(self, state):
        "Es meta si llegue a la zona segura"
        posicion_protagonista, _, _, _ = state
        return posicion_protagonista == ZONA_SEGURA

    def actions(self, state):
        """Las acciones son moverse a cada una de las casillas adyacentes evitando morir, matando o
        no en caso de que haya un zombie.
        """
        posicion_actual, zombies, vida, balas = state

        acciones = []
        for nueva_posicion in adyacentes(posicion_actual):
            if nueva_posicion in OBSTACULOS:
                # hay obstaculo, no nos podemos mover
                continue

            if nueva_posicion in zombies:
                if balas > 0:
                    acciones.append(('disparar', nueva_posicion))

                if vida > 30:
                    acciones.append(('mover_con_zombie', nueva_posicion))
            else:
                acciones.append(('mover', nueva_posicion))

        return acciones

    def result(self, state, action):
        posicion_actual, zombies, vida, balas = state
        accion, nueva_posicion = action
        if accion == 'disparar':
            zombies = tuple(zombie for zombie in zombies if zombie != nueva_posicion)
            balas -= 1
        elif accion == 'mover_con_zombie':
            vida -= 30
        return (nueva_posicion, zombies, vida, balas)

    def cost(self, state1, action, state2):
        accion = action[0]
        if accion == 'mover':
            cost = 5
        elif accion == 'disparar':
            cost = 20
        else:
            cost = 10
        return cost

    def heuristic(self, state):
        "Distancia de Manhattan considerando que todas las casillas estan libres de zombies"
        posicion = state[0]
        distancia = abs(posicion[0] - ZONA_SEGURA[0]) + abs(posicion[1] - ZONA_SEGURA[1])
        return distancia * 5


problema = AlectoProblem(ESTADO_INICIAL)
solucion = astar(problema, graph_search=True)

for accion, estado in solucion.path():
    if accion:
        accion = accion[0]
    posicion, _, vida, balas = estado
    print(f"Posicion: {posicion} Vida: {vida} Balas: {balas} Accion: {accion}")
