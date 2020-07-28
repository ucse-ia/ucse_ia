import itertools
from simpleai.search import CspProblem, backtrack, MOST_CONSTRAINED_VARIABLE, LEAST_CONSTRAINING_VALUE, HIGHEST_DEGREE_VARIABLE


variables = ['R' + str(num)
             for num in range(8)]

dominios = dict((variable, range(8))
                for variable in variables)


def diferentes(variables, valores):
    fila0, fila1 = valores

    return fila0 != fila1


def no_en_diagonal(variables, valores):
    fila0, fila1 = valores
    columna0, columna1 = [int(reina[1])
                          for reina in variables]

    dif_col = abs(columna0 - columna1)
    dif_fil = abs(fila0 - fila1)

    return dif_col != dif_fil


restricciones = []

for par in itertools.combinations(variables, 2):
    restricciones.append((par, diferentes))
    restricciones.append((par, no_en_diagonal))


csp = CspProblem(variables, dominios, restricciones)

resultado = backtrack(csp, inference=True,
                      variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                      value_heuristic=LEAST_CONSTRAINING_VALUE)

print resultado
