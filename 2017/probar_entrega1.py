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


def probar_codigo(interactivo=False, saltear_errores=False, resultado_verboso=False):
    # dependencias
    try:
        from simpleai.search.models import SearchNode
    except ImportError:
        problemas.append('No se pudo importar SimpleAI. Se encuentra instalado?')
        return

    # intentar importar la entrega
    print('Importando la entrega...')

    try:
        inicio = datetime.now()
        import entrega1
        fin = datetime.now()
    except ImportError:
        problemas.append('No se pudo encontrar el código python. Probablemente el nombre del '
                         'archivo .py no es correcto, o no está en la raiz del repositorio.')
        return

    validar_tiempo(inicio, fin, 3, problemas,
                   'El import de la entrega demora demasiado tiempo, probablemente están '
                   'haciendo búsqueda en el import. Hagan lo del if __name__ ... que se '
                   'recomienda en la consigna.')

    # intentar extraer y validar la funcion resolver
    print('Extrayendo la función resolver...')

    resolver = getattr(entrega1, 'resolver', None)

    if resolver is None:
        problemas.append('El módulo python no define la función resolver.')
        return

    if inspect.getargspec(resolver)[0] != ['metodo_busqueda', 'posiciones_aparatos']:
        problemas.append('La función resolver no recibe los parámetros definidos en la entrega.')
        return

    # validar el funcionamiento de la funcion resolver y el planteo del problema en general
    print('Probando la resolución de problemas...')

    # metodo_busqueda, posiciones_aparatos, limite_largo_camino, limite_tiempo
    pruebas = (

        # simples
        ('breadth_first', ((1, 2),), 10, 5),
        ('depth_first', ((1, 2),), None, 5),
        ('greedy', ((1, 2),), None, 5),
        ('astar', ((1, 2),), 10, 5),

        # completos
        ('breadth_first', ((1, 2), (2, 0), (3, 0)), 25, None),
        ('depth_first', ((1, 2), (2, 0), (3, 0)), None, 600),
        ('greedy', ((1, 2), (2, 0), (3, 0)), None, 300),
        ('astar', ((1, 2), (2, 0), (3, 0)), 25, 600),
    )

    for numero_prueba, (metodo_busqueda, posiciones_aparatos, limite_largo_camino, limite_tiempo) in enumerate(pruebas):
        print('  Prueba', numero_prueba, ':', metodo_busqueda, 'aparatos en', posiciones_aparatos)

        if not interactivo or input('ejecutar? (Y/n)').strip() in ('y', ''):
            try:
                inicio = datetime.now()
                resultado = resolver(metodo_busqueda=metodo_busqueda,
                                     posiciones_aparatos=posiciones_aparatos)

                if isinstance(resultado, SearchNode):
                    print('     largo camino:', len(resultado.path()))
                    print('     estado:', resultado.state)
                    print('     acciones:', [accion for accion, estado in resultado.path()])
                    if resultado_verboso:
                        print('     meta:', repr(resultado.state))
                        print('     camino:', repr(resultado.path()))
                else:
                    print('     resultado:', str(resultado))
                fin = datetime.now()

                if limite_tiempo is not None:
                    validar_tiempo(inicio, fin, limite_tiempo, advertencias,
                                   'La prueba {} demoró demasiado tiempo (más de {} segundos), '
                                   'probablemente algo no está demasiado bien.'.format(
                                       numero_prueba,
                                       limite_tiempo))

                if resultado is None:
                    problemas.append('El resultado devuelto por la función resolver en la '
                                     'prueba {} fue None, cuando el problema tiene que '
                                     'encontrar solución y se espera que retorne el nodo '
                                     'resultante. Puede que la función resolver no esté '
                                     'devolviendo el nodo resultante, o que el problema no esté '
                                     'encontrando solución como debería.'.format(numero_prueba))
                elif isinstance(resultado, SearchNode):
                    if limite_largo_camino and len(resultado.path()) > limite_largo_camino:
                        advertencias.append('El resultado devuelto en la prueba {} excede el '
                                            'largo de camino esperable ({}) para ese problema y '
                                            'método de búsqueda. Es posible que algo no esté '
                                            'bien.'.format(numero_prueba, limite_largo_camino))
                else:
                    problemas.append('El resultado devuelto por la función resolver en la '
                                     'prueba {} no es un nodo de búsqueda.'.format(numero_prueba))

            except Exception as err:
                if saltear_errores:
                    problemas.append('Error al ejecutar {} ({})'.format(metodo_busqueda, str(err)))
                else:
                    raise


def probar_estadisticas():
    # abrir el archivo de estadisticas
    print('Abriendo estadísticas...')

    nombre_archivo = 'entrega1.txt'
    if not os.path.exists(nombre_archivo):
        problemas.append('No se pudo encontrar el archivo de estadísticas. Probablemente el '
                         'nombre del archivo no es correcto, o no está en la raiz del '
                         'repositorio.')
        return

    with open(nombre_archivo) as archivo_stats:
        lineas_stats = archivo_stats.readlines()

    # validar contenidos
    casos = list(range(1, 5))
    casos_pendientes = casos[:]

    for linea in lineas_stats:
        linea = linea.strip()
        if linea:
            try:
                caso, valores = linea.split(':')
                caso = int(caso)
                valores = list(map(int, valores.split(',')))
                if len(valores) != 4:
                    raise ValueError()

                if caso not in casos:
                    problemas.append('Caso desconocido en archivo de estadísticas: {}'.format(caso))
                elif caso not in casos_pendientes:
                    problemas.append('Caso repetido en archivo de estadísticas: {}'.format(caso))
                else:
                    print('   Encontrado caso', caso)
                    print('    Valores:', valores)
                    casos_pendientes.remove(caso)
            except:
                problemas.append('La siguiente linea de estadísticas no respeta el formato '
                                 'definido: {}'.format(linea))

    if casos_pendientes:
        problemas.append('No se incluyeron las estadísticas de los siguientes '
                         'casos: {}'.format(repr(casos_pendientes)))


def imprimir_resultados():
    def listar_cosas(titulo, cosas):
        if cosas:
            print(titulo + ':')
            for cosa in cosas:
                print('*', cosa)

    listar_cosas('Problemas que es necesario corregir', problemas)
    listar_cosas('Advertencias (cosas que pueden ser un problema, aunque no siempre)', advertencias)
    listar_cosas('Recomendaciones', recomendaciones)


if __name__ == '__main__':
    print()
    probar_codigo(interactivo='-i' in sys.argv,
                  saltear_errores='-s' in sys.argv,
                  resultado_verboso='-v' in sys.argv)
    print()
    probar_estadisticas()
    print()
    print('Pruebas automáticas terminadas!')
    print()
    imprimir_resultados()
