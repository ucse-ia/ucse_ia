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


variables = ["mastil", "interno1", "interno2", "frente"]
dominios = {
    "mastil": ["taladro", "camara", "laser", "microscopio", "antena"],
    "interno1": ["bateria", "navegacion", "muestras", "antena"],
    "interno2": ["bateria", "navegacion", "muestras", "antena"],
    "frente": ["taladro", "laser", "microscopio", "muestras"],
}

PESOS = {
    "taladro": 15,
    "camara": 3,
    "laser": 5,
    "microscopio": 3,
    "antena": 7,
    "bateria": 10,
    "navegacion": 8,
    "muestras": 5,
}

restricciones = []

def diferentes(variables, values):
    m1, m2 = values
    return m1 != m2

for slot1, slot2 in combinations(variables, 2):
    restricciones.append(
        ((slot1, slot2), diferentes)
    )

def peso_total_ok(variables, values):
    return sum(PESOS[mejora] for mejora in values) <= 25

restricciones.append((variables, peso_total_ok))


def antena_bateria_incompatibles(variables, values):
    posible_antena, posible_bateria = values
    return not (posible_antena == "antena" and posible_bateria == "bateria")

for lugar_posible_antena in ("mastil", "interno1", "interno2"):
    for lugar_posible_bateria in ("interno1", "interno2"):
        if lugar_posible_bateria != lugar_posible_antena:
            restricciones.append(
                ((lugar_posible_antena, lugar_posible_bateria), antena_bateria_incompatibles)
            )


def laser_necesita_bateria(variables, values):
    posible_laser = values[0]
    posibles_baterias = values[1:]

    if posible_laser == "laser":
        return "bateria" in posibles_baterias
    else:
        return True


for lugar_posible_laser in ("mastil", "frente"):
    restricciones.append(
        ((lugar_posible_laser, "interno1", "interno2"), laser_necesita_bateria)
    )


def microscopio_taladro_incompatibles(variables, values):
    posible_microscopio, posible_taladro = values
    return not (posible_microscopio == "microscopio" and posible_taladro == "taladro")

for lugar_posible_microscopio in ("mastil", "frente"):
    for lugar_posible_taladro in ("mastil", "frente"):
        if lugar_posible_microscopio != lugar_posible_taladro:
            restricciones.append(
                ((lugar_posible_microscopio, lugar_posible_taladro), microscopio_taladro_incompatibles)
            )

MEJORAS_CIENCIA = "taladro", "microscopio", "laser", "muestra"

def necesitamos_ciencia(variables, values):
    for mejora in values:
        if mejora in MEJORAS_CIENCIA:
            return True

    return False

restricciones.append((variables, necesitamos_ciencia))


problema = CspProblem(variables, dominios, restricciones)
solucion = backtrack(problema)

print("Solución:")
print(solucion)

peso_total = sum(PESOS[mejora] for mejora in solucion.values())
print("Peso total:", peso_total)
