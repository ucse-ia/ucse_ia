from itertools import combinations
from simpleai.search import CspProblem, backtrack

arboles = ((0, 0), (0, 3), (1, 3), (2, 1), (3, 0))


def tiene_vecinos(posicion, posibles_vecinos):
    # recibe una posicion, y una lista de otras posiciones. Devuelve true si
    # alguna de las otras posiciones es vecina a la posicion pasada
    x1, y1 = posicion

    for posible in posibles_vecinos:
        x2, y2 = posible
        if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
            return True

    return False


# cada carpa es una variable
variables = 'carpa1', 'carpa2', 'carpa3', 'carpa4'

# armo una lista con todas las posiciones en las que puede ir una carpa, ya
# sacando las posiciones de los arboles, porque no pueden ir ahi, y sacando
# las pociciones que no tienen ningun arbol vecino, porque las carpas tienen
# que estar vecinas a algun arbol
posiciones = [(x, y)
              for x in range(4)
              for y in range(4)
              if (x, y) not in arboles and tiene_vecinos((x, y), arboles)]

# los valores posibles para cada carpa, son las posiciones disponibles
domains = {variable: posiciones[:] for variable in variables}


def carpas_no_estan_vecinas(variables, values):
    # restriccion binaria, chequea dos carpas:
    # asegurarse de que no estan vecinas
    return not tiene_vecinos(values[0], (values[1],))


def carpas_estan_en_diferentes_posiciones(variables, values):
    # restriccion binaria, chequea dos carpas:
    # asegurarse de que no estan en la misma posicion
    return values[0] != values[1]


constrains = []
for variable1, variable2 in combinations(variables, 2):
    # por cada par de carpas, hace falta mirar que no sean vecinas y que no
    # esten en la misma posicion
    constrains.append(((variable1, variable2), carpas_estan_en_diferentes_posiciones))
    constrains.append(((variable1, variable2), carpas_no_estan_vecinas))


problema = CspProblem(variables, domains, constrains)
result = backtrack(problema)

print result
