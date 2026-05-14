from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    min_conflicts,
)

#   c2 c1
#    T W O
# +  T W O
# -----------
#  F O U R

variables = [
    "T", "W", "O", "F", "U", "R", "c1", "c2"
]

domains = {
    letter: list(range(10))
    for letter in ("T", "W", "O", "U", "R")
}
for letter in ("c1", "c2"):
    domains[letter] = [0, 1]

domains["F"] = [1]

constraints = []


# r1: all diff

def different(variables, values):
    return values[0] != values[1]

for var1, var2 in combinations(("T", "W", "O", "F", "U", "R"), 2):
    constraints.append(
        ((var1, var2), different)
    )

# r2: la primer columna debe sumar bien

def primer_columna_ok(variables, values):
    o, r, c1 = values
    return o * 2 == r + c1 * 10


constraints.append(
    (("O", "R", "c1"), primer_columna_ok)
)

# r3: la segunda columna debe sumar bien

def segunda_columna_ok(variables, values):
    c1, w, u, c2 = values
    return w * 2 + c1 == u + 10 * c2

constraints.append(
    (("c1", "W", "U", "c2"), segunda_columna_ok)
)

# r4: la tercer columna debe sumar bien

def tercera_columna_ok(variables, values):
    c2, t, o, f = values
    return t * 2 + c2 == o + 10 * f

constraints.append(
    (("c2", "T", "O", "F"), tercera_columna_ok)
)


problem = CspProblem(variables, domains, constraints)
#solution = backtrack(problem)
solution = min_conflicts(problem, iterations_limit=1000)

print(solution)
