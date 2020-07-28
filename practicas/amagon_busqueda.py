import datetime
import random

from simpleai.search import SearchProblem
from simpleai.search.traditional import astar
from simpleai.search.viewers import BaseViewer

ES = (3, 5)
ACCIONES_MOVER = [('Arriba', (-1, 0)),
                  ('Abajo', (1, 0)),
                  ('Izquierda', (0, -1)),
                  ('Derecha', (0, 1))]


def posicion_valida(fila, columna):
    # No es valido estar afuera del depósito
    if fila < 0 or fila > 6 or columna < 0 or columna > 5:
        return False

    # Los estantes estan en columnas pares. En las mismas solo puedo estar en la fila 3
    if (columna % 2) == 0 and fila != 3:
        return False

    # Las demás posiciones son validas
    return True


def manhattan(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


class ProblemaAmagon(SearchProblem):
    '''Esta es la solución al enunciado del problema de Amagon.

    El estado va a ser una tupla compuesta de:
        Posicion del robot: tuple(fila, columna)
        Cajas a distribuir: Una tupla con cada una de las cajas a distribuir.
        Cajas cargadas: Un tupla con las cajas que el robot tiene cargadas.
                        Cuando una caja es cargada va a desaparecer de la lista anterior.

    Cada caja se va a representar con una tupla (<ID>, <posicion donde dejar la caja>)

    Vamos a considerar como meta cuando el robot repartió todas las cajas y además volvió a la
    posicion de partida.

    Las acciones van a ser:
        * (Mover, Nueva Posicion del robot): Arriba, abajo, izquierda y derecha
        * (Tomar, Caja que toma el robot): Solo aplicable cuando el robot está en el punto de
                                           partida y tiene lugar para cargar cajas
    No vamos a modelar la accion Soltar, vamos a suponer que cuando llega a la posicion final las
    cajas se sueltan automáticamente.

    Heuristica: calcula cuantos acciones faltan tomar. Va a ser una suma de:
        * La cantidad de acciones tomar que faltan: es el largo de cajas a distribuir
        * La distancia de las cajas a su posicion final: Acá hay que tener cuidado porque se puede
             llevar más de una caja a la vez y además, más de 1 caja puede ir a la misma celda.
             * Para las cajas cargadas: tomamos la distancia del robot a la caja más lejana.
             * Para las cajas a distribuir: tomamos la distancia de E/S a la posicion final de la
             caja. Como las cajas pueden ir de a pares, el caso más optimista es que las cajas del
             par tengan la misma celda destino. Un poco menos optimista, es que una de las cajas
             quede de camino a la otra... Con esto en mente, podriamos tomar la distancia mas lejana
             del par y estamos contemplando no sobreestimar. Para armar los pares vamos a ordenar
             las distancias de mayor a menor e ir tomando cajas contiguas. De esta forma vamos
             a reducir al maximo el valor de la prediccion y por ende, no vamos a sobreestimar.
    '''
    def __init__(self, a_distribuir):
        inicial = (ES, tuple(a_distribuir), tuple())
        super().__init__(inicial)

    def is_goal(self, state):
        pos_robot, a_distribuir, cargadas = state
        return pos_robot == ES and len(a_distribuir) == 0 and len(cargadas) == 0

    def actions(self, state):
        pos_robot, a_distribuir, cargadas = state
        fila_robot, columna_robot = pos_robot

        acciones = []

        # mover
        for nombre, (df, dc) in ACCIONES_MOVER:
            nueva_fila = fila_robot + df
            nueva_columna = columna_robot + dc
            if posicion_valida(nueva_fila, nueva_columna):
                acciones.append((nombre, (nueva_fila, nueva_columna)))

        # tomar
        if pos_robot == ES and len(cargadas) < 2:
            for caja in a_distribuir:
                acciones.append(('Tomar', caja))
        return acciones

    def result(self, state, action):
        pos_robot, a_distribuir, cargadas = state

        if action[0] == 'Tomar':
            caja = action[1]
            # saco la caja de a_distribuir y la agrego a cargadas
            a_distribuir = tuple([x for x in a_distribuir if x != caja])
            cargadas = cargadas + (caja, )
        else:
            pos_robot = action[1]
            # muevo el robot y si alguna caja cargada tiene como destino la nueva posicion, la
            # descargo
            cargadas = tuple([c for c in cargadas if c[1] != pos_robot])

        return (pos_robot, a_distribuir, cargadas)

    def cost(self, state1, action, state2):
        return 1

    def heuristic(self, state):
        pos_robot, a_distribuir, cargadas = state

        h_tomar = len(a_distribuir)

        if len(cargadas) > 0:
            distancias_cargadas = []
            for _, destino_caja in cargadas:
                distancias_cargadas.append(manhattan(pos_robot, destino_caja))
            h_cargadas = min(distancias_cargadas)
        else:
            h_cargadas = 0

        if len(a_distribuir) > 0:
            distancias = []
            for _, destino_caja in a_distribuir:
                distancias.append(manhattan(ES, destino_caja))

            distancias = sorted(distancias, reverse=True)
            # tomamos una distancia por medio para ir armando los pares
            distancias_a_considerar = distancias[::2]
            h_distribuir = sum(distancias_a_considerar)
        else:
            h_distribuir = 0

        return h_tomar + h_cargadas + h_distribuir


def resolver(cajas):
    problema = ProblemaAmagon(cajas)

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


def main():
    print('#' * 80)
    cajas = [('C1', (0, 1)), ('C2', (1, 1)), ('C3', (2, 5))]
    print('Ejemplo simple con {} cajas'.format(len(cajas)))
    resolver(cajas)
    print('#' * 80)

    print('#' * 80)
    cajas = []
    for i in range(6):
        fila = random.choice([0, 1, 2, 4, 5, 6])
        columna = random.choice([1, 3, 5])
        cajas.append(('C{}'.format(i), (fila, columna)))

    print('Ejemplo random con {} cajas'.format(len(cajas)))
    resolver(cajas)
    print('#' * 80)


if __name__ == '__main__':
    main()
