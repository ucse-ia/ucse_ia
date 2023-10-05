from simpleai.search import (
    SearchProblem,
    genetic,
)
from simpleai.search.viewers import BaseViewer, WebViewer
import random


INITIAL = (0, 0, 0, 0, 0, 0, 0, 0)


class QueensProblem(SearchProblem):
    def value(self, state):
        attacks = 0
        for queen, queen_row in enumerate(state):
            how_many_in_this_row = state.count(queen_row)
            attacks += how_many_in_this_row - 1

            for other_queen, other_queen_row in enumerate(state):
                if queen != other_queen:
                    diff_rows = abs(queen_row - other_queen_row)
                    diff_cols = abs(queen - other_queen)
                    if diff_rows == diff_cols:
                        attacks += 1

        return -attacks

    def generate_random_state(self):
        return tuple(
            random.randint(0, 7)
            for _ in range(8)
        )

    def crossover(self, state1, state2):
        cut_position = random.randint(1, 6)
        first_half = state1[:cut_position]
        second_half = state2[cut_position:]

        return first_half + second_half

    def mutate(self, state):
        mutation_pos = random.randint(0, 7)
        state = list(state)
        possible_values = list(range(8))
        possible_values.remove(state[mutation_pos])
        state[mutation_pos] = random.choice(possible_values)
        return tuple(state)



viewer = BaseViewer()
problem = QueensProblem(INITIAL)
result = genetic(problem, population_size=100, mutation_chance=0.1, iterations_limit=1000, viewer=viewer)

print("Result:", result.state)
print("Value:", problem.value(result.state))
print("Stats:", viewer.stats)


