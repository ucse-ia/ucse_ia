import random

from simpleai.search import SearchProblem, genetic



class GeneticQueensProblem(SearchProblem):
    def generate_random_state(self):
        queens = list(range(8))
        random.shuffle(queens)

        return tuple(queens)

    def mutate(self, state):
        queens = list(state)

        queen_to_mutate = random.randint(0, 7)
        new_row = random.randint(0, 7)

        queens[queen_to_mutate] = new_row

        return tuple(queens)

    def crossover(self, state1, state2):
        cross_point = random.randint(0, 7)

        half_from_state1 = state1[:cross_point]
        half_from_state2 = state2[cross_point:]

        new_state = half_from_state1 + half_from_state2

        return new_state

    def value(self, state):
        attacks = 0

        for queen_col, queen_row in enumerate(state):
            for queen2_col, queen2_row in enumerate(state):
                if queen_col < queen2_col:
                    # no son la misma reina, chequeemos ataques
                    if queen_row == queen2_row:
                        # están en la misma fila
                        attacks += 1
                    else:
                        # están en la misma diagonal?
                        cols_diff = abs(queen_col - queen2_col)
                        rows_diff = abs(queen_row - queen2_row)

                        if cols_diff == rows_diff:
                            # están en la misma diagonal
                            attacks += 1

        return -attacks


problem = GeneticQueensProblem(None)

result = genetic(problem, population_size=150, mutation_chance=0.1, iterations_limit=100)

print(result.state)
print("Attacks:", -problem.value(result.state))


