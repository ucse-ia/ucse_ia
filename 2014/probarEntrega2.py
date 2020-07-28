# coding: utf-8
import os
import sys
from simpleai.search.models import SearchNode

from simpleai.search import (MOST_CONSTRAINED_VARIABLE, LEAST_CONSTRAINING_VALUE,
                             HIGHEST_DEGREE_VARIABLE)

nombres_heuristicas = {
    MOST_CONSTRAINED_VARIABLE: 'MOST_CONSTRAINED_VARIABLE',
    HIGHEST_DEGREE_VARIABLE: 'HIGHEST_DEGREE_VARIABLE',
    LEAST_CONSTRAINING_VALUE: 'LEAST_CONSTRAINING_VALUE',
    None: 'None',
}


def salir(error=None):
    if not error:
        print u"La entrega cumple con la interfaz definida y puede ser corregida"
        sys.exit()
    else:
        print u"La entrega NO respeta la interfaz definida, NO puede ser corregida"
        print u"Problema:"
        print error
        sys.exit(1)


try:
    import entrega2
except ImportError:
    salir(u"No se pudo encontrar el módulo")


resolver = getattr(entrega2, 'resolver', None)

if resolver is None:
    salir(u"El módulo no define la función resolver")


parametros_resolver = (
    {'metodo_busqueda': 'backtrack', 'heuristica_variable': None, 'heuristica_valor': None},
    {'metodo_busqueda': 'backtrack', 'heuristica_variable': MOST_CONSTRAINED_VARIABLE, 'heuristica_valor': None},
    {'metodo_busqueda': 'backtrack', 'heuristica_variable': HIGHEST_DEGREE_VARIABLE, 'heuristica_valor': None},
    {'metodo_busqueda': 'backtrack', 'heuristica_variable': None, 'heuristica_valor': LEAST_CONSTRAINING_VALUE},
    {'metodo_busqueda': 'backtrack', 'heuristica_variable': MOST_CONSTRAINED_VARIABLE, 'heuristica_valor': LEAST_CONSTRAINING_VALUE},
    {'metodo_busqueda': 'backtrack', 'heuristica_variable': HIGHEST_DEGREE_VARIABLE, 'heuristica_valor': LEAST_CONSTRAINING_VALUE},
    {'metodo_busqueda': 'min_conflicts', 'heuristica_variable': None, 'heuristica_valor': None},
)

for parametros in parametros_resolver:
    print 'Llamando a resolver con:', parametros

    if raw_input('probar?') == 'y':
        try:
            resultado = resolver(**parametros)
        except:
            salir(u"Error al correr resolver con " + str(parametros))

        if not isinstance(resultado, dict):
            salir(u"El resultado devuelto por la función no es el resultado del método de búsqueda de simpleai (un diccionario con la asignación)")

        print 'Resultado:'
        print resultado


if not os.path.exists('entrega2.txt'):
    salir(u"No se pudo encontrar el archivo de estadísticas")

with open('entrega2.txt') as archivo_stats:
    lineas_stats = archivo_stats.readlines()

parametros_pendientes = [','.join(map(str, [p['metodo_busqueda'],
                                            nombres_heuristicas[p['heuristica_variable']],
                                            nombres_heuristicas[p['heuristica_valor']]]))
                         for p in parametros_resolver]

print 'Estadisticas:'

for linea in lineas_stats:
    if linea.strip():
        try:
            parametros, resultado = linea.split('{')
            parametros = parametros[:-1]  # sacamos la coma al final
            resultado = '{' + resultado  # agregamos el { sacado en el split
            resultado = eval(resultado)

            print parametros
            print resultado
        except:
            salir("La siguiente linea de estadísticas no respeta el formato definido:\n" + linea)

        if not isinstance(resultado, dict):
            salir(u"El siguiente resultado no es un resultado devuelto por simpleai (diccionario de asignaciones): " + parametros)

        if parametros not in parametros_pendientes:
            salir(u"Método de búsqueda desconocido en archivo de estadísticas: " + parametros)
        else:
            parametros_pendientes.remove(parametros)


if parametros_pendientes:
    salir(u"No se incluyeron las estadísticas de los siguientes métodos de búsqueda:\n" + ', '.join(parametros_pendientes))


salir()
