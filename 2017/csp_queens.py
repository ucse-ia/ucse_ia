import itertools

from simpleai.search import (CspProblem, backtrack, min_conflicts,
                             MOST_CONSTRAINED_VARIABLE,
                             LEAST_CONSTRAINING_VALUE,
                             HIGHEST_DEGREE_VARIABLE)


variables = list(range(8))
dominios = {n: list(range(8))
            for n in range(8)}

restricciones = [
]

def no_en_misma_fila(variables, values):
    fila_1, fila_2 = values
    return fila_1 != fila_2


def no_en_diagonal(variables, values):
    col_1, col_2 = variables
    fila_1, fila_2 = values
    return abs(fila_1 - fila_2) != abs(col_1 - col_2)



for reina_1, reina_2 in itertools.combinations(variables, 2):
    restricciones.append(((reina_1, reina_2), no_en_misma_fila))
    restricciones.append(((reina_1, reina_2), no_en_diagonal))


problema = CspProblem(variables, dominios, restricciones)
resultado = backtrack(problema, value_heuristic=LEAST_CONSTRAINING_VALUE,
                      variable_heuristic=MOST_CONSTRAINED_VARIABLE)
# resultado = min_conflicts(problema, iterations_limit=2)

print(resultado)
