from simpleai.search import CspProblem, backtrack, min_conflicts, MOST_CONSTRAINED_VARIABLE, HIGHEST_DEGREE_VARIABLE, LEAST_CONSTRAINING_VALUE

cantidad_reinas = 8

reinas = range(cantidad_reinas)

dominios = dict([(reina, range(cantidad_reinas))
                 for reina in reinas])

def diferentes(variables, valores):
    return len(valores) == len(set(valores))

def no_en_diagonal(variables, valores):
    x1, x2 = variables
    y1, y2 = valores

    return abs(x1 - x2) != abs(y1 - y2)


restricciones = [
    (reinas, diferentes),
]

for reina in reinas:
    for reina2 in reinas[reina + 1:]:
        restricciones.append(((reina, reina2), no_en_diagonal))


problema = CspProblem(reinas, dominios, restricciones)

result = backtrack(problema,
                   variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                   value_heuristic=LEAST_CONSTRAINING_VALUE,
                   inference=True)

#result = min_conflicts(problema, iterations_limit=100)

print result

