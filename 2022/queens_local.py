import random

from simpleai.search import SearchProblem, genetic
from simpleai.search.local import (hill_climbing,
                                   hill_climbing_random_restarts,
                                   hill_climbing_stochastic,
                                   simulated_annealing)
from simpleai.search.viewers import BaseViewer


class QueensProblem(SearchProblem):
    # for genetic and random restart
    def generate_random_state(self):
        state = list(range(8))
        random.shuffle(state)
        return tuple(state)

    def actions(self, state):
        available_actions = []
        for col, row in enumerate(state):
            if row > 0:
                # puedo subir
                action = (col, row - 1)
                available_actions.append(action)

            if row < 7:
                # puedo bajar
                action = (col, row + 1)
                available_actions.append(action)
        return available_actions

    def result(self, state, action):
        col, new_row = action
        state = list(state)
        state[col] = new_row
        return tuple(state)

    def value(self, state):
        attacks = 0
        for col_1, row_1 in enumerate(state):
            for col_2, row_2 in enumerate(state):
                if col_1 < col_2:
                    # se atacan horizontalmente?
                    if row_1 == row_2:
                        attacks += 1
                    # se atacan diagonal?
                    if abs(row_1 - row_2) == abs(col_1 - col_2):
                        attacks += 1
        return -attacks

    # for genetic
    def mutate(self, state):
        what_queen = random.randint(0, 7)
        where = random.randint(0, 7)
        state = list(state)
        state[what_queen] = where
        state = tuple(state)
        return state

    def crossover(self, state1, state2):
        crosspoint = random.randint(1, 7)
        half_state1 = state1[:crosspoint]
        half_state2 = state2[crosspoint:]
        return half_state1 + half_state2


if __name__ == '__main__':

    print("Hill climbing:")
    problem = QueensProblem()
    viewer = BaseViewer()
    problem.initial_state = problem.generate_random_state()
    result = hill_climbing(problem, iterations_limit=9999, viewer=viewer)
    print(result.state, "Attacks:", -problem.value(result.state), 'Stats', viewer.stats)

    print("Hill climbing random restarts:")
    problem = QueensProblem(None)
    viewer = BaseViewer()
    result = hill_climbing_random_restarts(problem, restarts_limit=999, iterations_limit=9999,
                                           viewer=viewer)
    print(result.state, "Attacks:", -problem.value(result.state), 'Stats', viewer.stats)

    # print("Simulated annealing:")
    # problem = QueensProblem()
    # problem.initial_state = problem.generate_random_state()
    # result = simulated_annealing(problem, iterations_limit=9999)
    # print(result.state, "Attacks:", -problem.value(result.state))

    print("Genetic:")
    problem = QueensProblem(None)
    result = genetic(problem, population_size=150, mutation_chance=0.1, iterations_limit=500)
    print(result.state, "Attacks:", -problem.value(result.state))
