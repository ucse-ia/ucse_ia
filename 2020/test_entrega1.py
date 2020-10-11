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


@pytest.mark.dependency(depends=["test_funcion_bien_definida"])
@pytest.mark.parametrize("camiones", (
    # un camion
    [("c1", "rafaela", 1.5)],
    # un camion normal y uno que no llega a nada
    [("c1", "rafaela", 1.5), ("c2", "rafaela", 0.002)],
    # un camion normal y uno que no se le acaba nunca el combustible
    [("c1", "rafaela", 1.5), ("c2", "santa_fe", 9999)],
))
@pytest.mark.parametrize("paquetes", (
    # un paquete
    [("p1", "rafaela", "lehmann")],
    # un paquete con recorrido complicado
    [("p1", "sunchales", "susana")],
    # un paquete con recorrido que requiere recarga
    [("p1", "sunchales", "sauce_viejo")],
    # dos paquetes con igual recorrido
    [("p1", "rafaela", "lehmann"), ("p2", "rafaela", "lehmann")],
    # dos paquetes con recorrido compartido
    [("p1", "rafaela", "lehmann"), ("p2", "rafaela", "sunchales")],
    # dos paquetes con viajes muy diferentes
    [("p1", "rafaela", "lehmann"), ("p2", "susana", "angelica")],
    # paquetes buenos para distribuir trabajo entre camiones
    [("p1", "lehmann", "sunchales"), ("p2", "santo_tome", "recreo")],
    # muchos paquetes
    [("p1", "rafaela", "susana"), ("p2", "rafaela", "susana"), ("p3", "susana", "angelica"),
     ("p4", "rafaela", "angelica"), ("p5", "rafaela", "susana"), ("p6", "susana", "rafaela"),
     ("p7", "angelica", "rafaela")],
))
@pytest.mark.parametrize("metodo", (
    "astar",
    "uniform_cost",
))
def test_itinerario_es_correcto(planear_camiones, metodo, camiones, paquetes):
    if metodo != "astar" and len(paquetes) > 2:
        pytest.skip("No testeamos los casos con muchos paquetes donde no se use A*, por lo que "
                    "demoran")

    if len(paquetes) <= 2:
        # casos simples, que deberían demorar poco
        limite_segs = 10
    else:
        limite_segs = None

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
