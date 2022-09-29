from itertools import combinations

from simpleai.search import CspProblem, backtrack, MOST_CONSTRAINED_VARIABLE, LEAST_CONSTRAINING_VALUE, HIGHEST_DEGREE_VARIABLE


#   T W O
# + T W O
# --------
# F O U R

letras = ("T", "W", "O", "F", "U", "R")
acarreos = ("c1", "c2")
variables = letras + acarreos

dominios = {}
for letra in letras:
    dominios[letra] = list(range(10))
dominios["R"] = [0, 2, 4, 6, 8]
for variable in ("F", "c1", "c2"):
    dominios[variable] = [0, 1]

dominios["F"] = [1, ]

restricciones = []

# restriccion de que las letras sean todos digitos diferentes
# nos van a usar así: son_diferentes(("T", "W"), (2, 6))

def son_diferentes(variables, values):
    val1, val2 = values
    return val1 != val2

for v1, v2 in combinations(letras, 2):
    restricciones.append(
        ((v1, v2), son_diferentes)
    )

# restriccion la primer columna da bien (desde la derecha)
def primer_columna_bien(variables, values):
    val_o, val_r, val_c1 = values
    return val_o * 2 == val_c1 * 10 + val_r

restricciones.append(
    (("O", "R", "c1"), primer_columna_bien)
)

# restriccion la segunda columna da bien (desde la derecha)
def segunda_columna_bien(variables, values):
    val_w, val_u, val_c1, val_c2 = values
    return val_w * 2 + val_c1 == val_u + val_c2 * 10

restricciones.append(
    (("W", "U", "c1", "c2"), segunda_columna_bien)
)

# restriccion la tercer columna da bien (desde la derecha)
def tercer_columna_bien(variables, values):
    val_t, val_o, val_c2, val_f = values
    return val_t * 2 + val_c2 == val_f * 10 + val_o

restricciones.append(
    (("T", "O", "c2", "F"), tercer_columna_bien)
)


problema = CspProblem(variables, dominios, restricciones)

solucion = backtrack(
    problema,
    inference=False,
    variable_heuristic=MOST_CONSTRAINED_VARIABLE,
    value_heuristic=LEAST_CONSTRAINING_VALUE,
)

print(solucion)
