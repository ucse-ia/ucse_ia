from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    min_conflicts,
    MOST_CONSTRAINED_VARIABLE,
    HIGHEST_DEGREE_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)
from simpleai.search.csp import _find_conflicts


N_REINAS = 1000

# las variables son las 8 reinas
variables = list(range(N_REINAS))

dominios = {reina: list(range(N_REINAS))
            for reina in variables}

restricciones = []

def no_se_atacan(variables, values):
    columna_reina1, columna_reina2 = variables
    fila_reina1, fila_reina2 = values

    if fila_reina1 == fila_reina2:
        return False

    dif_filas = abs(fila_reina1 - fila_reina2)
    dif_cols = abs(columna_reina1 - columna_reina2)
    if dif_filas == dif_cols:
        return False

    return True

for reina1, reina2 in combinations(variables, 2):
    restricciones.append(
        ((reina1, reina2), no_se_atacan)
    )


def jugar():
    problema = CspProblem(variables, dominios, restricciones)
    solucion = min_conflicts(problema)

    return solucion


if __name__ == "__main__":
    print("Resolviendo algo de ejemplo")
    problema = CspProblem(variables, dominios, restricciones)
    # solucion = backtrack(problema, variable_heuristic=MOST_CONSTRAINED_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)
    solucion = min_conflicts(problema)

    print("Solución:")
    print(solucion)
    print(_find_conflicts(problema, solucion))
