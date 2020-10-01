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

#  A4 A3 A2 A1
#     S  E  N  D
#  +  M  O  R  E
# ---------------
#  M  O  N  E  Y

variables = 'S E N D M O R Y A1 A2 A3 A4'.split()

normal_letters = 'S E N D M O R Y'.split()

domains = {}
for normal_letter in normal_letters:
    domains[normal_letter] = list(range(10))


for carry in 'A1 A2 A3 A4'.split():
    domains[carry] = [0, 1]


constraints = []


def different_digits(variables, values):
    # variables = ('S', 'E')
    # values = (3, 8)
    value1, value2 = values

    return value1 != value2


for normal_letter1, normal_letter2 in combinations(normal_letters, 2):
    constraints.append(
        ((normal_letter1, normal_letter2), different_digits)
    )


def first_column_works(variables, values):
    d, e, y, a1 = values

    return d + e == a1 * 10 + y


constraints.append((('D', 'E', 'Y', 'A1'), first_column_works))

def other_column_works(variables, values):
    letter1, letter2, previous_carry, result_letter, result_carry = values

    return letter1 + letter2 + previous_carry == 10 * result_carry + result_letter


constraints.append((('N', 'R', 'A1', 'E', 'A2'), other_column_works))
constraints.append((('E', 'O', 'A2', 'N', 'A3'), other_column_works))
constraints.append((('S', 'M', 'A3', 'O', 'A4'), other_column_works))


def equals(variables, values):
    value1, value2 = values
    return value1 == value2

constraints.append((('M', 'A4'), equals))

print('Variables:', variables)
print('Domains:', domains)

problem = CspProblem(variables, domains, constraints)

print('Solving with backtracking')
result_bt = backtrack(problem,
                      variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                      value_heuristic=LEAST_CONSTRAINING_VALUE,
                      inference=True)

print('Solving with min conflicts')
result_mc = min_conflicts(problem, iterations_limit=500)

print('Binarizing and solving again with backtracking')
new_variables, new_domains, new_constraints = convert_to_binary(variables, domains, constraints)
result_btb = backtrack(CspProblem(new_variables, new_domains, new_constraints),
                       variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                       value_heuristic=LEAST_CONSTRAINING_VALUE)


def human_result(result):
    template = """
     A4 A3 A2 A1
        S  E  N  D
     +  M  O  R  E
    ---------------
     M  O  N  E  Y
    """

    for variable, value in result.items():
        template = template.replace(variable, str(value))

    print(template)


print('Result backtracking:')
print(result_bt)
human_result(result_bt)

print('Result min conflicts:')
print(result_mc)
human_result(result_mc)

print('Result backtracking, binarized:')
print(result_btb)
human_result(result_btb)
