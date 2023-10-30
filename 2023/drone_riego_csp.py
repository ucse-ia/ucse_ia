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


# las variables son los slots de mejoras
variables = ['Mejora {}'.format(i) for i in range(3)]

mejoras = {
    'Motor': (300, 0),
    'Aspersor': (100, 100),
    'Estructura': (250, -150),
    'Tanque': (10, 300),
    'Sistema': (50, 100),
    'Bateria': (150, 200)
}
dominios = {mejora: list(mejoras.keys())
            for mejora in variables}

restricciones = []

# bateria y motor: si esta la bateria => tiene que estar motor
def bateria_y_motor(variables, valores):
    if 'Bateria' in valores:
        return 'Motor' in valores
    return True

# tanque y sistema no puede ir juntos
def tanque_y_sistema_incompatibles(variables, valores):
    return not('Tanque' in valores and 'Sistema' in valores)

# costo <= 450
def costo_total(variables, valores):
    return sum([mejoras[v][0] for v in valores]) <= 450

# peso <= 300
def peso_total_agregado(variables, valores):
    return sum([mejoras[v][1] for v in valores]) <= 300

# todos distintos
def distintos(variables, valores):
    return len(valores) == len(set(valores))

for mejora1, mejora2 in combinations(variables, 2):
    restricciones.append(((mejora1, mejora2), distintos))
    restricciones.append(((mejora1, mejora2), tanque_y_sistema_incompatibles))

restricciones.append((variables, bateria_y_motor))
restricciones.append((variables, costo_total))
restricciones.append((variables, peso_total_agregado))

problema = CspProblem(variables, dominios, restricciones)
solucion = backtrack(problema,
                     variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                     value_heuristic=LEAST_CONSTRAINING_VALUE)
# solucion = min_conflicts(problema)

print("Solución:")
print(solucion)
print(_find_conflicts(problema, solucion))
