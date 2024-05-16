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


N_REINAS = 100

variables = list(range(N_REINAS))

dominios = {
    reina: list(range(N_REINAS))
    for reina in variables
}

def que_no_se_ataquen(variables, values):
    reina1, reina2 = variables
    fila1, fila2 = values

    if fila1 == fila2:
        return False
    else:
        delta_filas = abs(fila1 - fila2)
        delta_cols = abs(reina1 - reina2)
        if delta_filas == delta_cols:
            return False

    return True


restricciones = []
for reina1, reina2 in combinations(variables, 2):
    restricciones.append(
        ((reina1, reina2), que_no_se_ataquen)
    )


problema = CspProblem(variables, dominios, restricciones)
# solucion = backtrack(problema,
                     # variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                     # value_heuristic=LEAST_CONSTRAINING_VALUE)
solucion = min_conflicts(problema, iterations_limit=3)

print(solucion)
conflicts = _find_conflicts(problema, solucion)
print("Ataques:", len(conflicts))
print(conflicts)
