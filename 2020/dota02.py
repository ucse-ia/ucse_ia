from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    min_conflicts,
    MOST_CONSTRAINED_VARIABLE,
    HIGHEST_DEGREE_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)
from simpleai.search.csp import convert_to_binary


variables = ['slot_a', 'slot_b', 'slot_c']

dominios = {}

for variable in ('slot_b', 'slot_c'):
    dominios[variable] = [
        'assault cuirass',
        'battlefury',
        'cloak',
        'hyperstone',
        'quelling blade',
        'shadow blade',
        'veil of discord',
    ]

dominios['slot_a'] = ['battlefury', 'veil of discord']


COSTOS = {
    'assault cuirass': 5000,
    'battlefury': 4000,
    'cloak': 500,
    'hyperstone': 2000,
    'quelling blade': 200,
    'shadow blade': 3000,
    'veil of discord': 2000,
}


restricciones = []

def sumar_items(variables, values):
    costo_total = sum(COSTOS[item] for item in values)

    return costo_total <= 6000

restricciones.append(
    (('slot_a', 'slot_b', 'slot_c'), sumar_items),
)


def hyperstone_no_con_shadow_blade(variables, values):
    # {bla, ble} es un set (no es un diccionario!!)
    mala_combinacion = {'hyperstone', 'shadow blade'}
    return set(values) != mala_combinacion


def quelling_blade_no_con_shadow_blade(variables, values):
    # {bla, ble} es un set (no es un diccionario!!)
    mala_combinacion = {'quelling blade', 'shadow blade'}
    return set(values) != mala_combinacion


def cloak_no_con_veil(variables, values):
    # {bla, ble} es un set (no es un diccionario!!)
    mala_combinacion = {'cloak', 'veil of discord'}
    return set(values) != mala_combinacion


def diferentes(variables, values):
    item1, item2 = values
    return item1 != item2


for variable1, variable2 in combinations(variables, 2):
    restricciones.extend([
        ((variable1, variable2), hyperstone_no_con_shadow_blade),
        ((variable1, variable2), quelling_blade_no_con_shadow_blade),
        ((variable1, variable2), cloak_no_con_veil),
        ((variable1, variable2), diferentes),
    ])


problema = CspProblem(variables, dominios, restricciones)
# result = backtrack(problema)
result = min_conflicts(problema, iterations_limit=100)

print(result)
