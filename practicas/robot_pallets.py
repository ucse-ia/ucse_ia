# coding: utf-8
import datetime
from simpleai.search import astar, SearchProblem
from simpleai.search.viewers import BaseViewer


class RobotProblem(SearchProblem):
    def __init__(self, pallets_a_entregar):
        '''
        En el estado necesitamos llevar la posición de los pallets, la del
        robot, si tenemos un pallet cargado cual es y la lista de pallets por
        llevar. El estado entonces lo vamos a representar con una tupla con
        estos elementos, las posiciones serán tuplas de coordenadas y para los
        pallets una tupla de posiciones para cada pallet. Si el pallet deja de
        estar en el tablero la posición sera None.

        Las coordenadas arrancan en (0, 0). Por ejemplo, la posicion de entrega
        es (2, 4)
        '''
        self.posicion_entrega = (2, 4)

        pallets = ((0, 2), (1, 0), (3, 0), (2, 0), (0, 2),
                   (4, 0), (4, 1), (2, 2), (0, 4), (1, 1))
        robot = (1, 4)
        cargado = None

        inicial = (pallets, robot, cargado, tuple([p-1 for p in pallets_a_entregar]))
        super(RobotProblem, self).__init__(inicial)

    def is_goal(self, state):
        'Nuestra meta es que todos los pallets hayan sido entregados'
        return len(state[3]) == 0

    def actions(self, state):
        '''
        Las acciones posibles son moverse hacia los 4 lados, dejar y agarrar.

        Para poder moverse no debemos salir del tablero o entrar en la casilla
        de un pallet que no vamos a tomar.

        Para agarrar debemos estar en la misma posicion que el pallet. Si
        estamos en la misma posición que un pallet, entonces estamos obligados
        a tomarlo.

        Para dejar un pallet tenemos que estar en la posición de entrega con un
        pallet cargado.
        '''
        acciones = []

        pallets, robot, cargado, pendientes = state

        x, y = robot
        pallet_en_posicion = self.buscar_pallet_en_coordenadas(x, y, pallets)

        if pallet_en_posicion is not None:
            acciones.append(('Agarrar', None, None))
        else:
            acciones.extend(self.calcular_movimientos(state))
            if cargado is not None and robot == self.posicion_entrega:
                acciones.append(('Dejar', None, None))

        return acciones

    def calcular_movimientos(self, state):
        posibles_movimientos = [
            ('Arriba', -1, 0),
            ('Abajo', 1, 0),
            ('Izquierda', 0, -1),
            ('Derecha', 0, 1),
        ]
        movimientos = []

        pallets, robot, cargado, pendientes = state
        cx, cy = robot

        for accion, dx, dy in posibles_movimientos:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx <= 4 and 0 <= ny <= 4:
                p = self.buscar_pallet_en_coordenadas(nx, ny, pallets)
                if p is None or (p in pendientes and cargado is None):
                    movimientos.append((accion, dx, dy))
        return movimientos

    def buscar_pallet_en_coordenadas(self, x, y, pallets):
        for pallet, posicion in enumerate(pallets):
            if (x, y) == posicion:
                return pallet
        return None

    def result(self, state, action):
        pallets, robot, cargado, pendientes = state
        x, y = robot
        accion, dx, dy = action

        if accion == 'Dejar':
            pendientes = tuple([w for w in pendientes if w != cargado])
            cargado = None
        elif accion == 'Agarrar':
            cargado = self.buscar_pallet_en_coordenadas(x, y, pallets)
            pallet_list = list(pallets)
            pallet_list[cargado] = None
            pallets = tuple(pallet_list)
        else:
            robot = (x + dx, y + dy)

        return (pallets, robot, cargado, pendientes)

    def cost(self, state1, action, state2):
        'El costo de la acción es siempre 1'
        return 1

    def heuristic(self, state):
        '''
        Una posible heuristica es la suma de las distancias de Manhattan de
        cada uno de los pallets a quitar
        '''
        pallets, robot, cargado, pendientes = state
        posiciones_pendientes = [pallets[x] for x in pendientes if x != cargado]

        if cargado is not None:
            posiciones_pendientes.append(robot)
        return sum([manhattan(x, self.posicion_entrega)
                    for x in posiciones_pendientes])

    def state_representation(self, state):
        pallets, robot, cargado, pendientes = state
        template = [['   ']*5 for x in range(5)]
        for pallet, pos in enumerate(pallets):
            if pos is not None:
                fila, columna = pos
                template[fila][columna] = str(pallet+1)
        x, y = self.posicion_entrega
        template[x][y] = 'E'
        r = 'R'
        if cargado:
            r = 'R' + str(cargado+1)
        x, y = robot
        template[x][y] = r
        return '\n'.join([' | '.join(fila) for fila in template])


def manhattan(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x2 - x1) + abs(y2 - y1)


def main():
    problema = RobotProblem([8, 3, 9])

    visor = BaseViewer()
    inicio = datetime.datetime.now()
    resultado = astar(problema, graph_search=True, viewer=visor)
    tiempo = (datetime.datetime.now() - inicio).total_seconds()

    for i, (accion, estado) in enumerate(resultado.path()):
        print('Acción N: {} {} ## Estado: {}'.format(i, accion, estado))

    print("Costo: {}".format(resultado.cost))
    print("Nodos explorados: {}".format(visor.stats['visited_nodes']))
    print("Tamaño máximo frontera: {}".format(visor.stats['max_fringe_size']))
    print("Tiempo transcurrido: {} segundos".format(tiempo))


if __name__ == '__main__':
    main()
