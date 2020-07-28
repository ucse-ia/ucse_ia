# coding: utf-8
import datetime
from itertools import chain, combinations
from simpleai.search import astar, SearchProblem
from simpleai.search.viewers import BaseViewer


def a_listas(tuplas):
    return [list(x) for x in tuplas]


def a_tuplas(listas):
    return tuple([tuple(x) for x in listas])


class PresidentesProblem(SearchProblem):
    def __init__(self):
        '''
        En el estado necesitamos cuantos presidentes de cada faccion hay en cada area.
        Para eso vamos a hacer que el estado sea una tupla con tres tuplas adentro representando
        cada una de las areas: Auditorio, Hall y Sala de prensa.
        En cada una de las areas vamos a enumerar los presidentes que se encuentran adentro.

        Los presidentes los vamos a representar solo con una letra de la faccion a la que
        representan: cApitalistas, cEntristas y cOmunistas
        '''
        inicial = (('a', 'a', 'e', 'e', 'o', 'o'), tuple(), tuple())
        super(PresidentesProblem, self).__init__(inicial)

    def is_goal(self, state):
        'Nuestra meta es que todos los presidentes esten en la ultima sala'
        return len(state[2]) == 6

    def actions(self, state):
        '''
        Las acciones posibles, por cada sala que no sea la ultima, son:
        * Mover cada presidente de forma individual
        * Mover todas las combinaciones de a 2 presidentes posibles.

        Las acciones las vamos a representar con una tupla <sala origin, <presidentes_a_mover>>
        '''
        acciones = []

        for sala in (0, 1):
            presidentes_en_la_sala = state[sala]
            posibles_combinaciones = chain(combinations(presidentes_en_la_sala, 1),
                                           combinations(presidentes_en_la_sala, 2))
            for presidentes_a_mover in posibles_combinaciones:
                accion = (sala, presidentes_a_mover)
                estado_resultante = self.result(state, accion)
                if self.es_valido(estado_resultante):
                    acciones.append(accion)
        return acciones

    def es_valido(self, state):
        '''
        Un estado es valido si:
        * No hay dos presidentes de la misma faccion solos en una sala.
        * Entre dos presidentes de la misma faccion no hay una sala de por medio.
        '''
        # dos presidentes de la misma faccion en una sala
        for sala in state:
            cantidad_presidentes = len(sala)
            cantidad_facciones = len(set(sala))
            if cantidad_presidentes == 2 and cantidad_facciones == 1:
                return False

        # Separados en salas no adyacentes. Para que esto ocurra, la unica opcion es que haya
        # un presidente de una faccion en la primer sala y el otro en la ultima. Dicho de otra forma
        # hay que validar que las facciones que aparecen en la primer sala no aparezcan en la ultima
        # y viceversa. O sea, la interseccion de estos conjuntos debe ser vacia.
        sala_0 = set(state[0])
        sala_2 = set(state[2])
        return len(sala_0.intersection(sala_2)) == 0

    def result(self, state, action):
        state = a_listas(state)
        sala, presidentes = action
        for p in presidentes:
            state[sala + 1].append(p)
            state[sala].remove(p)
        return a_tuplas(state)

    def cost(self, state1, action, state2):
        'El costo de la acción es siempre 1'
        return 1

    def heuristic(self, state):
        '''
        Una posible heuristica es la cantidad de presidentes que faltan en la sala de prensa.
        Como con un solo movimiento podemos mover 2 presidentes, al numero anterior lo dividimos por
        dos.
        '''
        return (6 - len(state[2])) // 2


def main():
    problema = PresidentesProblem()

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
