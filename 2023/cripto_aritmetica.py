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

letras = ["T", "W", "O", "F", "U", "R"]
acarreos = ["c1", "c2"]

variables = letras + acarreos

dominios = {
    letra: list(range(1, 10))
    for letra in letras
}
for variable in ("c1", "c2", "F"):
    dominios[variable] = [0, 1]

dominios["F"] = [1]


restricciones = []

def diferentes(variables, values):
    n1, n2 = values
    return n1 != n2

for letra1, letra2 in combinations(letras, 2):
    restricciones.append(
        ((letra1, letra2), diferentes)
    )

def primer_columna(variables, values):
    O, R, c1 = values
    return O * 2 == R + c1 * 10

restricciones.append((("O", "R", "c1"), primer_columna))


def segunda_columna(variables, values):
    W, U, c1, c2 = values
    return W * 2 + c1 == U + c2 * 10

restricciones.append((("W", "U", "c1", "c2"), segunda_columna))


def tercer_columna(variables, values):
    T, O, c2, F = values
    return T * 2 + c2 == O + F * 10

restricciones.append((("T", "O", "c2", "F"), tercer_columna))



problema = CspProblem(variables, dominios, restricciones)
solucion = backtrack(problema)

print("Solución:")
print(solucion)
