import random

from simpleai.search import (SearchProblem, hill_climbing, hill_climbing_stochastic,
                             hill_climbing_random_restarts, beam)
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer

ITEMS = tuple('ABCDLHQSV')
CONFLICTOS = (
    ('H', 'S'),
    ('Q', 'S'),
    ('Q', 'B'),
    ('C', 'V'),
)

PRECIOS = {
    'A': 5000,
    'B': 4000,
    'C': 500,
    'D': 3000,
    'L': 2500,
    'H': 2000,
    'Q': 200,
    'S': 3000,
    'V': 2000,
}


class ItemsDota(SearchProblem):
    def cost(self, state1, action, state2):
        return 1

    def actions(self, state):
        reemplazos = []

        for item_actual in state:
            for otro_item in ITEMS:
                if otro_item not in state:
                    reemplazos.append((item_actual, otro_item))

        return reemplazos

    def result(self, state, action):
        item_actual, nuevo_item = action
        items = list(state)
        items.remove(item_actual)
        items.append(nuevo_item)

        return tuple(items)

    def value(self, state):
        # arranca siendo la suma de todos los precios
        suma = sum(PRECIOS[item] for item in state)
        # pero despues restamos los precios de las cosas "rotas" por conflicto
        for item_a, item_b in CONFLICTOS:
            if item_a in state and item_b in state:
                suma -= PRECIOS[item_a]
                suma -= PRECIOS[item_b]

        return suma

    def generate_random_state(self):
        items_disponibles = list(ITEMS)  # creamos una copia para nosotros
        random.shuffle(items_disponibles)

        items_equipados = []
        for i in range(4):
            items_equipados.append(items_disponibles.pop())

        return tuple(items_equipados)

print 'Hill climbing:'
v = BaseViewer()
result = hill_climbing(ItemsDota(('A', 'B', 'C', 'D')), viewer=v)
print result.state
print result.value
print v.stats


print 'Hill climbing random restarts'
result = hill_climbing_random_restarts(ItemsDota(), restarts_limit=100)
print result.state
print result.value
