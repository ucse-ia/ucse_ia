import itertools

from simpleai.search import (CspProblem, backtrack, min_conflicts,
                             MOST_CONSTRAINED_VARIABLE, 
                             LEAST_CONSTRAINING_VALUE, 
                             HIGHEST_DEGREE_VARIABLE)


casillas = list('abcdefghij')

dominios = {casilla: range(-100, 101)
            for casilla in casillas}


dominios['a'] = [42, ]
dominios['c'] = [0, ]
dominios['d'] = [6, ]
dominios['h'] = [1, ]


def diferentes(variables, valores):
    return valores[0] != valores[1]


def suma_da_bien(variables, valores):
    return valores[0] == valores[1] + valores[2]


restricciones = []

for variable1, variable2 in itertools.combinations(casillas, 2):
    restricciones.append(((variable1, variable2), diferentes))

restricciones.append((('a', 'b', 'c'), suma_da_bien))
restricciones.append((('b', 'd', 'e'), suma_da_bien))
restricciones.append((('c', 'e', 'f'), suma_da_bien))
restricciones.append((('d', 'g', 'h'), suma_da_bien))
restricciones.append((('e', 'h', 'i'), suma_da_bien))
restricciones.append((('f', 'i', 'j'), suma_da_bien))



if __name__ == '__main__':
    problema = CspProblem(casillas, dominios, restricciones)

    resultado = backtrack(problema)
    print 'backtrack:'
    print resultado

    resultado = min_conflicts(problema, iterations_limit=500)
    print 'min conflicts:'
    print resultado
