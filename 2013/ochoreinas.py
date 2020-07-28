import random
from simpleai.search import SearchProblem
from simpleai.search import hill_climbing, hill_climbing_stochastic, hill_climbing_random_restarts, beam, simulated_annealing, genetic


INITIAL = (0, 0, 0, 0, 0, 0, 0, 0,)


class OchoReinas(SearchProblem):
    def actions(self, state):
        actions = []

        for reina, fila in enumerate(state):
            if fila > 0:
                actions.append((reina, fila - 1))
            if fila < 7:
                actions.append((reina, fila + 1))

        return actions

    def result(self, state, action):
        state = list(state)
        reina, fila = action

        state[reina] = fila

        return tuple(state)

    def value(self, state):
        maldad = 0

        for reina, fila in enumerate(state):
            for reina2, fila2 in enumerate(state):
                if reina != reina2:
                    diferencia_c = abs(reina - reina2)
                    diferencia_f = abs(fila - fila2)

                    if fila == fila2 or diferencia_c == diferencia_f:
                        maldad += 1

        return -maldad

    def generate_random_state(self):
        return tuple(random.randint(0, 7) for x in range(8))


result = hill_climbing(OchoReinas(INITIAL))
#result = hill_climbing_stochastic(OchoReinas(INITIAL))
#result = hill_climbing_random_restarts(OchoReinas(), restarts_limit=100)
#result = beam(OchoReinas(), beam_size=5)
#result = simulated_annealing(OchoReinas(INITIAL), iterations_limit=20)

print result


