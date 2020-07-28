# coding: utf-8
import itertools

from simpleai.search import (backtrack, CspProblem, LEAST_CONSTRAINING_VALUE,
                             min_conflicts, MOST_CONSTRAINED_VARIABLE)
N = 5
MAX_NUMBER = 8
# las variables van a ser tuplas de forma <fila, columna>
variables = [(fila, columna) for fila in range(N) for columna in range(N)]
dominios = {var: list(range(1, MAX_NUMBER + 1)) for var in variables}


restricciones = []


def distinto_valor(variables, valores):
    'Compara que los valores de las variables sean distintos'
    return valores[0] != valores[1]


# Todas las filas deben tener distintos valores
for fila in range(N):
    for col1, col2 in itertools.combinations(range(N), 2):
        var1 = (fila, col1)
        var2 = (fila, col2)
        restricciones.append(((var1, var2), distinto_valor))


# Todos los casilleros deben tener al menos dos vecinos con valor menor al propio
def al_menos_dos_menores(variables, valores):
    valor_casillero = valores[0]
    valores_vecinos = valores[1:]
    return len([x for x in valores_vecinos if x < valor_casillero]) >= 1


# Todos los casilleros deben tener al menos un vecino con valor igual o mayor al propio
def al_menos_un_mayor_o_igual(variables, valores):
    valor_casillero = valores[0]
    valores_vecinos = valores[1:]
    return len([x for x in valores_vecinos if x > valor_casillero]) >= 1


def vecinos_variable(variable):
    f, c = variable
    vecinos = []
    for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if 0 <= f + df < N and 0 <= c + dc < N:
            vecinos.append((f + df, c + dc))
    return vecinos


for variable in variables:
    vecinos = vecinos_variable(variable)
    if variable != (0, 0):
        restricciones.append(([variable] + vecinos, al_menos_dos_menores))
    if variable != (N - 1, N - 1):
        restricciones.append(([variable] + vecinos, al_menos_un_mayor_o_igual))


problem = CspProblem(variables, dominios, restricciones)


# result = backtrack(problem,
                   # variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                   # value_heuristic=LEAST_CONSTRAINING_VALUE,
                   # inference=True)

result = min_conflicts(problem, iterations_limit=1000)


def imprime_cubo(cubo):
    for fila in range(N):
        for columna in range(N):
            print(cubo[(fila, columna)], end="")
        print("")

imprime_cubo(result)
