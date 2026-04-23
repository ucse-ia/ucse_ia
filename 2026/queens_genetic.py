from random import randint
from itertools import combinations

from simpleai.search import SearchProblem, genetic


N_QUEENS = 8


class QueensProblem(SearchProblem):
    def value(self, state):
        queens = list(range(N_QUEENS))
        attacking_pairs = 0

        # por cada par posible de reinas, ver si se atacan
        for queen_col1, queen_col2 in combinations(queens, 2):
            queen_row1 = state[queen_col1]
            queen_row2 = state[queen_col2]

            if queen_row1 == queen_row2:
                # misma fila?
                attacking_pairs += 1
            elif abs(queen_col1 - queen_col2) == abs(queen_row1 - queen_row2):
                # están en diagonal
                attacking_pairs += 1

        return -attacking_pairs

    def generate_random_state(self):
        state = [
            randint(0, N_QUEENS - 1)
            for _ in range(N_QUEENS)
        ]

        return tuple(state)

    def crossover(self, state1, state2):
        cut_index = randint(1, N_QUEENS - 1)

        first_half = state1[:cut_index]
        second_half = state2[cut_index:]

        child = first_half + second_half
        return child

    def mutate(self, state):
        mutation_position = randint(0, N_QUEENS - 1)
        new_value = randint(0, N_QUEENS - 1)

        state = list(state)
        state[mutation_position] = new_value

        return tuple(state)


if __name__ == "__main__":
    p = QueensProblem(None)

    result = genetic(p, population_size=100, mutation_chance=0.1, iterations_limit=1000)

    print("Board:")
    print(result.state)
    print("Attacks:")
    print(p.value(result.state))

