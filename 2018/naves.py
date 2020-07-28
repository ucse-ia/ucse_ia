import itertools

from simpleai.search import (CspProblem, backtrack, min_conflicts,
                             MOST_CONSTRAINED_VARIABLE,
                             LEAST_CONSTRAINING_VALUE,
                             HIGHEST_DEGREE_VARIABLE)
INTERCONECTADAS = {
    1: [2, 3],
    2: [1, 3],
    3: [2, 1],
    4: [],
    5: [6],
    6: [5],
    7: [8],
    8: [7],
}

variables = list(range(1, 9))

posiciones_disponibles = {
    'motor': [7, 8],
    'ocultamiento': [1, 2, 3, 5],
    'apuntamiento': [1, 2, 3, 4],
    'torpedos': [1, 2],
    'medica': [5, 6, 7, 8],
    'mejorada': [5, 6],
    'escudo': variables,
    'comunicacion': variables,
    'evasion': [7, 8]
}

dominios = {}

for mejora, posiciones in posiciones_disponibles.items():
    for pos in posiciones:
        if pos in dominios:
            dominios[pos].append(mejora)
        else:
            dominios[pos] = [mejora]


def motor_u_ocultamiento(vars, vals):
    return not('motor' in vals and 'ocultamiento' in vals)


def torpedos_apuntamiento(vars, vals):
    if 'torpedos' in vals and 'apuntamiento' in vals:
        var1, var2 = vars
        if var2 not in INTERCONECTADAS[var1]:
            return False
    return True


def distintos(vars, vals):
    return len(set(vals)) == len(vals)


def escudo_comunicaciones(vars, vals):
    if 'escudo' in vals and 'comunicacion' in vals:
        var1, var2 = vars
        if var1 in INTERCONECTADAS[var2]:
            return False
    return True


restricciones = []

for pos1, pos2 in itertools.combinations(variables, 2):
    restricciones.append(((pos1, pos2), motor_u_ocultamiento))
    restricciones.append(((pos1, pos2), torpedos_apuntamiento))
    restricciones.append(((pos1, pos2), distintos))
    restricciones.append(((pos1, pos2), escudo_comunicaciones))


problema = CspProblem(variables, dominios, restricciones)
# resultado = backtrack(problema, value_heuristic=LEAST_CONSTRAINING_VALUE,
                      # variable_heuristic=MOST_CONSTRAINED_VARIABLE)
resultado = min_conflicts(problema)
print(resultado)
