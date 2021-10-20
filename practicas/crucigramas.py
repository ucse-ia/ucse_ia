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


How to use Machine Learning on a Very Complicated Problem
So far in Part 1, 2 and 3, we’ve used machine learning to solve isolated problems that have only
one step — estimating the price of a house, generating new data based on existing data and telling
if an image contains a certain object. All of those problems can be solved by choosing one machine
learning algorithm, feeding in data, and getting the result.
But face recognition is really a series of several related problems:
First, look at a picture and find all the faces in it
Second, focus on each face and be able to understand that even if a face is turned in a weird
direction or in bad lighting, it is still the same person.
Third, be able to pick out unique features of the face that you can use to tell it apart from other
people— like how big the eyes are, how long the face is, etc.
Finally, compare the unique features of that face to all the people you already know to determine
the person’s name.
As a human, your brain is wired to do all of this automatically and instantly. In fact, humans are
too good at recognizing faces and end up seeing faces in everyday objects:

Computers are not capable of this kind of high-level generalization (at least not yet…), so we have
to teach them how to do each step in this process separately.
We need to build a pipeline where we solve each step of face recognition separately and pass the
result of the current step to the next step. In other words, we will chain together several machine
learning algorithms:
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

print('backtrack:')
result = backtrack(problem,
                   variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                   value_heuristic=LEAST_CONSTRAINING_VALUE,
                   inference=True)
posiciones = {
    '1H': (0, 0), '2H': (0, 3), '4H': (1, 2), '5H': (2, 1), '7H': (3, 3),
    '8H': (4, 2), '10H': (5, 0), '11H': (5, 4),
    '1V': (0, 0), '2V': (0, 3), '3V': (0, 5), '4V': (1, 2), '6V': (3, 0),
    '7V': (3, 3), '8V': (4, 2), '9V': (4, 5),
}

posiciones_letras = {}
crucigrama = [['\u25A0'] * 6 for x in range(6)]
for palabra, (fila, columna) in posiciones.items():
    for letra in range(largos[palabra]):
        fila_letra = fila
        columna_letra = columna
        if palabra.endswith('H'):
            columna_letra += letra
        else:
            fila_letra += letra
        crucigrama[fila_letra][columna_letra] = result[palabra][letra]
print(result)
print('\n'.join(['| ' + ' | '.join(palabra) + ' |' for palabra in crucigrama]))
