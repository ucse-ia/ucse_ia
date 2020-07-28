import random

from simpleai.search import SearchProblem, genetic

N = 4

class GeneticQueens(SearchProblem):
    def crossover(self, state1, state2):
        cut_point = random.randint(1, N - 1)
        child = state1[:cut_point] + state2[cut_point:]
        return child

    def mutate(self, state):
        queen = random.randint(0, N - 1)
        new_row = random.randint(0, N - 1)
        state = list(state)
        state[queen] = new_row
        return tuple(state)

    def value(self, state):
        attacks = 0

        for queen, current_row in enumerate(state):
            for queen2, current_row2 in enumerate(state):
                if queen < queen2:
                    # same row
                    if current_row == current_row2:
                        attacks += 1
                    else:
                        # diagonal
                        diff_col = abs(queen - queen2)
                        diff_row = abs(current_row - current_row2)
                        if diff_col == diff_row:
                            attacks += 1

        return -attacks

    def generate_random_state(self):
        state = []
        for queen in range(N):
            row = random.randint(0, N - 1)
            state.append(row)

        return tuple(state)


if __name__ == '__main__':
    problem = GeneticQueens(None)
    result = genetic(problem, population_size=200, mutation_chance=0.1,
                     iterations_limit=500)
    print(result.state)
    print('Attacks:', -problem.value(result.state))
