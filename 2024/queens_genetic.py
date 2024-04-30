from simpleai.search import (
    SearchProblem,
    genetic,
)
from simpleai.search.viewers import BaseViewer, WebViewer
import random


BOARD_SIZE = 8


class QueensProblem(SearchProblem):
    def value(self, state):
        attacks = 0
        for queen_number, current_row in enumerate(state):
            for other_queen_number, other_current_row in enumerate(state):
                if queen_number != other_queen_number:
                    if current_row == other_current_row:
                        attacks += 1
                    else:
                        delta_rows = abs(current_row - other_current_row)
                        delta_cols = abs(queen_number - other_queen_number)
                        if delta_cols == delta_rows:
                            attacks += 1

        return -attacks

    def generate_random_state(self):
        board = tuple(
            random.randint(0, BOARD_SIZE - 1)
            for _ in range(BOARD_SIZE)
        )
        return board

    def crossover(self, state1, state2):
        cut_index = random.randint(1, BOARD_SIZE - 1)
        first_half = state1[:cut_index]
        second_half = state2[cut_index:]

        child = first_half + second_half
        return child

    def mutate(self, state):
        queen_to_mutate = random.randint(0, BOARD_SIZE - 1)
        new_row = random.randint(0, BOARD_SIZE - 1)

        state = list(state)
        state[queen_to_mutate] = new_row

        return tuple(state)


problem = QueensProblem(None)

result = genetic(problem, population_size=500, mutation_chance=0.1, iterations_limit=100, viewer=WebViewer())

print("Final state: (value:", problem.value(result.state), ")")
print(result.state)
