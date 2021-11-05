import time
from datetime import datetime
from itertools import combinations

from simpleai.search import MOST_CONSTRAINED_VARIABLE, CspProblem, backtrack


# Un par de funciones auxiliares
def son_adyacentes(variables):
    "dada una tupla de dos variables devuelve si las mismas son adyacentes"
    v1, v2 = variables
    distancia = abs(v1[0] - v2[0]) + abs(v1[1] - v2[1])
    return distancia == 1


def adyacentes_de(variable):
    "Dada una variable, devuelve todas las variables adyacentes a la misma"
    adyacentes = []
    fila, columna = variable
    for df, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nf = fila + df
        nc = columna + dc
        if 0 <= nf <= 4 and 0 <= nc <= 4:
            adyacentes.append((nf, nc))
    return adyacentes


def imprimir_solucion(solucion, titulo, segundos):
    print(f"Solution {titulo} encontrada en {segundos} segundos:")
    for fila in range(5):
        for columna in range(5):
            print(solucion[(fila, columna)][0], end="")
        print("")


# Las variables son todas las posiciones
variables_problema = [(fila, columna)
                      for fila in range(5)
                      for columna in range(5)]

# Los dominios son los tipos de casilleros, aunque podemos evitar
# las veredas en la fila Norte
dominios = {}
for variable in variables_problema:
    f, _ = variable
    if f == 0:
        dominios[variable] = ["espacio_verde", "arboles", "nidos", "juegos", "vereda"]
    else:
        dominios[variable] = ["espacio_verde", "arboles", "nidos", "juegos"]


def no_mas_veredas_que_espacios_verdes_y_arboles(variables, values):
    cantidad_verdes = 0
    cantidad_grises = 0
    for v in values:
        if v in ["espacio_verde", "arboles"]:
            cantidad_verdes += 1
        elif v == "vereda":
            cantidad_grises += 1
    return cantidad_verdes >= cantidad_grises


def no_nidos_y_vereda_o_juego_juntos(variables, values):
    """si las variables son adyacentes, entonces hay que chequear que las asignaciones
    no sean nidos y (vereda o juego)
    """
    if son_adyacentes(variables):
        if "nidos" in values and ("vereda" in values or "juegos" in values):
            return False
    return True


def contenido_distinto_en_adyacentes(variables, values):
    """si las variables son adyacentes, entonces hay que chequear que las asignaciones
    no sean nidos y (vereda o juego)
    """
    if son_adyacentes(variables):
        # con set eliminamos duplicados, si los valores son iguales el largo seria de 1
        return len(set(values)) == 2
    return True


def arboles_al_norte_de_vereda(variables, values):
    "si una variable está al sur de la otra y tiene vereda, en la otra debe haber un arbol"
    v0, v1 = variables
    if v0[0] == v1[0] + 1:
        contenido_norte = values[0]
        contenido_sur = values[1]
    elif v0[0] == v1[0] - 1:
        contenido_norte = values[1]
        contenido_sur = values[0]
    else:
        # Nada que comparar, la restriccion no se viola porque no hay
        # una de las variables al norte de la otra
        return True
    return contenido_norte == "arbol" or contenido_sur != "vereda"


# creamos las restricciones de a pares de variebles a sabiendas que no es el mejor approach
restricciones = []
restricciones.append((variables_problema, no_mas_veredas_que_espacios_verdes_y_arboles))
for vars_ in combinations(variables_problema, 2):
    restricciones.append((vars_, no_nidos_y_vereda_o_juego_juntos))
    restricciones.append((vars_, contenido_distinto_en_adyacentes))
    restricciones.append((vars_, arboles_al_norte_de_vereda))


# creamos las restricciones de una manera más optima
restricciones_eficientes = []
restricciones_eficientes.append((variables_problema, no_mas_veredas_que_espacios_verdes_y_arboles))

for variable in variables_problema:
    # para los nidos y contenido distinto debemos generar solo los adyacentes de variable
    for v2 in adyacentes_de(variable):
        restricciones_eficientes.append(((variable, v2), no_nidos_y_vereda_o_juego_juntos))
        restricciones_eficientes.append(((variable, v2), contenido_distinto_en_adyacentes))

    # para el caso de los arboles y veredas solo debemos generar los pares donde las casillas
    # estan adyacentes verticalmente. Lo podemos lograr agregando la variable y la que esta debajo
    # total la restriccion contempla el ambos ordenes
    if variable[0] < 4:  # evitamos la ultima fila
        variable_al_sur = (variable[0] + 1, variable[1])
        restricciones_eficientes.append(((variable, variable_al_sur), arboles_al_norte_de_vereda))


if __name__ == '__main__':
    # probamos con las restricciones menos eficientes y mas eficientes para comparar
    nagai_problem = CspProblem(variables_problema, dominios, restricciones)
    inicio = datetime.now()
    solution = backtrack(nagai_problem, variable_heuristic=MOST_CONSTRAINED_VARIABLE)
    segundos = (datetime.now() - inicio).total_seconds()
    imprimir_solucion(solution, "no eficiente", segundos)

    alecto_problem = CspProblem(variables_problema, dominios, restricciones_eficientes)
    inicio = datetime.now()
    solution = backtrack(alecto_problem, variable_heuristic=MOST_CONSTRAINED_VARIABLE)
    segundos = (datetime.now() - inicio).total_seconds()
    imprimir_solucion(solution, "eficiente", segundos)
