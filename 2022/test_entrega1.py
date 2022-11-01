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

    duracion_segs = int((fin - inicio).total_seconds())
    if limite_segs is not None and duracion_segs > limite_segs:
        warnings.warn(mensaje + f" [duración: {duracion_segs} segundos]")


@pytest.mark.dependency()
def test_modulo_existe():
    # Si falla este test es porque no se pudo encontrar el código python de la entrega.
    # Probablemente el nombre del archivo no es correcto (debe ser entrega1.py), o no está en la
    # raiz del repo, o no se están corriento los tests desde la raiz del repo.
    mensaje_si_demora = ("El import de la entrega demora demasiado tiempo, probablemente están "
                         "haciendo búsqueda en el import. Hagan lo del if __name__ ... que se "
                         "recomienda en la consigna")
    with warning_si_demora(1, mensaje_si_demora):
        import entrega1


@pytest.fixture()
def jugar():
    import entrega1
    funcion_jugar = getattr(entrega1, "jugar", None)

    return funcion_jugar


@pytest.mark.dependency(depends=["test_modulo_existe"])
def test_funcion_existe(jugar):
    assert jugar is not None, "La función jugar no existe"


@pytest.mark.dependency(depends=["test_funcion_existe"])
def test_funcion_bien_definida(jugar):
    parametros = list(signature(jugar).parameters)

    # los primeros parámetros de la función tienen que ser los pedidos
    assert parametros[:5] == ['paredes', 'cajas', 'objetivos', 'jugador', 'maximos_movimientos'], \
           "La función jugar no recibe los parámetros definidos en la entrega"


DIRECCIONES = {
    "arriba": (-1, 0),
    "abajo": (1, 0),
    "izquierda": (0, -1),
    "derecha": (0, 1),
}


def mover(posicion, direccion):
    f_actual, c_actual = posicion
    f_paso, c_paso = DIRECCIONES[direccion]
    return f_actual + f_paso, c_actual + c_paso



@pytest.mark.dependency(depends=["test_funcion_bien_definida"])
@pytest.mark.parametrize("tablero,maximos_movimientos,pasos_esperados,limite_segs", (
    # referencias de los tableros:
    # # = pared
    # o = objetivo
    # C = caja
    # j = jugador
    # @ = caja en objetivo

    # para testear que si el juego ya está ganado, no hay que hacer nada
    pytest.param(("######",
                  "#   @#"
                  "# @j #",
                  "#    #"
                  "######"), 10, 0, 3, id="juego_ganado_no_hacer_nada"),

    pytest.param(("#######",
                  "#     #"
                  "# oCj #",
                  "#     #"
                  "#######"), 10, 1, 3, id="1_caja_1_movimiento"),

    pytest.param(("#######",
                  "# o   #",
                  "#  C  #",
                  "#   j #",
                  "#######"), 10, 5, 3, id="1_caja_diagonal"),

    # para testear que permitan mover el jugador por sobre los objetivos
    pytest.param(("#######",
                  "#   # #",
                  "# Coj #",
                  "#   # #",
                  "#######"), 10, 6, 3, id="1_caja_pasando_objetivo"),

    pytest.param(("#######",
                  "#     #",
                  "# jCo #",
                  "# C   #",
                  "# o   #",
                  "#     #",
                  "#######"), 10, 3, 3, id="2_cajas_cerca"),

    pytest.param(("#######",
                  "#   j #",
                  "# C   #",
                  "#     #",
                  "#     #",
                  "#   o #",
                  "#######"), 20, 9, 3, id="1_caja_lejos"),

    pytest.param(("#######",
                  "# j   #",
                  "#   C #",
                  "#  ####",
                  "#  #o #",
                  "#     #",
                  "#     #",
                  "#######"), 30, 18, 3, id="1_caja_con_vueltas"),

    # para testear que no muevan cajas sobre cajas
    pytest.param(("##########",
                  "#        #",
                  "#        #",
                  "# ooCC j #",
                  "#        #",
                  "#        #",
                  "##########"), 30, 14, 10, id="2_cajas_requiere_desordenar"),

    pytest.param(("#######",
                  "# j   #",
                  "#   C #",
                  "# C####",
                  "#  #o #",
                  "#     #",
                  "#o    #",
                  "#######"), 30, 22, 3, id="2_cajas_con_vueltas"),

    # caso complicado pero que tienen que poder resolver
    pytest.param(("  ##### ",
                  "###   # ",
                  "# j   # ",
                  "### Co# ",
                  "#o##C # ",
                  "# # o ##",
                  "#C  CCo#",
                  "#   o  #",
                  "########"), 30, 23, 60, id="5_cajas_similar_consigna_simplificado"),

    # caso muy heavy, deshabilitado por el momento
    # pytest.param(("  ##### ",
                  # "###   # ",
                  # "#ojC  # ",
                  # "### Co# ",
                  # "#o##C # ",
                  # "# # o ##",
                  # "#C @CCo#",
                  # "#   o  #",
                  # "########"), 30, 1, 10, id="juego_grande_ejemplo_consigna"),
))
def test_plan_es_correcto(jugar, tablero, maximos_movimientos, pasos_esperados, limite_segs):
    paredes = set()
    cajas = set()
    objetivos = set()
    jugador = None
    for f, contenido_f in enumerate(tablero):
        for c, cosa in enumerate(contenido_f):
            posicion = f, c
            if cosa == "#":
                paredes.add(posicion)
            elif cosa == "o":
                objetivos.add(posicion)
            elif cosa == "C":
                cajas.add(posicion)
            elif cosa == "@":
                objetivos.add(posicion)
                cajas.add(posicion)
            elif cosa == "j":
                jugador = posicion

    mensaje_si_demora = (f"La prueba con paredes {paredes}, cajas {cajas}, objetivos {objetivos}, "
                         f"jugador {jugador} y maximos_movimientos {maximos_movimientos} demoró "
                         f"demasiado tiempo (más de {limite_segs} segundos), probablemente algo "
                         "no está demasiado bien")

    with warning_si_demora(limite_segs, mensaje_si_demora):
        secuencia = jugar(list(paredes), list(cajas), list(objetivos), jugador, maximos_movimientos)

    # chequeamos la estructura de datos de forma muy básica
    assert isinstance(secuencia, list), \
           f"El resultado de jugar no fue una lista, sino {type(secuencia)}"
    for paso in secuencia:
        assert isinstance(paso, str), f"Un paso del plan no es un string, sino {type(paso)}"
        assert paso in DIRECCIONES, f"Un paso del plan no es una dirección válida: {paso}"

    # para simular el plan, vamos a necesitar ir trackeando la posición y carga de cada robot
    estado = {
        "jugador": jugador,
        "cajas": cajas,
        "movimientos": 0,
    }

    # por cada paso, hacemos chequeos y vamos simulando todo para ver que sea posible
    for numero_paso, paso in enumerate(secuencia):
        print(estado)
        print(paso)
        # movemos al jugador
        estado["jugador"] = mover(estado["jugador"], paso)

        # el personaje tiene que poder moverse en esa dirección
        assert estado["jugador"] not in paredes, f"El paso {numero_paso} deja al jugador adentro de una pared"

        # si hay una caja...
        if estado["jugador"] in estado["cajas"]:
            # movemos la caja
            nueva_caja = mover(estado["jugador"], paso)

            # no debe haber otra cosa que impida mover la caja
            assert nueva_caja not in paredes, f"El paso {numero_paso} deja una caja adentro de una pared"
            assert nueva_caja not in estado["cajas"], f"El paso {numero_paso} deja una caja adentro de otra caja"

            # y aplicamos el cambio
            estado["cajas"].remove(estado["jugador"])
            estado["cajas"].add(nueva_caja)


    # validamos que no quedaron cajas sin ubicar
    assert estado["cajas"] == objetivos, f"La secuencia de pasos no ubica todas las cajas ({estado['cajas']} en los objetivos {objetivos}"

    # validamos que la cantidad de viajes sea la esperada para el caso
    if pasos_esperados is not None:
        assert len(secuencia) <= pasos_esperados, \
            f"La secuencia tiene {len(secuencia)} pasos, pero este caso puede resolverse en menos pasos: {pasos_esperados}"
