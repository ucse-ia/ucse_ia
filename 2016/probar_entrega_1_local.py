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
        import entrega_1_local
        fin = datetime.now()
    except ImportError:
        problemas.append(u'No se pudo encontrar el código python. Probablemente el nombre del archivo .py no es correcto, o no está en la raiz del repositorio.')
        return

    validar_tiempo(inicio, fin, 5, problemas, u'El import de la entrega demora demasiado tiempo, probablemente están haciendo búsqueda en el import. Hagan lo del if __name__ ... que se recomienda en la consigna.')

    # intentar extraer y validar la funcion resolver
    print u'Extrayendo la función resolver...'

    resolver = getattr(entrega_1_local, 'resolver', None)

    if resolver is None:
        problemas.append(u'El módulo python no define la función resolver.')
        return

    if inspect.getargspec(resolver)[0] != ['metodo_busqueda', 'iteraciones', 'haz', 'reinicios']:
        print resolver.__code__.co_varnames
        problemas.append(u'La función resolver no recibe los parámetros definidos en la entrega.')
        return

    # validar el funcionamiento de la funcion resolver y el planteo del problema en general
    print u'Probando la resolución de problemas...'

    # metodo_busqueda, posicion_rey, graph_search, limite_largo_camino, limite_tiempo
    pruebas = (
        ('hill_climbing', dict(iteraciones=50)),
        ('hill_climbing_stochastic', dict(iteraciones=50)),
        ('beam', dict(iteraciones=50, haz=5)),
        ('hill_climbing_random_restarts', dict(iteraciones=50, reinicios=5)),
        ('simulated_annealing', dict(iteraciones=50)),
    )

    parametros_default = dict(reinicios=None, haz=None)

    for numero_prueba, (metodo_busqueda, parametros_pisados) in enumerate(pruebas):
        parametros = parametros_default.copy()
        parametros.update(parametros_pisados)

        print u'  Prueba', numero_prueba, ':', \
              metodo_busqueda, \
              u'con parametros', parametros

        if not interactivo or raw_input('ejecutar? (Y/n)').strip() in ('y', ''):
            try:
                inicio = datetime.now()
                resultado = resolver(metodo_busqueda=metodo_busqueda,
                                     **parametros)
                fin = datetime.now()

                if not isinstance(resultado, SearchNode):
                    problemas.append(u'El resultado devuelto por la función resolver en la prueba %i no es un nodo de búsqueda. Puede que la función resolver no esté devolviendo el nodo resultante, o que el problema no esté encontrando solución como debería.' % numero_prueba)
                else:
                    print u'     meta:', repr(resultado.state)
                    print u'     valor:', repr(resultado.value)
            except Exception as err:
                if saltear_errores:
                    problemas.append(u'Error al ejecutar %s (%s)' % (metodo_busqueda, str(err)))
                else:
                    raise


def probar_estadisticas():
    # abrir el archivo de estadisticas
    print u'Abriendo estadísticas...'

    nombre_archivo = 'entrega_1_local.txt'
    if not os.path.exists(nombre_archivo):
        problemas.append(u'No se pudo encontrar el archivo de estadísticas. Probablemente el nombre del archivo no es correcto, o no está en la raiz del repositorio.')
        return

    with open(nombre_archivo) as archivo_stats:
        lineas_stats = archivo_stats.readlines()

    # validar contenidos
    casos = range(1, 6)
    casos_pendientes = casos[:]

    for linea in lineas_stats:
        linea = linea.strip()
        if linea:
            try:
                caso, valor = map(int, linea.split(':'))

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
