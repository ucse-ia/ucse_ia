from itertools import combinations

from simpleai.search import CspProblem, backtrack


#  F  c2 c1
#     T  W  O
# +   T  W  O
# -------------
#  F  O  U  R


letters = [
    "T",
    "W",
    "O",
    "F",
    "U",
    "R",
]

carries = [
    "c1",
    "c2",
]

problem_variables = letters + carries


domains = {}
for letter in letters:
    domains[letter] = list(range(10))
for carry in carries:
    domains[carry] = [0, 1]


print("Variables:", problem_variables)
print("Domains:", domains)


constraints = []


# restriction: all letters have different digits

def letters_are_different(variables, values):
    # ej:
    # variables = ("T", "W")
    # values = (5, 8)
    digit1, digit2 = values
    return digit1 != digit2


for letter1, letter2 in combinations(letters, 2):
    constraints.append(
        ((letter1, letter2), letters_are_different)
    )

# restriction: last column sum works

def last_column_sum(variables, values):
    value_o, value_r, value_c1 = values
    return value_o + value_o == value_c1 * 10 + value_r


constraints.append(
    (("O", "R", "c1"), last_column_sum)
)

# restriction: middle column sum works
# restriction: first column sum works

def normal_column_sum(variables, values):
    value_c_in, value_summed_letter, value_result_letter, value_c_out = values
    return value_summed_letter + value_summed_letter + value_c_in == value_c_out * 10 + value_result_letter


constraints.append(
    (("c1", "W", "U", "c2"), normal_column_sum)
)
constraints.append(
    (("c2", "T", "O", "F"), normal_column_sum)
)


problem = CspProblem(problem_variables, domains, constraints)
solution = backtrack(problem)

print("Solution:")
print(solution)




#  0  0  0
#     1  3  2
# +   1  3  2
# -------------
#  0  2  6  4


# {'T': 1, 'W': 3, 'O': 2, 'F': 0, 'U': 6, 'R': 4, 'c1': 0, 'c2': 0}
