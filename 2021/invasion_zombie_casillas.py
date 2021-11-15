import time
from datetime import datetime
from itertools import combinations
from pprint import pprint

from simpleai.search import MOST_CONSTRAINED_VARIABLE, CspProblem, backtrack


# Un par de funciones auxiliares
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
# En este archivo vamos a resolver el CSP usando las casillas como variables
# y los elementos como valores. (la forma no recomendable...)
###############################################################################

# Las variables son todas las posiciones
CASILLAS = [(f, c) for f in range(5) for c in range(5)]
ESQUINAS = [(0, 0), (4, 0), (0, 4), (4, 4)]

# Como una solucion tiene todas las variables con valor, tenemos que inventar
# un valor para los casilleros que no llevan nada. Lo vamos a denominar "vacio"
ELEMENTOS = ['zombie', 'pared', 'protagonista', 'zona_segura', 'vacio']

variables_problema = CASILLAS

dominios = {}
for variable in variables_problema:
    dominios[variable] = ELEMENTOS

restricciones = []


# Distinta posicion: no hace falta validar, toda variable va a tener un unico valor
# Lo que tenemos que chequear en esta version es que se respeten las cantidades de elementos...
def control_cantidad_de(elemento, cantidad):
    'funcion que usamos para crear funciones de restriccion'
    def la_restriccion(variables, values):
        cantidad_apariciones = 0
        for value in values:
            if value == elemento:
                cantidad_apariciones += 1
        return cantidad == cantidad_apariciones
    return la_restriccion


restricciones.append((variables_problema, control_cantidad_de('zombie', 5)))
restricciones.append((variables_problema, control_cantidad_de('pared', 7)))
restricciones.append((variables_problema, control_cantidad_de('protagonista', 1)))
restricciones.append((variables_problema, control_cantidad_de('zona_segura', 1)))


def zombies_no_amontonados(variables, values):
    """En cada llamada nos llega la casilla bajo estudio y luego las casillas adyacentes a la misma.
    Si la cailla bajo estudio es un zombie, entonces tenemos que contar cuantos adyacentes son
    zombies.
    """

    bajo_estudio, *elementos_adyacentes = values
    if bajo_estudio == 'zombie':
        cantidad_zombies_adyacentes = 0
        for e in elementos_adyacentes:
            if e == 'zombie':
                cantidad_zombies_adyacentes += 1
        return cantidad_zombies_adyacentes <= 2
    return True


for casilla in variables_problema:
    restricciones.append(([casilla] + adyacentes_de(casilla), zombies_no_amontonados))


def esquinas_opuestas(variables, values):
    """Chequeamos que en las esquinas opuestas esten la protagonista y la zonas segura
    """
    posiciones_de_interes = [pos
                             for pos, elem in zip(variables, values)
                             if elem in ('zona_segura', 'protagonista')]
    if len(posiciones_de_interes) != 2:
        # la protagonista y la zona_segura no estan en esquinas
        return False

    (f1, c1), (f2, c2) = posiciones_de_interes
    return (abs(f1 - f2) == 4) and (abs(c1 - c2) == 4)


restricciones.append((ESQUINAS, esquinas_opuestas))


def una_y_solo_una_pared(variables, values):
    "La primer variable es la esquina, el resto son las casillas adyacentes a la misma"
    esquina, *adyacentes = values
    if esquina != 'zona_segura':
        return True
    cantidad_paredes_adyacentes = 0
    for elemento in adyacentes:
        if elemento == 'pared':
            cantidad_paredes_adyacentes += 1
    return cantidad_paredes_adyacentes == 1


for esquina in ESQUINAS:
    scope = [esquina] + adyacentes_de(esquina)
    restricciones.append((scope, una_y_solo_una_pared))


def zona_segura_sin_zombies(variables, values):
    "La primer variable es la esquina, el resto son las casillas adyacentes a la misma"
    esquina, *adyacentes = values
    if esquina != 'zona_segura':
        return True
    for elemento in adyacentes:
        if elemento == 'zombie':
            return False
    return True


for esquina in ESQUINAS:
    scope = [esquina] + adyacentes_de(esquina)
    restricciones.append((scope, zona_segura_sin_zombies))


if __name__ == '__main__':
    invasion_problem = CspProblem(variables_problema, dominios, restricciones)
    inicio = datetime.now()
    solution = backtrack(invasion_problem, variable_heuristic=MOST_CONSTRAINED_VARIABLE)
    segundos = (datetime.now() - inicio).total_seconds()
    print(f"Tiempo total: {segundos}s")
    pprint(solution)
