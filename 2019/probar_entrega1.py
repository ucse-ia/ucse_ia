# coding: utf-8
import argparse
import importlib.util
import inspect
import os
from datetime import datetime


problemas = []


def problema(mensaje, *args):
    problemas.append(mensaje.format(*args))


def validar_tiempo(inicio, fin, tope, mensaje):
    diferencia = (fin - inicio).total_seconds()
    if diferencia > tope:
        problema(mensaje)


def probar_codigo(interactivo=False, saltear_errores=False, resultado_verboso=False, grupo=None):
    # dependencias
    try:
        from simpleai.search.models import SearchNode
    except ImportError:
        problema('No se pudo importar SimpleAI. Se encuentra instalado?')
        return

    # intentar importar la entrega
    print('Importando la entrega...')

    try:
        inicio = datetime.now()
        if grupo:
            spec = importlib.util.spec_from_file_location("{}.entrega1".format(grupo),
                                                          "{}/entrega1.py".format(grupo))
            entrega1 = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(entrega1)
        else:
            import entrega1
        fin = datetime.now()
    except ImportError:
        problema('No se pudo encontrar el código python. Probablemente el nombre del archivo .py '
                 'no es correcto, o no está en la raiz del repositorio.')
        return

    validar_tiempo(inicio, fin, 3,
                   'El import de la entrega demora demasiado tiempo, probablemente están '
                   'haciendo búsqueda en el import. Hagan lo del if __name__ ... que se '
                   'recomienda en la consigna.')

    # intentar extraer y validar la funcion resolver
    print('Extrayendo la función resolver...')

    resolver = getattr(entrega1, 'resolver', None)

    if resolver is None:
        problema('El módulo python no define la función resolver.')
        return

    firma_resolver = inspect.getargspec(resolver)
    args = firma_resolver.args
    defaults = firma_resolver.defaults or []
    if args[:len(args) - len(defaults)] != ['metodo_busqueda', 'franceses', 'piratas']:
        problema('La función resolver no recibe los parámetros definidos en la entrega.')
        return

    # validar el funcionamiento de la funcion resolver y el planteo del problema en general
    print('Probando la resolución de problemas...')

    franceses_consigna = (
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
        (2, 1),
        (2, 2),
        (2, 3),
        (3, 0),
        (3, 1),
        (3, 2),
        (4, 0),
        (4, 1),
        (5, 0),
    )
    piratas_consigna = (
        (4, 4),
        (4, 5),
        (5, 4),
    )

    # metodo_busqueda, franceses, piratas, limite_largo_camino, limite_tiempo
    pruebas = (
        # sin franceses, 1 pirata
        ('breadth_first', [], [(4, 4)], 14, 2),
        ('depth_first', [], [(4, 4)], 100, 10),
        ('greedy', [], [(4, 4)], 25, 2),
        ('astar', [], [(4, 4)], 14, 2),

        # 3 franceses, 2 piratas
        ('breadth_first', [(1, 0), (2, 1), (3, 0)], [(3, 4), (4, 4)], 19, 10),
        ('depth_first', [(1, 0), (2, 1), (3, 0)], [(3, 4), (4, 4)], 200, 30),
        ('greedy', [(1, 0), (2, 1), (3, 0)], [(3, 4), (4, 4)], 50, 10),
        ('astar', [(1, 0), (2, 1), (3, 0)], [(3, 4), (4, 4)], 19, 10),

        # caso de la consigna
        ('breadth_first', franceses_consigna, piratas_consigna, 33, 30),
        ('depth_first', franceses_consigna, piratas_consigna, 500, 60),
        ('greedy', franceses_consigna, piratas_consigna, 60, 30),
        ('astar', franceses_consigna, piratas_consigna, 33, 30),
    )

    for numero_prueba, prueba in enumerate(pruebas):
        metodo_busqueda, franceses, piratas, limite_largo_camino, limite_tiempo = prueba
        print('  Prueba', numero_prueba, ':', metodo_busqueda, 'franceses:', franceses, 'piratas:',
              piratas)

        if not interactivo or input('ejecutar? (Y/n)').strip() in ('y', ''):
            try:
                inicio = datetime.now()
                resultado = resolver(metodo_busqueda=metodo_busqueda,
                                     franceses=franceses,
                                     piratas=piratas)
                fin = datetime.now()

                if isinstance(resultado, SearchNode):
                    print('     largo camino:', len(resultado.path()))
                    print('     estado:', resultado.state)
                    print('     acciones:', [accion for accion, estado in resultado.path()])
                    if resultado_verboso:
                        print('     meta:', repr(resultado.state))
                        print('     camino:', repr(resultado.path()))
                else:
                    print('     resultado:', str(resultado))
                print('    duración:', (fin - inicio).total_seconds())

                if resultado is None:
                    problema('El resultado devuelto por la función resolver en la prueba {} fue '
                             'None, cuando el problema tiene que encontrar solución y se espera '
                             'que retorne el nodo resultante. Puede que la función resolver no '
                             'esté devolviendo el nodo resultante, o que el problema no esté '
                             'encontrando solución como debería.',
                             numero_prueba)
                elif isinstance(resultado, SearchNode):
                    if limite_largo_camino and len(resultado.path()) > limite_largo_camino:
                        problema('El resultado devuelto en la prueba {} excede el largo de camino'
                                 'esperable ({}) para ese problema y método de búsqueda. Es '
                                 'posible que algo no esté bien.',
                                 numero_prueba, limite_largo_camino)
                else:
                    problema('El resultado devuelto por la función resolver en la prueba {} no es '
                             'un nodo de búsqueda.',
                             numero_prueba)

                if limite_tiempo is not None:
                    validar_tiempo(inicio, fin, limite_tiempo,
                                   'La prueba {} demoró demasiado tiempo (más de {} segundos), '
                                   'probablemente algo no está demasiado '
                                   'bien.'.format(numero_prueba, limite_tiempo))
            except Exception as err:
                if saltear_errores:
                    problema('Error al ejecutar prueba {} ({})', numero_prueba, str(err))
                else:
                    raise


def probar_estadisticas(grupo=None):
    # abrir el archivo de estadisticas
    print('Abriendo estadísticas...')

    nombre_archivo = 'entrega1.txt'
    if grupo:
        nombre_archivo = os.path.join(grupo,nombre_archivo)

    if not os.path.exists(nombre_archivo):
        problema('No se pudo encontrar el archivo de estadísticas. Probablemente el nombre del '
                 'archivo no es correcto, o no está en la raiz del repositorio.')
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
                    problema('Caso desconocido en archivo de estadísticas: {}', caso)
                elif caso not in casos_pendientes:
                    problema('Caso repetido en archivo de estadísticas: {}', caso)
                else:
                    print('   Encontrado caso', caso)
                    print('    Valores:', valores)
                    casos_pendientes.remove(caso)
            except:
                problema('La siguiente linea de estadísticas no respeta el formato definido: {}',
                         linea)

    if casos_pendientes:
        problema('No se incluyeron las estadísticas de los siguientes casos: {}',
                 repr(casos_pendientes))


def imprimir_resultados():
    def listar_cosas(titulo, cosas):
        if cosas:
            print(titulo + ':')
            for cosa in cosas:
                print('*', cosa)

    listar_cosas('Problemas que es necesario corregir', problemas)


def probar(interactivo=False, saltear_errores=False, resultado_verboso=False, grupo=None):
    print('#' * 80)
    if grupo:
        print("Probando grupo", grupo)
    probar_codigo(interactivo, saltear_errores, resultado_verboso, grupo)
    print()
    probar_estadisticas(grupo)
    print()
    print('Pruebas automáticas terminadas!')
    print()
    imprimir_resultados()
    print('#' * 80)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store_true', help='Interactivo')
    parser.add_argument('-s', action='store_true', help='Saltear errores')
    parser.add_argument('-v', action='store_true', help='Resultado verboso')
    parser.add_argument('--path', help='Path a la entrega')
    args = parser.parse_args()

    probar(args.i, args.s, args.v, args.path)
