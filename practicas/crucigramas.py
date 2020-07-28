# coding: utf-8
import itertools
import re

from simpleai.search import (backtrack, CspProblem, LEAST_CONSTRAINING_VALUE,
                             min_conflicts, MOST_CONSTRAINED_VARIABLE)

largos = {
    '1H': 2, '2H': 3, '4H': 2, '5H': 2, '7H': 2, '8H': 2, '10H': 3, '11H': 2,
    '1V': 2, '2V': 2, '3V': 3, '4V': 2, '6V': 3, '7V': 2, '8V': 2, '9V': 2,
}

palabras = set(re.sub(r'[^\w] ', '', '''Este es un texto para sacar palabras y asi
emular las claves del diccionario expuesto en el ejercicio.

Artificial Intelligence (AI) is a big field, and this is a big book. We have tried to explore the
full breadth of the field, which encompasses logic, probability, and continuous mathematics;
perception, reasoning, learning, and action; and everything from microelectronic devices to
robotic planetary explorers. The book is also big because we go into some depth.
The subtitle of this book is “A Modern Approach.” The intended meaning of this rather
empty phrase is that we have tried to synthesize what is now known into a common frame-
work, rather than trying to explain each subfield of AI in its own historical context. We
apologize to those whose subfields are, as a result, less recognizable.
''').lower().split())


variables = []
dominios = {}

for var, largo in largos.items():
    # agrego variables
    variables.append(var)

    # optamos por restringir el dominio a solo las palabras que poseen el largo
    # para completar la variable. Otra posibilidad es agregar restricciones.
    dominios[var] = [x for x in palabras if len(x) == largo]


restricciones = []


def distinto_valor(variables, valores):
    'Compara que los valores de las variables sean distintos'
    return valores[0] != valores[1]


# Todas las variables tienen que ser distintas. Con este diccionario no alcanza
# para que se cumpla esta restriccion; si se quiere ver un resultado hay que
# comentar esta restriccion o agregar un texto que contenga mas palabras para
# formar el vocabulario.
for var1, var2 in itertools.combinations(variables, 2):
    restricciones.append(((var1, var2), distinto_valor))


def interseccion(pos1, pos2):
    '''
    Devuelve una "restriccion" que controla que la interseccion de la primer
    palabra[pos1] sea igual a la segunda palabra[pos2].
    '''
    def restriccion(variables, valores):
        return valores[0][pos1] == valores[1][pos2]
    return restriccion

# Agregamos las intersecciones donde tienen que coincidir los caracteres
restricciones.append((('1H', '1V'), interseccion(0, 0)))
restricciones.append((('2H', '2V'), interseccion(0, 0)))
restricciones.append((('2H', '3V'), interseccion(2, 0)))
restricciones.append((('4H', '4V'), interseccion(0, 0)))
restricciones.append((('4H', '2V'), interseccion(1, 1)))
restricciones.append((('5H', '4V'), interseccion(1, 1)))
restricciones.append((('7H', '7V'), interseccion(0, 0)))
restricciones.append((('8H', '8V'), interseccion(0, 0)))
restricciones.append((('8H', '7V'), interseccion(1, 1)))
restricciones.append((('6V', '10H'), interseccion(2, 0)))
restricciones.append((('10H', '8V'), interseccion(2, 1)))
restricciones.append((('11H', '9V'), interseccion(1, 1)))


problem = CspProblem(variables, dominios, restricciones)

print 'backtrack:'
result = backtrack(problem,
                   variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                   value_heuristic=LEAST_CONSTRAINING_VALUE,
                   inference=True)

print result
