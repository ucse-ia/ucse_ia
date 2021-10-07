from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    HIGHEST_DEGREE_VARIABLE,
    MOST_CONSTRAINED_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)


problem_variables = ["mejora1", "mejora2", "mejora3"]

domains = {}
for variable in problem_variables:
    domains[variable] = [
        ("baterias", 12.5, 300),
        ("brazo", 60, 50),
        ("ventana", 100, 550),
        ("antena", 20, 30),
        ("exp_plantas", 80, 250),
        ("exp_fisicos", 75, 300),
        ("computadoras", 50, 20),
        ("reciclador", 30, 100),
    ]



constraints = []

def different(variables, values):
    improv1, improv2 = values
    return improv1 != improv2


for variable1, variable2 in combinations(problem_variables, 2):
    constraints.append(((variable1, variable2), different))


# restricción: suma de dinero (programada como restricción global, de 3 variables)

def money_is_enough(variables, values):
    total_cost = sum(improv[1] for improv in values)
    return total_cost <= 150


constraints.append((problem_variables, money_is_enough))

# restricción: suma de peso (programada como restricción global, de 3 variables)

def weight_is_enough(variables, values):
    total_weight = sum(improv[2] for improv in values)
    return total_weight <= 1000


constraints.append((problem_variables, weight_is_enough))

# restricción: no podemos elegir el laboratorio de plantas y el físico al mismo tiempo

domains["mejora2"].remove(("exp_fisicos", 75, 300))
domains["mejora2"].remove(("exp_plantas", 80, 250))

domains["mejora3"].remove(("exp_fisicos", 75, 300))
domains["mejora3"].remove(("exp_plantas", 80, 250))


# restricción: si están las computadoras, necesitamos que estén las baterías

def computers_require_batteries(variables, values):
    has_computers = "computadoras" in [improv[0] for improv in values]
    has_batteries = "baterías" in [improv[0] for improv in values]

    if has_computers:
        return has_batteries
    else:
        return True


constraints.append((problem_variables, computers_require_batteries))



problem = CspProblem(problem_variables, domains, constraints)
solution = backtrack(problem, variable_heuristic=HIGHEST_DEGREE_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)

print("Solution:")
print(solution)
