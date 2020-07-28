import itertools

from simpleai.search import (CspProblem, backtrack, min_conflicts,
                             MOST_CONSTRAINED_VARIABLE,
                             LEAST_CONSTRAINING_VALUE,
                             HIGHEST_DEGREE_VARIABLE)


variables = ['p' + str(n)
             for n in range(1, 9)]

modules = ['motor', 'ocultamiento', 'apuntamiento', 'torpedos', 'medica', 'evasion', 'carga',
           'escudo', 'comunicaciones']

domains = {pos: modules[:]
           for pos in variables}


constraints = []

front_side = 'p1', 'p2', 'p3', 'p5'
back_side = 'p7', 'p8'
front_exposed_side = 'p1', 'p2', 'p3', 'p4'
tips_side = 'p1', 'p2'
habitable_side = 'p5', 'p6', 'p7', 'p8'
not_exposed = 'p5', 'p6'

connected_groups = (
    ('p1', 'p2', 'p3'),
    ('p5', 'p6'),
    ('p7', 'p8'),
)


# El nuevo motor de salto a velocidad de la luz solo puede ubicarse en la parte trasera de la nave (p7, p8).

for pos in variables:
    if pos not in back_side:
        domains[pos].remove('motor')

# El nuevo sistema de ocultamiento debe instalarse en el sector delantero de la nave pero no en la cabina (es decir, en p1, p2, p3 o p5).

for pos in variables:
    if pos not in front_side:
        domains[pos].remove('ocultamiento')

# El nuevo sistema de ocultamiento no es compatible con el nuevo motor, por lo que solo puede instalarse una de estas dos mejoras, no ambas.

def check_motor_vs_ocultamiento(variables, values):
    value_front, value_back = values
    return not (value_back == 'motor' and value_front == 'ocultamiento')

for front_pos in front_side:
    for back_pos in back_side:
        constraints.append(((front_pos, back_pos), check_motor_vs_ocultamiento))

# El nuevo sistema de apuntamiento de armas debe ubicarse en alguna posición delantera y expuesta para poder ser utilizado: p1, p2, p3 o p4.

for pos in variables:
    if pos not in front_exposed_side:
        domains[pos].remove('apuntamiento')

# El nuevo lanzador de torpedos de protones solo puede instalarse en las posiciones p1 o p2, y debe ser una posición interconectada (lineas negras en el diagrama) con el nuevo sistema de apuntamiento.

for pos in variables:
    if pos not in tips_side:
        domains[pos].remove('torpedos')

def check_interconnection_torpedos(variables, values):
    if 'torpedos' in values:
        return 'apuntamiento' in values
    else:
        return True

constraints.append((connected_groups[0], check_interconnection_torpedos))

# Existe solo un equipo disponible de cada tipo de mejora, por lo que no se puede instalar la misma mejora en dos posiciones al mismo tiempo.

def different(variables, values):
    val1, val2 = values
    return val1 != val2

for pos1, pos2 in itertools.combinations(variables, 2):
    constraints.append(((pos1, pos2), different))

# La nueva bahía médica solo puede ubicarse en zonas habitables y seguras: p5, p6, p7 o p8.

for pos in variables:
    if pos not in habitable_side:
        domains[pos].remove('medica')

# El nuevo sistema de evasión solo puede ubicarse en las zonas de motores, p7 o p8.

for pos in variables:
    if pos not in back_side:
        domains[pos].remove('evasion')

# La bahía de carga mejorada no debe instalarse en zonas expuestas, por lo que debe estar en p5 o p6.

for pos in variables:
    if pos not in not_exposed:
        domains[pos].remove('carga')

# Finalmente, el escudo mejorado y el nuevo sistema de comunicaciones, no deben encontrarse en posiciones interconectadas, por la interferencia que genera el escudo.

def not_comunicaciones_con_escudo(variables, values):
    return set(values) != set(('escudo', 'comunicaciones'))

for group in connected_groups:
    for pos1, pos2 in itertools.combinations(group, 2):
        constraints.append(((pos1, pos2), not_comunicaciones_con_escudo))


result = backtrack(CspProblem(variables, domains, constraints))
print(result)
