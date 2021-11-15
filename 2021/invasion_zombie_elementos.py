import time
from datetime import datetime
from itertools import combinations
from pprint import pprint

from simpleai.search import MOST_CONSTRAINED_VARIABLE, CspProblem, backtrack


def son_adyacentes(casillas):
    "dada una tupla de dos casillas devuelve si las mismas son adyacentes"
    v1, v2 = casillas
    distancia = abs(v1[0] - v2[0]) + abs(v1[1] - v2[1])
    return distancia == 1


def adyacentes_de(casilla):
    "Dada una casilla, devuelve todas las casillas adyacentes a la misma"
    adyacentes = []
    fila, columna = casilla
    for df, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nf = fila + df
        nc = columna + dc
        if 0 <= nf <= 4 and 0 <= nc <= 4:
            adyacentes.append((nf, nc))
    return adyacentes


###############################################################################
# En este archivo vamos a resolver el CSP usando los elementos como variables
# y las casillas como valores.
###############################################################################

# Las variables son todas las posiciones
ZOMBIES = [f'zombie_{i}' for i in range(5)]
PAREDES = [f'pared_{i}' for i in range(7)]
PROTAGONISTA = 'protagonista'
ZONA_SEGURA = 'zona_segura'

CASILLAS = [(f, c) for f in range(5) for c in range(5)]
ESQUINAS = [(0, 0), (4, 0), (0, 4), (4, 4)]

variables_problema = ZOMBIES + PAREDES + [PROTAGONISTA, ZONA_SEGURA]

dominios = {}
for variable in variables_problema:
    dominios[variable] = CASILLAS

dominios[PROTAGONISTA] = ESQUINAS
dominios[ZONA_SEGURA] = ESQUINAS

restricciones = []


def distinta_posicion(variables, values):
    return len(values) == len(set(values))


for v1, v2 in combinations(variables_problema, 2):
    restricciones.append(((v1, v2), distinta_posicion))


def zombies_no_amontonados(variables, values):
    """Las variables son todos los zombies.
    Por cada zombie contamos la cantidad de adyacentes, si superan los 2 permitidos
    devolvemos False"""
    for zombie in values:
        cantidad_adyacentes = 0
        for otro_zombie in values:
            if zombie != otro_zombie and son_adyacentes([zombie, otro_zombie]):
                cantidad_adyacentes += 1
        if cantidad_adyacentes > 2:
            return False
    return True


restricciones.append((ZOMBIES, zombies_no_amontonados))


def esquinas_opuestas(variables, values):
    """Chequea que las dos variables esten en esquinas opuestas. Esto pasa cuando la distancia
    es 4 en filas y columnas.
    """
    (f1, c1), (f2, c2) = values
    return (abs(f1 - f2) == 4) and (abs(c1 - c2) == 4)


restricciones.append(((PROTAGONISTA, ZONA_SEGURA), esquinas_opuestas))


def una_y_solo_una_pared(variables, values):
    "La primer variable es la zona segura, el resto son las paredes"
    zona_segura, *paredes = values
    cantidad_paredes_adyacentes = 0
    for pared in paredes:
        if son_adyacentes([zona_segura, pared]):
            cantidad_paredes_adyacentes += 1
    return cantidad_paredes_adyacentes == 1


restricciones.append(([ZONA_SEGURA] + PAREDES, una_y_solo_una_pared))


def zona_segura_sin_zombies(variables, values):
    "La primer variable es la zona segura, el resto los zombies"
    zona_segura, *zombies = values
    for zombie in zombies:
        if son_adyacentes([zona_segura, zombie]):
            return False
    return True


restricciones.append(([ZONA_SEGURA] + ZOMBIES, zona_segura_sin_zombies))


if __name__ == '__main__':
    invasion_problem = CspProblem(variables_problema, dominios, restricciones)
    inicio = datetime.now()
    solution = backtrack(invasion_problem, variable_heuristic=MOST_CONSTRAINED_VARIABLE)
    segundos = (datetime.now() - inicio).total_seconds()
    print(f"Tiempo total: {segundos}s")
    pprint(solution)
