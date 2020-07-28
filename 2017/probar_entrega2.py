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
        problemas.append('No se pudo importar SimpleAI. Se encuentra instalado?')
        return

    # intentar importar la entrega
    print('Importando la entrega...')

    try:
        inicio = datetime.now()
        import entrega2
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

    resolver = getattr(entrega2, 'resolver', None)

    if resolver is None:
        problemas.append('El módulo python no define la función resolver.')
        return

    if inspect.getargspec(resolver)[0] != ['metodo_busqueda', 'iteraciones']:
        problemas.append('La función resolver no recibe los parámetros definidos en la entrega.')
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

                if isinstance(resultado, dict):
                    print('     resultado:', ', '.join('{}: {}'.format(k, v) for k, v in sorted(list(resultado.items()))))
                else:
                    problemas.append(u'El resultado devuelto por la función resolver en la prueba {} no es el diccionario que retorna el método de búsqueda de SimpleAI. Puede que la función resolver no esté devolviendo el diccionario resultante, o que el problema no esté encontrando solución como debería.'.format(numero_prueba))

                fin = datetime.now()

                if limite_tiempo is not None:
                    validar_tiempo(inicio, fin, limite_tiempo, advertencias,
                                   'La prueba {} demoró demasiado tiempo (más de {} segundos), '
                                   'probablemente algo no está demasiado bien.'.format(
                                       numero_prueba,
                                       limite_tiempo))
            except Exception as err:
                if saltear_errores:
                    problemas.append('Error al ejecutar {} ({})'.format(metodo_busqueda, str(err)))
                else:
                    raise


def probar_estadisticas():
    # abrir el archivo de estadisticas
    print('Abriendo estadísticas...')

    nombre_archivo = 'entrega2.txt'
    if not os.path.exists(nombre_archivo):
        problemas.append('No se pudo encontrar el archivo de estadísticas. Probablemente el '
                         'nombre del archivo no es correcto, o no está en la raiz del '
                         'repositorio.')
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
                    problemas.append('Caso desconocido en archivo de estadísticas: {}'.format(caso))
                elif caso not in casos_pendientes:
                    problemas.append('Caso repetido en archivo de estadísticas: {}'.format(caso))
                else:
                    if isinstance(resultado, dict):
                        print('   Encontrado caso', caso)
                        print('     resultado:', repr(resultado))
                        casos_pendientes.remove(caso)
                    else:
                        problemas.append(u'El resultado informado para el caso {} no es el diccionario que retorna el método de búsqueda de SimpleAI.'.format(caso))
                        print('     resultado en formato incorrecto:', repr(resultado))
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
                  saltear_errores='-s' in sys.argv)
    print()
    probar_estadisticas()
    print()
    print('Pruebas automáticas terminadas!')
    print()
    imprimir_resultados()
