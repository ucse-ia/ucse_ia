# coding: utf-8
import itertools

from simpleai.search import (backtrack, CspProblem, LEAST_CONSTRAINING_VALUE,
                             min_conflicts, MOST_CONSTRAINED_VARIABLE)
N = 3
# las variables van a ser tuplas de forma <fila, columna>
variables = [(fila, columna) for fila in range(N) for columna in range(N)]
dominios = {var: range(1, (N**2)+1) for var in variables}


restricciones = []


def distinto_valor(variables, valores):
    'Compara que los valores de las variables sean distintos'
    return valores[0] != valores[1]


# Todas las variables tienen que tener valor distinto.
for var1, var2 in itertools.combinations(variables, 2):
    restricciones.append(((var1, var2), distinto_valor))


# Todas las filas y columnas deben sumar el mismo valor
def misma_suma(variables, valores):
    '''
    Controla que la suma de las primeras N variables sea igual a la suma de las
    segundas N variables.
    '''
    return sum(valores[:N]) == sum(valores[N:])

# Agregamos las restricciones necesarias para asegurar qeu todas las filas y
# columnas sumen lo mismo

filas = [tuple([(f, c) for c in range(N)]) for f in range(N)]
columnas = [tuple([(f, c) for f in range(N)]) for c in range(N)]
lineas = filas + columnas

for l1, l2 in itertools.combinations(lineas, 2):
    restricciones.append((l1+l2, misma_suma))

problem = CspProblem(variables, dominios, restricciones)

print 'backtrack:'
result = backtrack(problem,
                   variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                   value_heuristic=LEAST_CONSTRAINING_VALUE,
                   inference=True)


def imprime_cubo(cubo):
    for fila in range(N):
        for columna in range(N):
            print cubo[(fila, columna)],
        print ""

imprime_cubo(result)
