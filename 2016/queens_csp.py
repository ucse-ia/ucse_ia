import itertools

from simpleai.search import (CspProblem, backtrack, min_conflicts,
                             MOST_CONSTRAINED_VARIABLE, 
                             LEAST_CONSTRAINING_VALUE, 
                             HIGHEST_DEGREE_VARIABLE)

REINAS = 8


reinas = ['r' + str(numero) for numero in range(REINAS)]

dominios = {reina: range(REINAS) for reina in reinas}


def no_en_misma_fila(variables, values):
    fila_a, fila_b = values

    # misma fila?
    return fila_a != fila_b


def no_en_diagonal(variables, values):
    reina_a, reina_b = variables
    fila_a, fila_b = values
    columna_a = int(reina_a[1])
    columna_b = int(reina_b[1])

    # en diagonal?
    if abs(columna_a - columna_b) == abs(fila_a - fila_b):
        return False

    return True



restricciones = []


for reina_a, reina_b in itertools.combinations(reinas, 2):
    restricciones.append(
        ((reina_a, reina_b), no_en_misma_fila)
    )

    restricciones.append(
        ((reina_a, reina_b), no_en_diagonal)
    )


def imprimir(resultado):
    for fila in range(REINAS):
        for reina in reinas:
            if resultado[reina] == fila:
                print '|#',
            else:
                print '| ',
        print
        print '+--' * REINAS


if __name__ == '__main__':
    problema = CspProblem(reinas, dominios, restricciones)

    resultado = backtrack(problema)
    print 'backtrack:'
    imprimir(resultado)

    resultado = min_conflicts(problema, iterations_limit=10)
    print 'min conflicts:'
    imprimir(resultado)
