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


metodos_busqueda = (
    'backtrack',
    'min_conflicts',
)


for metodo_busqueda in metodos_busqueda:
    print 'Llamando a', metodo_busqueda
    probar = raw_input('ejecutar?')
    if probar != 'n':
        try:
            resultado = resolver(metodo_busqueda=metodo_busqueda)
        except:
            print u"Error al correr", metodo_busqueda
            raise

        if not isinstance(resultado, dict):
            salir(u"El resultado devuelto por la función no es el resultado del método de búsqueda de simpleai (un diccionario con la asignación)")

        print 'Resultado:'
        print resultado


if not os.path.exists('entrega2.txt'):
    salir(u"No se pudo encontrar el archivo de estadísticas")

with open('entrega2.txt') as archivo_stats:
    lineas_stats = archivo_stats.readlines()

metodos_busqueda_pendientes = list(metodos_busqueda)

print 'Estadisticas:'

for linea in lineas_stats:
    if linea.strip():
        try:
            metodo, resultado = linea.split(':{')
            resultado = eval('{' + resultado)

            print metodo
            print resultado
        except:
            salir("La siguiente linea de estadísticas no respeta el formato definido:\n" + linea)

        if not isinstance(resultado, dict):
            salir(u"El siguiente resultado no es un resultado devuelto por simpleai (diccionario de asignaciones): " + resultado)

        if metodo not in metodos_busqueda:
            print u"Método de búsqueda desconocido en archivo de estadísticas: " + metodo
        else:
            metodos_busqueda_pendientes.remove(metodo)


if metodos_busqueda_pendientes:
    salir(u"No se incluyeron las estadísticas de los siguientes métodos de búsqueda:\n" + ', '.join(metodos_busqueda_pendientes))


salir()
