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
        from simpleai.search import CspProblem
    except ImportError:
        problemas.append(u'No se pudo importar SimpleAI. Se encuentra instalado?')
        return

    # intentar importar la entrega
    print u'Importando la entrega...'

    try:
        inicio = datetime.now()
        import entrega_2
        fin = datetime.now()
    except ImportError:
        problemas.append(u'No se pudo encontrar el código python. Probablemente el nombre del archivo .py no es correcto, o no está en la raiz del repositorio.')
        return

    validar_tiempo(inicio, fin, 5, problemas, u'El import de la entrega demora demasiado tiempo, probablemente están haciendo búsqueda en el import. Hagan lo del if __name__ ... que se recomienda en la consigna.')

    # intentar extraer y validar la funcion resolver
    print u'Extrayendo la función resolver...'

    resolver = getattr(entrega_2, 'resolver', None)

    if resolver is None:
        problemas.append(u'El módulo python no define la función resolver.')
        return

    if inspect.getargspec(resolver)[0] != ['metodo_busqueda', 'iteraciones']:
        print resolver.__code__.co_varnames
        problemas.append(u'La función resolver no recibe los parámetros definidos en la entrega.')
        return

    # validar el funcionamiento de la funcion resolver y el planteo del problema en general
    print u'Probando la resolución de problemas...'

    # metodo_busqueda, posicion_rey, graph_search, limite_largo_camino, limite_tiempo
    pruebas = (
        ('backtrack', None, 10),
        ('min_conflicts', dict(iteraciones=50), 10),
    )

    parametros_default = dict(iteraciones=None)

    for numero_prueba, (metodo_busqueda, parametros_pisados, limite_tiempo) in enumerate(pruebas):
        parametros = parametros_default.copy()
        if parametros_pisados:
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

                if limite_tiempo is not None:
                    validar_tiempo(inicio, fin, limite_tiempo, advertencias, u'La prueba %i demoró demasiado tiempo (más de %i segundos), probablemente algo no está demasiado bien.' % (numero_prueba, limite_tiempo))

                if not isinstance(resultado, dict):
                    problemas.append(u'El resultado devuelto por la función resolver en la prueba %i no es el diccionario que retorna el método de búsqueda de SimpleAI. Puede que la función resolver no esté devolviendo el diccionario resultante, o que el problema no esté encontrando solución como debería.' % numero_prueba)
                else:
                    print u'     resultado:', ' | '.join('%s: %s' % (k, v) for k, v in sorted(list(resultado.items())))
            except Exception as err:
                if saltear_errores:
                    problemas.append(u'Error al ejecutar %s (%s)' % (metodo_busqueda, str(err)))
                else:
                    raise


def probar_estadisticas():
    # abrir el archivo de estadisticas
    print u'Abriendo estadísticas...'

    nombre_archivo = 'entrega_2.txt'
    if not os.path.exists(nombre_archivo):
        problemas.append(u'No se pudo encontrar el archivo de estadísticas. Probablemente el nombre del archivo no es correcto, o no está en la raiz del repositorio.')
        return

    with open(nombre_archivo) as archivo_stats:
        lineas_stats = archivo_stats.readlines()

    # validar contenidos
    casos = range(1, 3)
    casos_pendientes = casos[:]

    for linea in lineas_stats:
        linea = linea.strip()
        if linea:
            try:
                caso = int(linea[:1])
                resultado = eval(linea[2:])

                if caso not in casos:
                    problemas.append(u'Caso desconocido en archivo de estadísticas: %i' % caso)
                elif caso not in casos_pendientes:
                    problemas.append(u'Caso repetido en archivo de estadísticas: %i' % caso)
                else:
                    print u"   Encontrado caso", caso
                    casos_pendientes.remove(caso)

                    if not isinstance(resultado, dict):
                        problemas.append(u'El resultado informado para el caso %i no es el diccionario que retorna el método de búsqueda de SimpleAI.' % caso)
                        print u'     resultado en formato incorrecto:', repr(resultado)
                    else:
                        print u'     resultado:', repr(resultado)
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
