# coding: utf-8
from simpleai.search import astar, SearchProblem
from simpleai.search.viewers import WebViewer


class JarrosProblem(SearchProblem):
    def __init__(self, numero_de_jarros):
        '''
        El estado lo representamos con una tupla de N posiciones, donde el
        jarro de capacidad x esta en la posición x-1.

        En el estado inicial tenemos todos los jarros vacios excepto el
        último que está lleno
        '''

        self.N = numero_de_jarros
        inicial = tuple([0] * (self.N - 1) + [self.N])
        super(JarrosProblem, self).__init__(inicial)

    def is_goal(self, state):
        'Nuestra meta es que todos los jarros posean 1 litro de agua'
        return all(x == 1 for x in state)

    def capacidad(self, posicion_jarro, litros_que_tiene):
        'Funcion auxiliar para calcular la capacidad restante de un jarro'
        return posicion_jarro + 1 - litros_que_tiene

    def actions(self, state):
        '''
        El enunciado dice que las operaciones son trasvasar de un jarro a otro,
        con lo cual, nuestras acciones van a ser una tupla (jarro_origen, jarro_destino),
        siendo jarro_origen y jarro_destino las posiciones de los jarros.

        Una acción va a ser aplicable solo cuando jarro_origen tenga agua y
        jarro_destino no esté lleno.
        '''
        acciones = []
        for jarro_origen, litros_origen in enumerate(state):
            for jarro_destino, litros_destino in enumerate(state):
                if (litros_origen > 0 and self.capacidad(jarro_destino, litros_destino) > 0):
                    acciones.append((jarro_origen, jarro_destino))
        return acciones

    def cost(self, state1, action, state2):
        'El costo de la acción es la capacidad total del jarro origen'
        return action[0] + 1

    def result(self, state, action):
        '''
        Esta funcion le quita X litros a jarro origen y los pone en jarro_destino

        X puede ser los litros del jarro origen o lo que falte para llenar el
        jarro destino, lo que demande menos agua.
        '''
        jarro_origen, jarro_destino = action
        litros_origen, litros_destino = state[jarro_origen], state[jarro_destino]

        a_trasvasar = min(litros_origen,
                          self.capacidad(jarro_destino, litros_destino))

        s = list(state)
        s[jarro_origen] -= a_trasvasar
        s[jarro_destino] += a_trasvasar

        return tuple(s)

    def heuristic(self, state):
        'Una posible heuristica es la cantidad de jarros que no tienen agua'
        return len([x for x in state if x == 0])


# Resolucion por A*
result = astar(JarrosProblem(4), graph_search=True, viewer=WebViewer())
