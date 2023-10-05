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


variables = [
    (fila, col)
    for fila in range(9)
    for col in range(9)
]

dominios = {
    casilla: list(range(1, 10))
    for casilla in variables
}

dominios[(0, 2)] = [3]
dominios[(0, 4)] = [2]
dominios[(0, 6)] = [6]
dominios[(1, 0)] = [9]
dominios[(1, 3)] = [3]
dominios[(1, 5)] = [5]
dominios[(1, 8)] = [1]
dominios[(2, 2)] = [1]
dominios[(2, 3)] = [8]
dominios[(2, 5)] = [6]
dominios[(2, 6)] = [4]
dominios[(3, 2)] = [8]
dominios[(3, 3)] = [1]
dominios[(3, 5)] = [2]
dominios[(3, 6)] = [9]
dominios[(4, 0)] = [7]
dominios[(4, 8)] = [8]
dominios[(5, 2)] = [6]
dominios[(5, 3)] = [7]
dominios[(5, 5)] = [8]
dominios[(5, 6)] = [2]
dominios[(6, 2)] = [2]
dominios[(6, 3)] = [6]
dominios[(6, 5)] = [9]
dominios[(6, 6)] = [5]
dominios[(7, 0)] = [8]
dominios[(7, 3)] = [2]
dominios[(7, 5)] = [3]
dominios[(7, 8)] = [9]
dominios[(8, 2)] = [5]
dominios[(8, 4)] = [1]
dominios[(8, 6)] = [3]

restricciones = []

def diferentes(variables, values):
    n1, n2 = values
    return n1 != n2


# pares de casillas en la misma fila
for fila in range(9):
    casillas_fila = [(fila, col) for col in range(9)]
    for casilla1, casilla2 in combinations(casillas_fila, 2):
        restricciones.append(
            ((casilla1, casilla2), diferentes)
        )

# pares de casillas en la misma columna
for col in range(9):
    casillas_col = [(fila, col) for fila in range(9)]
    for casilla1, casilla2 in combinations(casillas_col, 2):
        restricciones.append(
            ((casilla1, casilla2), diferentes)
        )

# armamos un dict que tiene por cada cuadrante "grande", los casilleros que contiene
cuadrantes = {}
for fila, col in variables:
    cuadrante = int(fila / 3), int(col / 3)

    if cuadrante not in cuadrantes:
        cuadrantes[cuadrante] = []

    cuadrantes[cuadrante].append((fila, col))

# pares de casillas en el mismo cuadrante
for casillas_cuadrante in cuadrantes.values():
    for casilla1, casilla2 in combinations(casillas_cuadrante, 2):
        restricciones.append(
            ((casilla1, casilla2), diferentes)
        )



problema = CspProblem(variables, dominios, restricciones)
solucion = backtrack(problema, variable_heuristic=MOST_CONSTRAINED_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)

print("Solución:")
print(solucion)

for fila in range(9):
    for col in range(9):
        print(solucion[(fila, col)], end=" ")
    print()

#print(_find_conflicts(problema, solucion))
