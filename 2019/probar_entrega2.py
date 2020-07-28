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


def probar_codigo(interactivo=False, saltear_errores=False, grupo=None):
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
            spec = importlib.util.spec_from_file_location("{}.entrega2".format(grupo),
                                                          "{}/entrega2.py".format(grupo))
            entrega2 = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(entrega2)
        else:
            import entrega2
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

    resolver = getattr(entrega2, 'resolver', None)

    if resolver is None:
        problema('El módulo python no define la función resolver.')
        return

    firma_resolver = inspect.getargspec(resolver)
    args = firma_resolver.args
    defaults = firma_resolver.defaults or []
    if args[:len(args) - len(defaults)] != ['metodo_busqueda', 'iteraciones']:
        problema('La función resolver no recibe los parámetros definidos en la entrega.')
        return

    # validar el funcionamiento de la funcion resolver y el planteo del problema en general
    print('Probando la resolución de problemas...')

    # metodo_busqueda, iteraciones, limite_tiempo
    pruebas = (
        ('backtrack', None, 30),
        ('min_conflicts', 50, 30),
    )

    for numero_prueba, (metodo_busqueda, iteraciones, limite_tiempo) in enumerate(pruebas):
        print('  Prueba', numero_prueba, ':', metodo_busqueda)

        if not interactivo or input('ejecutar? (Y/n)').strip() in ('y', ''):
            try:
                inicio = datetime.now()
                resultado = resolver(metodo_busqueda=metodo_busqueda,
                                     iteraciones=iteraciones)
                fin = datetime.now()

                if isinstance(resultado, dict):
                    print(
                        '     resultado:',
                        ', '.join('{}: {}'.format(k, v)
                                  for k, v in sorted(list(resultado.items())))
                    )
                else:
                    problema('El resultado devuelto por la función resolver en la prueba {} no es '
                             'el diccionario que retorna el método de búsqueda de SimpleAI. Puede '
                             'que la función resolver no esté devolviendo el diccionario '
                             'resultante, o que el problema no esté encontrando solución como '
                             'debería.',
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

    nombre_archivo = 'entrega2.txt'
    if grupo:
        nombre_archivo = os.path.join(grupo, nombre_archivo)

    if not os.path.exists(nombre_archivo):
        problema('No se pudo encontrar el archivo de estadísticas. Probablemente el nombre del '
                 'archivo no es correcto, o no está en la raiz del repositorio.')
        return

    with open(nombre_archivo) as archivo_stats:
        lineas_stats = archivo_stats.readlines()

    # validar contenidos
    casos = list(range(1, 3))
    casos_pendientes = casos[:]

    for linea in lineas_stats:
        linea = linea.strip()
        if linea:
            try:
                caso, resultado = linea.split(':',1)
                caso = int(caso)
                resultado = eval(resultado)

                if caso not in casos:
                    problema('Caso desconocido en archivo de estadísticas: {}', caso)
                elif caso not in casos_pendientes:
                    problema('Caso repetido en archivo de estadísticas: {}', caso)
                else:
                    if isinstance(resultado, dict):
                        print('   Encontrado caso', caso)
                        print('     resultado:', repr(resultado))
                        casos_pendientes.remove(caso)
                    else:
                        problema('El resultado informado para el caso {} no es el diccionario que '
                                 'retorna el método de búsqueda de SimpleAI.',
                                 caso)
                        print('     resultado en formato incorrecto:', repr(resultado))
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



def probar(interactivo=False, saltear_errores=False, grupo=None):
    print('#' * 80)
    if grupo:
        print("Probando grupo", grupo)
    probar_codigo(interactivo, saltear_errores, grupo)
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
    parser.add_argument('--path', help='Path a la entrega')
    args = parser.parse_args()

    probar(args.i, args.s, args.path)
