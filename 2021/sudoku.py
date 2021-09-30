from itertools import combinations

from simpleai.search import CspProblem, backtrack


columns = list(range(9))
rows = list(range(9))

problem_variables = [
    (row, col)
    for row in rows
    for col in columns
]

domains = {}
for cells in problem_variables:
    domains[cells] = [1, 2, 3, 4, 5, 6, 7, 8, 9]


# TODO 1:
# limpiar y dejar solo 1 valor en los dominios de las celdas ya rellenas
# ej:
domains[(0, 2)] = [3, ]  # porque la casilla A3 tiene el número 3


constraints = []

def cells_are_different(variables, values):
    digit1, digit2 = values
    return digit1 != digit2


for row in rows:
    cells_in_row = [
        (row, col)
        for col in columns
    ]
    for cell1, cell2 in combinations(cells_in_row, 2):
        constraints.append(
            ((cell1, cell2), cells_are_different)
        )

for col in columns:
    cells_in_col = [
        (row, col)
        for row in rows
    ]
    for cell1, cell2 in combinations(cells_in_col, 2):
        constraints.append(
            ((cell1, cell2), cells_are_different)
        )


# TODO 2:
# agregar todas las restricciones de que sean diferentes las celdas dentro de cada mega-cuadrado (de 3x3)

problem = CspProblem(problem_variables, domains, constraints)
solution = backtrack(problem)

print("Solution:")
print(solution)
