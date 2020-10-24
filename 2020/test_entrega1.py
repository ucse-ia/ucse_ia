import argparse
import importlib.util
import logging
import os
import sys
import warnings
from contextlib import contextmanager
from datetime import datetime
from inspect import signature

import pytest


@contextmanager
def warning_si_demora(limite_segs, mensaje):
    """
    Context manager para chequear la duración de algo, y si demora demasiado, disparar un warning.
    """
    inicio = datetime.now()

    yield

    fin = datetime.now()
    if limite_segs is not None and (fin - inicio).total_seconds() > limite_segs:
        warnings.warn(mensaje)


@pytest.mark.dependency()
def test_modulo_existe():
    # Si falla este test es porque no se pudo encontrar el código python de la entrega.
    # Probablemente el nombre del archivo no es correcto (debe ser entrega1.py), o no está en la
    # raiz del repo, o no se están corriento los tests desde la raiz del repo.
    mensaje_si_demora = ("El import de la entrega demora demasiado tiempo, probablemente están "
                         "haciendo búsqueda en el import. Hagan lo del if __name__ ... que se "
                         "recomienda en la consigna")
    with warning_si_demora(3, mensaje_si_demora):
        import entrega1


@pytest.fixture()
def planear_camiones():
    import entrega1
    funcion_planear = getattr(entrega1, "planear_camiones", None)

    return funcion_planear


@pytest.mark.dependency(depends=["test_modulo_existe"])
def test_funcion_existe(planear_camiones):
    assert planear_camiones is not None, "La función planear_camiones no existe"


@pytest.mark.dependency(depends=["test_funcion_existe"])
def test_funcion_bien_definida(planear_camiones):
    parametros = list(signature(planear_camiones).parameters)

    # los primeros parámetros de la función tienen que ser los pedidos
    assert parametros[:3] == ['metodo', 'camiones', 'paquetes'], \
           "La función planear_camiones no recibe los parámetros definidos en la entrega"


DISTANCIAS = {
    ('sunchales', 'lehmann'): 32,
    ('lehmann', 'rafaela'): 8,
    ('rafaela', 'susana'): 10,
    ('susana', 'angelica'): 25,
    ('angelica', 'san_vicente'): 18,
    ('angelica', 'sc_de_saguier'): 60,
    ('rafaela', 'esperanza'): 70,
    ('esperanza', 'recreo'): 20,
    ('recreo', 'santa_fe'): 10,
    ('santa_fe', 'santo_tome'): 5,
    ('santo_tome', 'angelica'): 85,
    ('santo_tome', 'sauce_viejo'): 15,
}
# agregamos las inversas también:
for (ciudad1, ciudad2), kms in list(DISTANCIAS.items()):
    DISTANCIAS[(ciudad2, ciudad1)] = kms

# solo por legibilidad de fails
TRAMOS_VALIDOS = set(DISTANCIAS.keys())
SEDES = 'rafaela', 'santa_fe'


CAMION_NORMAL = "c_normal", "rafaela", 1.5
CAMION_NORMAL2 = "c_normal2", "rafaela", 1.5
CAMION_COSTERO = "c_este", "santa_fe", 1.5
CAMION_INUTIL = "c_inutil", "rafaela", 0.002

PAQUETE_NORMAL = "p_normal", "rafaela", "lehmann"
PAQUETE_NORMAL2 = "p_normal2", "rafaela", "lehmann"
PAQUETE_INVERTIDO = "p_invertido", "lehmann", "rafaela"
PAQUETE_OPUESTO = "p_opuesto", "rafaela", "susana"
PAQUETE_PASANDO_NORMAL = "p_pasando_normal", "rafaela", "sunchales"
PAQUETE_MOLESTO = "p_molesto", "sunchales", "susana"
PAQUETE_MUY_LEJOS = "p_lejos", "sunchales", "sauce_viejo"
PAQUETE_COSTERO = "p2", "santo_tome", "recreo"


@pytest.mark.dependency(depends=["test_funcion_bien_definida"])
@pytest.mark.parametrize("camiones,paquetes,metodo,viajes_esperados,limite_segs", (
    # casos super básicos
    ((CAMION_NORMAL, ), (PAQUETE_NORMAL, ), "breadth_first", 2, 3),
    ((CAMION_NORMAL, ), (PAQUETE_NORMAL, ), "uniform_cost", 2, 3),
    ((CAMION_NORMAL, ), (PAQUETE_NORMAL, ), "astar", 2, 3),

    # camión único con paquete que tiene que ir a ser buscado
    ((CAMION_NORMAL, ), (PAQUETE_INVERTIDO, ), "breadth_first", 2, 3),
    ((CAMION_NORMAL, ), (PAQUETE_INVERTIDO, ), "uniform_cost", 2, 3),
    ((CAMION_NORMAL, ), (PAQUETE_INVERTIDO, ), "astar", 2, 3),

    # camión único con par de paquetes iguales
    ((CAMION_NORMAL, ), (PAQUETE_NORMAL, PAQUETE_NORMAL2), "breadth_first", 2, 3),
    ((CAMION_NORMAL, ), (PAQUETE_NORMAL, PAQUETE_NORMAL2), "uniform_cost", 2, 3),
    ((CAMION_NORMAL, ), (PAQUETE_NORMAL, PAQUETE_NORMAL2), "astar", 2, 3),

    # camión único con paquetes para la ida y la vuelta
    ((CAMION_NORMAL, ), (PAQUETE_NORMAL, PAQUETE_INVERTIDO), "breadth_first", 2, 3),
    ((CAMION_NORMAL, ), (PAQUETE_NORMAL, PAQUETE_INVERTIDO), "uniform_cost", 2, 3),
    ((CAMION_NORMAL, ), (PAQUETE_NORMAL, PAQUETE_INVERTIDO), "astar", 2, 3),

    # camión único con par de paquetes que comparten recorrido
    ((CAMION_NORMAL, ), (PAQUETE_NORMAL, PAQUETE_PASANDO_NORMAL), "breadth_first", 4, 5),
    ((CAMION_NORMAL, ), (PAQUETE_NORMAL, PAQUETE_PASANDO_NORMAL), "uniform_cost", 4, 5),
    ((CAMION_NORMAL, ), (PAQUETE_NORMAL, PAQUETE_PASANDO_NORMAL), "astar", 4, 5),

    # camión único con par de paquetes con viajes disyuntos
    ((CAMION_NORMAL, ), (PAQUETE_NORMAL, PAQUETE_OPUESTO), "breadth_first", 4, 5),
    ((CAMION_NORMAL, ), (PAQUETE_NORMAL, PAQUETE_OPUESTO), "uniform_cost", 4, 5),
    ((CAMION_NORMAL, ), (PAQUETE_NORMAL, PAQUETE_OPUESTO), "astar", 4, 5),

    # camión único con paquete de viaje con recarga en el medio
    ((CAMION_NORMAL, ), (PAQUETE_MOLESTO, ), "breadth_first", 6, 5),
    ((CAMION_NORMAL, ), (PAQUETE_MOLESTO, ), "uniform_cost", 6, 5),
    ((CAMION_NORMAL, ), (PAQUETE_MOLESTO, ), "astar", 6, 5),

    # un camion teniendo que llevar paquete muy lejos recargando más de una vez y terminando en
    # otra ciudad que la de origen
    ((CAMION_NORMAL, ), (PAQUETE_MUY_LEJOS, ), "breadth_first", 11, 15),
    ((CAMION_NORMAL, ), (PAQUETE_MUY_LEJOS, ), "uniform_cost", 11, 5),
    ((CAMION_NORMAL, ), (PAQUETE_MUY_LEJOS, ), "astar", 11, 5),

    # dos camiones pero uno no hace falta que haga nada
    ((CAMION_NORMAL, CAMION_NORMAL2), (PAQUETE_NORMAL, PAQUETE_NORMAL2), "breadth_first", 2, 5),
    ((CAMION_NORMAL, CAMION_NORMAL2), (PAQUETE_NORMAL, PAQUETE_NORMAL2), "uniform_cost", 2, 5),
    ((CAMION_NORMAL, CAMION_NORMAL2), (PAQUETE_NORMAL, PAQUETE_NORMAL2), "astar", 2, 5),

    # dos camiones con recorridos que se acomodan bien a que se repartan
    ((CAMION_NORMAL, CAMION_COSTERO), (PAQUETE_NORMAL, PAQUETE_COSTERO), "breadth_first", 6, 15),
    ((CAMION_NORMAL, CAMION_COSTERO), (PAQUETE_NORMAL, PAQUETE_COSTERO), "uniform_cost", 6, 5),
    ((CAMION_NORMAL, CAMION_COSTERO), (PAQUETE_NORMAL, PAQUETE_COSTERO), "astar", 6, 5),

    # dos camiones pero uno es inútil así que el otro tiene que hacer todo
    # en el caso de breadth_first no va a ser óptimo, porque el camino de menos pasos entre
    # rafaela y santa fe, no es el de menos costo
    ((CAMION_NORMAL, CAMION_INUTIL), (PAQUETE_NORMAL, PAQUETE_COSTERO), "breadth_first", 8, 15),
    ((CAMION_NORMAL, CAMION_INUTIL), (PAQUETE_NORMAL, PAQUETE_COSTERO), "uniform_cost", 9, 5),
    ((CAMION_NORMAL, CAMION_INUTIL), (PAQUETE_NORMAL, PAQUETE_COSTERO), "astar", 9, 5),

    # un camion con mucho trabajo
    ((CAMION_NORMAL, ),
     (PAQUETE_NORMAL, PAQUETE_NORMAL2, PAQUETE_PASANDO_NORMAL, PAQUETE_INVERTIDO, PAQUETE_MOLESTO,
      PAQUETE_OPUESTO),
     "astar", 6, 20),
))
def test_itinerario_es_correcto(planear_camiones, metodo, camiones, paquetes, viajes_esperados,
                                limite_segs):
    mensaje_si_demora = (f"La prueba con método {metodo}, camiones {camiones} y paquetes "
                         f"{paquetes} demoró demasiado tiempo (más de {limite_segs} segundos), "
                         f"probablemente algo no está demasiado bien")

    with warning_si_demora(limite_segs, mensaje_si_demora):
        itinerario = planear_camiones(metodo, camiones, paquetes)

    # chequeamos la estructura de datos de forma muy básica
    assert isinstance(itinerario, list), \
           f"El resultado de planear_camiones no fue una lista, sino {itinerario}"
    for viaje in itinerario:
        assert isinstance(viaje, tuple), f"Un viaje del itinerario no es una tupla, sino {viaje}"
        assert len(viaje) == 4, f"Un viaje del itinerario no contiene 4 datos: {viaje}"

    # capacidad de combustible los camiones en forma de dict, para leerla rápido
    capacidad = {id_camion: maximo_combustible
                 for id_camion, ciudad_origen, maximo_combustible in camiones}

    # para simular el itinerario, vamos a necesitar ir trackeando ciudad y combustible actual de
    # cada camion.
    estado_actual = {id_camion: (ciudad_origen, maximo_combustible)
                     for id_camion, ciudad_origen, maximo_combustible in camiones}

    # para simular los movimietnos de paquetes, vamos a ir actualizando la ciudad actual de cada
    # paquete
    ciudad_actual_paquete = {id_paquete: ciudad_origen
                             for id_paquete, ciudad_origen, ciudad_destino in paquetes}

    # por cada viaje, hacemos chequeos y vamos simulando todo para ver que sea posible
    for viaje in itinerario:
        id_camion, ciudad_destino, consumo_viaje, paquetes_viaje = viaje

        # el camion debe existir
        assert id_camion in estado_actual, \
               f"El itinerario incluye un viaje de un camión que no existe: {viaje}"

        # todos los paquetes deben existir
        for id_paquete in paquetes_viaje:
            assert id_paquete in ciudad_actual_paquete, \
                   (f"El itinerario incluye un viaje con un paquete que no existe: {id_paquete} "
                    f"del viaje {viaje}")

        ciudad_actual, combustible_actual = estado_actual[id_camion]

        # validamos que el viaje se puede realizar por las conexiones en el mapa
        tramo = ciudad_actual, ciudad_destino
        assert tramo in TRAMOS_VALIDOS, \
               (f"El itinerario contiene un viaje que no es posible realizar: {viaje} desde "
                f"{ciudad_actual}")

        # validamos que el consumo de combustible sea el correcto
        consumo_esperado = DISTANCIAS[tramo] / 100
        assert consumo_viaje == consumo_esperado, \
               (f"El itinerario contiene un viaje con consumo incorrecto de combustible: {viaje} "
                f"desde {ciudad_actual}")

        # validamos que el camion pueda realizar el viaje con el combustible que tiene actualmente
        assert consumo_viaje <= combustible_actual, \
               ("Un viaje del itinerario tiene un consumo mayor al combustible que el camión "
                "tiene al partir de la ciudad actual, por lo que se quedaría sin combustible en "
                f"el medio de la ruta. Viaje {viaje} desde {ciudad_actual}, con combustible "
                f"actual={combustible_actual}")

        # validamos que los paquetes se encontraban en la ciudad de origen, y si es correcto,
        # actulizamos la ciudad actual del paquete
        for id_paquete in paquetes_viaje:
            ciudad_paquete = ciudad_actual_paquete[id_paquete]
            assert ciudad_paquete == ciudad_actual, \
                   ("Un viaje del itinerario está intentando mover un paquete que no se "
                    f"encuentra en la ciudad de origen del viaje. Paquete {id_paquete} en el "
                    f"viaje {viaje} desde {ciudad_actual}, cuando ese paquete está actualmente en "
                    f"{ciudad_paquete}")

            ciudad_actual_paquete[id_paquete] = ciudad_destino

        # actualizamos los datos del camión en la simulación
        ciudad_actual = ciudad_destino
        if ciudad_actual in SEDES:
            combustible_actual = capacidad[id_camion]
        else:
            combustible_actual -= consumo_viaje
        estado_actual[id_camion] = ciudad_actual, combustible_actual

    # validamos que todos los camiones terminen sus viajes en alguna sede
    for id_camion, (ciudad_actual, combustible_actual) in estado_actual.items():
        assert ciudad_actual in SEDES, \
               (f"El itinerario del camión {id_camion} no termina en una sede de la empresa, "
                f"sino en {ciudad_actual}")

    # validamos que todos los paquetes hayan terminado en su ciudad de destino
    for id_paquete, ciudad_origen, ciudad_destino in paquetes:
        ciudad_paquete = ciudad_actual_paquete[id_paquete]
        assert ciudad_paquete == ciudad_destino, \
               ("El itinerario deja un paquete sin llegar a su ciudad de destino. El paquete "
                f"{id_paquete} termina en {ciudad_paquete} pero debería terminar en "
                f"{ciudad_destino}")

    # validamos que la cantidad de viajes sea la esperada para el caso
    if viajes_esperados is not None:
        assert len(itinerario) == viajes_esperados, \
               (f"El itinerario construído tiene {len(itinerario)} viajes, pero para este caso "
                f"el largo esperado del itinerario es de {viajes_esperados}.")
