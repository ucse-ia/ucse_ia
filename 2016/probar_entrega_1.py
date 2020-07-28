# coding: utf-8
from datetime import datetime
import inspect
import os
import sys



problemas = []
recomendaciones = []
advertencias = []


def validar_tiempo(inicio, fin, tope, listado, mensaje):
    diferencia = (fin - inicio).total_seconds()
    if diferencia > tope:
        listado.append(mensaje)


def probar_codigo(interactivo=False, saltear_errores=False):
    # dependencias
    try:
        from simpleai.search.models import SearchNode
    except ImportError:
        problemas.append(u'No se pudo importar SimpleAI. Se encuentra instalado?')
        return

    # intentar importar la entrega
    print u'Importando la entrega...'

    try:
        inicio = datetime.now()
        import entrega_1_tradicional
        fin = datetime.now()
    except ImportError:
        problemas.append(u'No se pudo encontrar el código python. Probablemente el nombre del archivo .py no es correcto, o no está en la raiz del repositorio.')
        return

    validar_tiempo(inicio, fin, 5, problemas, u'El import de la entrega demora demasiado tiempo, probablemente están haciendo búsqueda en el import. Hagan lo del if __name__ ... que se recomienda en la consigna.')

    # intentar extraer y validar la funcion resolver
    print u'Extrayendo la función resolver...'

    resolver = getattr(entrega_1_tradicional, 'resolver', None)

    if resolver is None:
        problemas.append(u'El módulo python no define la función resolver.')
        return

    if inspect.getargspec(resolver)[0] != ['metodo_busqueda', 'posicion_rey', 'controlar_estados_repetidos']:
        print resolver.__code__.co_varnames
        problemas.append(u'La función resolver no recibe los parámetros definidos en la entrega.')
        return

    # validar el funcionamiento de la funcion resolver y el planteo del problema en general
    print u'Probando la resolución de problemas...'

    # metodo_busqueda, posicion_rey, graph_search, limite_largo_camino, limite_tiempo
    pruebas = (
        ('breadth_first', (5, 3), True, 10, 10),
        ('depth_first', (5, 3), True, None, 10),
        ('greedy', (5, 3), True, None, 10),
        ('astar', (5, 3), False, 10, 10),
    )

    for numero_prueba, (metodo_busqueda, posicion_rey, graph_search, limite_largo_camino, limite_tiempo) in enumerate(pruebas):
        print u'  Prueba', numero_prueba, ':', \
              metodo_busqueda, \
              u'con el rey en', posicion_rey, \
              u'y control de estados repetidos en', graph_search

        if not interactivo or raw_input('ejecutar? (Y/n)').strip() in ('y', ''):
            try:
                inicio = datetime.now()
                resultado = resolver(metodo_busqueda=metodo_busqueda,
                                     posicion_rey=posicion_rey,
                                     controlar_estados_repetidos=graph_search)
                print u'     meta:', repr(resultado.state)
                print u'     camino:', repr(resultado.path())
                fin = datetime.now()

                validar_tiempo(inicio, fin, limite_tiempo, advertencias, u'La prueba %i demoró demasiado tiempo (más de %i segundos), probablemente algo no está demasiado bien.' % (numero_prueba, limite_tiempo))

                if resultado is None:
                    problemas.append(u'El resultado devuelto por la función resolver en la prueba %i fue None, cuando el problema tiene que encontrar solución y se espera que retorne el nodo resultante. Puede que la función resolver no esté devolviendo el nodo resultante, o que el problema no esté encontrando solución como debería.' % numero_prueba)
                elif isinstance(resultado, SearchNode):
                    if limite_largo_camino and len(resultado.path()) > limite_largo_camino:
                        advertencias.append(u'El resultado devuelto en la prueba %i excede el largo de camino esperable (%i) para ese problema y método de búsqueda. Es posible que algo no esté bien.' % (numero_prueba, limite_largo_camino))
                else:
                    problemas.append(u'El resultado devuelto por la función resolver en la prueba %i no es un nodo de búsqueda.' % numero_prueba)

            except Exception as err:
                if saltear_errores:
                    problemas.append(u'Error al ejecutar %s (%s)' % (metodo_busqueda, str(err)))
                else:
                    raise


def probar_estadisticas():
    # abrir el archivo de estadisticas
    print u'Abriendo estadísticas...'

    nombre_archivo = 'entrega_1_tradicional.txt'
    if not os.path.exists(nombre_archivo):
        problemas.append(u'No se pudo encontrar el archivo de estadísticas. Probablemente el nombre del archivo no es correcto, o no está en la raiz del repositorio.')
        return

    with open(nombre_archivo) as archivo_stats:
        lineas_stats = archivo_stats.readlines()

    # validar contenidos
    casos = range(1, 9)
    casos_pendientes = casos[:]

    for linea in lineas_stats:
        linea = linea.strip()
        if linea:
            try:
                caso, valores = linea.split(':')
                caso = int(caso)
                valores = map(int, valores.split(','))
                if len(valores) != 4:
                    raise ValueError()

                if caso not in casos:
                    problemas.append(u'Caso desconocido en archivo de estadísticas: %i' % caso)
                elif caso not in casos_pendientes:
                    problemas.append(u'Caso repetido en archivo de estadísticas: %i' % caso)
                else:
                    print u"   Encontrado caso", caso
                    casos_pendientes.remove(caso)
            except:
                problemas.append(u'La siguiente linea de estadísticas no respeta el formato definido: %s' % linea)

    if casos_pendientes:
        problemas.append(u'No se incluyeron las estadísticas de los siguientes casos: %s' % repr(casos_pendientes))


def imprimir_resultados():
    def listar_cosas(titulo, cosas):
        if cosas:
            print titulo + ':'
            for cosa in cosas:
                print '*', cosa

    listar_cosas(u'Problemas que es necesario corregir', problemas)
    listar_cosas(u'Advertencias (cosas que pueden ser un problema, aunque no siempre)', advertencias)
    listar_cosas(u'Recomendaciones', recomendaciones)


if __name__ == '__main__':
    print
    probar_codigo()
    print
    probar_estadisticas()
    print
    print u'Pruebas automáticas terminadas!'
    print
    imprimir_resultados()
