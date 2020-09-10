from random import shuffle

from itertools import combinations
from simpleai.search import (
    SearchProblem,
    hill_climbing,
    hill_climbing_random_restarts,
    simulated_annealing,
)
from eight_puzzle import find


INITIAL_STATE = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9),
)


class CuadradosProblem(SearchProblem):
    def actions(self, state):
        """
        Todas las combinaciones de los números del 1 al 9, tomadas de a 2.
        (son los pares de fichas que podemos intercambiar).
        """
        return list(combinations(range(1, 10), 2))

    def result(self, state, action):
        state = list(list(fila) for fila in state)
        numero_a, numero_b = action

        fila_a, col_a = find(numero_a, state)
        fila_b, col_b = find(numero_b, state)

        state[fila_a][col_a] = numero_b
        state[fila_b][col_b] = numero_a

        return tuple(tuple(fila) for fila in state)

    def value(self, state):
        totales = []

        # totales por fila
        for fila in state:
            totales.append(sum(fila))

        # totales por columna
        for indice_col in range(3):
            numeros_col = [fila[indice_col] for fila in state]
            totales.append(sum(numeros_col))

        # cuantos hay igual a 15??
        correctas = totales.count(15)

        return correctas

    def generate_random_state(self):
        numeros = list(range(1, 10))
        shuffle(numeros)

        state = tuple(numeros[:3]), tuple(numeros[3:6]), tuple(numeros[6:])

        return state


if __name__ == '__main__':
    problema = CuadradosProblem(INITIAL_STATE)
    # resultado = hill_climbing(problema)
    # resultado = simulated_annealing(problema)
    resultado = hill_climbing_random_restarts(problema, 1000)

    print(resultado.state)
    print('Cuantas dan 15?:', problema.value(resultado.state))

