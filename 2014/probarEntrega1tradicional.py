# coding: utf-8
import os
import sys
from simpleai.search.models import SearchNode


ciudades = 'san francisco,chicago,montreal,new york,atlanta,washington,los angeles,mexico city,miami,bogota,lima,santiago,sao paulo,buenos aires,madrid,london,paris,essen,milan,st petersburg,moscow,istanbul,algiers,cairo,baghdad,tehran,delhi,karachi,riyadh,mumbai,kolkata,chennai,lagos,khartoum,kinshasa,johannesburg,beijing,soul,tokyo,shanghai,osaka,taipei,hong kong,bangkok,ho chi minh city,manila,jakarta,sydney'.split(',')


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
    import entrega1tradicional
except ImportError:
    salir(u"No se pudo encontrar el módulo")


resolver = getattr(entrega1tradicional, 'resolver', None)

if resolver is None:
    salir(u"El módulo no define la función resolver")


metodos_busqueda = 'breadth_first depth_first limited_depth_first greedy astar'.split()

for metodo_busqueda in metodos_busqueda:
    print 'Llamando a', metodo_busqueda
    ciudad = 'sydney'
    infecciones = dict((ciudad, 0) for ciudad in ciudades)
    infecciones['los angeles'] = 1
    infecciones['tokyo'] = 3
    infecciones['seoul'] = 2

    probar = raw_input(metodo_busqueda)
    if probar != 'n':
        try:
            resultado = resolver(metodo_busqueda=metodo_busqueda,
                                ciudad=ciudad,
                                infecciones=infecciones)
        except:
            salir(u"Error al correr " + metodo_busqueda)

        if not isinstance(resultado, (SearchNode, type(None))):
            salir(u"El resultado devuelto por la función no es un nodo de búsqueda")

        print 'Resultado:'
        if resultado is None:
            print 'Sin solucion'
        else:
            print resultado.state
            print '\n'.join(map(str, resultado.path()))

if not os.path.exists('entrega1tradicional.txt'):
    salir(u"No se pudo encontrar el archivo de estadísticas")

with open('entrega1tradicional.txt') as archivo_stats:
    lineas_stats = archivo_stats.readlines()

metodos_busqueda_pendientes = metodos_busqueda[:]

print 'Estadisticas:'

for linea in lineas_stats:
    if linea.strip():
        try:
            metodo, valores = linea.split(':')
            valores = map(int, valores.split(','))

            print metodo
            print valores
        except:
            salir("La siguiente linea de estadísticas no respeta el formato definido:\n" + linea)

        if len(valores) != 4:
            salir(u"Cantidad incorrecta de valores para el método de búsqueda: " + metodo)

        if metodo not in metodos_busqueda:
            salir(u"Método de búsqueda desconocido en archivo de estadísticas: " + metodo)
        else:
            metodos_busqueda_pendientes.remove(metodo)


if metodos_busqueda_pendientes:
    salir(u"No se incluyeron las estadísticas de los siguientes métodos de búsqueda:\n" + ', '.join(metodos_busqueda_pendientes))


salir()
