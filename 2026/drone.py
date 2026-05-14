from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    min_conflicts,
)

variables = ["BahiaDelantera", "BahiaTrasera", "Motores"]

domains = {
    "BahiaDelantera": ["BatAdicional", "CamResolucion", "Antena", "ParteFum"],
    "BahiaTrasera": ["BatAdicional", "CamTermica", "Antena", "ParteFum"],
    "Motores": ["MotPotente", "MotEficiente", "MotDuradero"]
}

WEIGHTS = {
    "BatAdicional": 3,
    "MotPotente": 1,
    "MotEficiente": 0.5,
    "MotDuradero": 1.2,
    "CamResolucion": 1.5,
    "CamTermica": 1,
    "Antena": 0.5,
    "ParteFum": 2,
}

constraints = []

# no repetir mejora

def different(variables, values):
    if values[0] == "ParteFum":
        return True
    else:
        return values[0] != values[1]

constraints.append(
    (("BahiaDelantera", "BahiaTrasera"), different)
)

# peso total <= 5kg

def peso_total(variables, values):
    m1, m2, m3 = values

    return WEIGHTS[m1] + WEIGHTS[m2] + WEIGHTS[m3] <= 5


constraints.append(
    (("BahiaDelantera", "BahiaTrasera", "Motores"), peso_total)
)


# los motores potentes requiren bateria adicional

def motores_potentes_requieren_bateria(variables, values):
    m_bd, m_bt, m_m = values

    if m_m == "MotPotente":
        return "BatAdicional" in (m_bd, m_bt)
    else:
        return True

constraints.append(
    (("BahiaDelantera", "BahiaTrasera", "Motores"), motores_potentes_requieren_bateria)
)

# los motores potentes son incompatibles con camara de mejor resolucion

def motores_potentes_vs_camara_resolucion(variables, values):
    m_m, m_bd = values

    if m_bd == "CamResolucion":
        return m_m != "MotPotente"
    else:
        return True

constraints.append(
    (("Motores", "BahiaDelantera"), motores_potentes_vs_camara_resolucion)
)

# sistema de fumigacion require 2 partes

def partes_fumigacion(variables, values):
    return values.count("ParteFum") in (0, 2)

constraints.append(
    (("BahiaDelantera", "BahiaTrasera"), partes_fumigacion)
)


problem = CspProblem(variables, domains, constraints)
#solution = backtrack(problem)
solution = min_conflicts(problem, iterations_limit=1000)

print(solution)
print("Peso total:", sum(WEIGHTS[m] for m in solution.values()))

