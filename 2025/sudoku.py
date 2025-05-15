from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    min_conflicts,
)


variables = [
    (row, col)
    for row in range(9)
    for col in range(9)
]

domains = {
    variable: [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for variable in variables
}

constraints = []


def not_same_digit(variables, values):
    val1, val2 = values
    return val1 != val2


for cell1, cell2 in combinations(variables, 2):
    row1, col1 = cell1
    row2, col2 = cell2

    same_row = row1 == row2
    same_col = col1 == col2
    same_group = (
        (row1 // 3 == row2 // 3)
        and (col1 // 3 == col2 // 3)
    )

    if same_row or same_col or same_group:
        constraints.append(((cell1, cell2), not_same_digit))


problem = CspProblem(variables, domains, constraints)
solution = backtrack(problem)

print(solution)
