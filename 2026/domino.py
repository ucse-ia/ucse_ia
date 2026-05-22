from simpleai.search import (
    CspProblem,
    LEAST_CONSTRAINING_VALUE,
    MOST_CONSTRAINED_VARIABLE,
    backtrack,
)
from itertools import combinations

LARGO_CADENA = 10

# Variables: las posiciones donde van las fichas [1,2,3,4,...]
variables = list(range(LARGO_CADENA))

# Dominios: todas las fichas del domino
fichas_domino = []
# Por más que sean la misma ficha, planteamos como distintas a las fichas (x,y) e (y,x).
# Ejemplo: (1,2) <> (2,1). Esto para ahorrarnos la complejidad de representar la orientación.
for x in range(7):
    for y in range(7):
        fichas_domino += ((x,y),)

dominios = { var: list(fichas_domino) for var in variables }

# La primer pieza debe comenzar con 1.
# Esta restricción unaria se puede aplicar desde el dominio para reducir la búsqueda.
dominios[variables[0]] = [
    ficha for ficha in fichas_domino
    if ficha[0] == 1
]

# La última pieza debe terminar con 6.
# Nuevamente, se restringe el dominio en lugar de agregar una restricción unaria.
dominios[variables[-1]] = [
    ficha for ficha in fichas_domino
    if ficha[1] == 6
]

def diferentes(vars, vals):
    # Usando sorted incluimos los casos donde la ficha es la misma al revés.
    return sorted(vals[0]) != sorted(vals[1])

def no_suman_mas_de_15(vars, vals):
    suma = 0
    for val in vals:
        suma += val[0]
        suma += val[1]
    return suma <= 15

def mitades_adyacentes_tienen_mismo_numero(vars, vals):
    primera_mitad = vals[0][1]
    segunda_mitad = vals[1][0]
    return primera_mitad == segunda_mitad

restricciones = []

# Restricción all_dif (contemplando cambio de orientación):
for comb in combinations(variables, 2):
    restricciones.append((comb, diferentes))

for index in range(len(variables) - 1):
    # La suma de los números de dos piezas vecinas nunca puede superar 15
    restricciones.append(((variables[index], variables[index+1]), no_suman_mas_de_15))
    # En un camino de dominó válido dos piezas adyacentes comparten el mismo número en las mitades adyacentes
    restricciones.append(((variables[index], variables[index+1]), mitades_adyacentes_tienen_mismo_numero))

def resolver():
    domino = CspProblem(variables, dominios, restricciones)
    return backtrack(
        domino,
        variable_heuristic=MOST_CONSTRAINED_VARIABLE,
        value_heuristic=LEAST_CONSTRAINING_VALUE,
    )

def main():
    result = resolver()

    if result is None:
        print("No se encontró solución")
        return

    for variable in variables:
        print(result[variable])

if __name__ == "__main__":
    main()
