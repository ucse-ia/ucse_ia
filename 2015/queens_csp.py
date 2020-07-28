import itertools
from simpleai.search import CspProblem, backtrack, MOST_CONSTRAINED_VARIABLE, LEAST_CONSTRAINING_VALUE, HIGHEST_DEGREE_VARIABLE, min_conflicts

variables = ['r' + str(columna) for columna in range(8)]

dominios = {}
for reina in variables:
    dominios[reina] = range(8)


def distinta_fila(variables, valores):
    return valores[0] != valores[1]


def no_en_diagonal(variables, valores):
    fila_a = valores[0]
    columna_a = int(variables[0][1])
    fila_b = valores[1]
    columna_b = int(variables[1][1])

    return abs(fila_a - fila_b) != abs(columna_a - columna_b)


restricciones = []

for reina_a, reina_b in itertools.combinations(variables, 2):
    restricciones.append(((reina_a, reina_b), distinta_fila))
    restricciones.append(((reina_a, reina_b), no_en_diagonal))


problem = CspProblem(variables, dominios, restricciones)

print 'backtrack:'
result = backtrack(problem,
                   variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                   value_heuristic=LEAST_CONSTRAINING_VALUE,
                   inference=True)

print result


print 'min_conflicts:'
result = min_conflicts(problem, iterations_limit=100)

print result
