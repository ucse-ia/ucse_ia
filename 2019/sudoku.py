import itertools

from simpleai.search import (CspProblem, backtrack, min_conflicts,
                             MOST_CONSTRAINED_VARIABLE,
                             LEAST_CONSTRAINING_VALUE,
                             HIGHEST_DEGREE_VARIABLE)


def different(variables, values):
    val1, val2 = values
    return val1 != val2


def big_square_of(cell):
    row, col = cell
    return row // 3, col // 3


def solve_sudoku(board):
    variables = [(row, col)
                 for row in range(9)
                 for col in range(9)]

    domains = {variable: list(range(1, 10))
               for variable in variables}

    for cell, number in board.items():
        domains[cell] = [number, ]

    constraints = []

    for cell1, cell2 in itertools.combinations(variables, 2):
        row1, col1 = cell1
        row2, col2 = cell2

        if (row1 == row2) or (col1 == col2) or (big_square_of(cell1) == big_square_of(cell2)):
            constraints.append(((cell1, cell2), different))

    problem = CspProblem(variables, domains, constraints)
    result = backtrack(problem,
                       variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                       inference=True)

    return result


if __name__ == '__main__':
    board = {
        (0, 2): 3,
        (0, 4): 2,
        (0, 6): 6,
        (1, 0): 9,
        (1, 3): 3,
        (1, 5): 5,
        (1, 8): 1,
        (2, 2): 1,
        (2, 3): 8,
        (2, 5): 6,
        (2, 6): 4,
        (3, 2): 8,
        (3, 3): 1,
        (3, 5): 2,
        (3, 6): 9,
        (4, 0): 7,
        (4, 8): 8,
        (5, 2): 6,
        (5, 3): 7,
        (5, 5): 8,
        (5, 6): 2,
        (6, 2): 2,
        (6, 3): 6,
        (6, 5): 9,
        (6, 6): 5,
        (7, 0): 8,
        (7, 3): 2,
        (7, 5): 3,
        (7, 8): 9,
        (8, 2): 5,
        (8, 4): 1,
        (8, 6): 3,
    }

    result = solve_sudoku(board)
    for row in range(9):
        if row % 3 == 0:
            print('-' * 24)

        for col in range(9):
            if col % 3 == 0:
                print('|', end=' ')

            cell = row, col
            number = result[cell]
            print(number, end=' ')

        print()
