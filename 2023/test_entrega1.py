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
    assert parametros[:6] == ["filas", "columnas", "pisos", "salida", "piezas", "pieza_sacar"], \
           "La función jugar no recibe los parámetros definidos en la entrega"


DELTAS = {
    "arriba": (0, -1, 0),
    "abajo": (0, 1, 0),
    "izquierda": (0, 0, -1),
    "derecha": (0, 0, 1),
    "trepar": (1, 0, 0),
    "caer": (-1, 0, 0),
}


class NoPuedeMoverException(Exception):
    pass


def crear_tablero(pisos, filas, columnas, piezas):
    tablero = {
        (idx_piso, idx_fila, idx_columna): None
        for idx_piso in range(pisos)
        for idx_fila in range(filas)
        for idx_columna in range(columnas)
    }

    for pieza in piezas:
        for fila_parte, columna_parte in pieza["partes"]:
            idx = pieza["piso"], fila_parte, columna_parte
            assert tablero[idx] is None
            tablero[idx] = pieza["id"]

    return tablero


def mover(tablero, pieza_mover, movimiento, limites):
    nuevo_tablero = dict(tablero.items())

    # sacar la pieza del lugar actual
    for idx, pieza_actual in tablero.items():
        if pieza_actual == pieza_mover:
            nuevo_tablero[idx] = None

    # agregarla en el nuevo lugar
    delta_piso, delta_fila, delta_columna = DELTAS[movimiento]
    for (idx_piso, idx_fila, idx_columna), pieza_actual in tablero.items():
        if pieza_actual == pieza_mover:
            nuevo_idx = idx_piso + delta_piso, idx_fila + delta_fila, idx_columna + delta_columna
            for nuevo_valor_idx, limite in zip(nuevo_idx, limites):
                if not 0 <= nuevo_valor_idx < limite:
                    raise NoPuedeMoverException("Fuera de tablero")

            if nuevo_tablero[nuevo_idx] != None:
                raise NoPuedeMoverException(f"Ocupado por pieza {nuevo_tablero[nuevo_idx]}")
            nuevo_tablero[nuevo_idx] = pieza_mover

    return nuevo_tablero


def dibujar(tablero, pisos, filas, columnas):
    for piso in reversed(range(pisos)):
        print("  PISO", piso)
        for fila in range(filas):
            print("    ", end="")
            for columna in range(columnas):
                print(tablero[piso, fila, columna] or "#", end="")
            print()


@pytest.mark.dependency(depends=["test_funcion_bien_definida"])
@pytest.mark.parametrize("pisos_tablero,pasos_esperados,limite_segs", (
    # referencias de los tableros:
    # - # = nada
    # - letra = pieza con ese id
    # - la pieza a sacar es siempre la pieza "A"
    # - la salida está siempre en (piso=0, fila=0, columna=0)
    # - los pisos están dibujados en orden invertido, 0 es el de abajo, para mejor visibilidad

    # para testear que si el juego ya está ganado, no hay que hacer nada

    # con una pieza super simple de 1x1
    pytest.param((
        ("A##",
         "###"),
    ), 0, 3),

    # con una pieza de más partes
    pytest.param((
        ("AA#",
         "#A#"),
    ), 0, 3),


    # casos super simples donde solo tenemos la pieza a sacar, y hay que moverla

    # con un solo piso y pieza de 1x1
    pytest.param((
        ("###",
         "##A"),
    ), 3, 5),

    # un solo piso y pieza de más partes
    pytest.param((
        ("###",
         "#AA"),
    ), 2, 5),

    # con dos pisos y pieza de 1x1
    pytest.param((
        ("###",
         "##A"),
        ("###",
         "###"),
    ), 4, 5),

    # con dos pisos y pieza de más partes
    pytest.param((
        ("#AA",  # piso 1, superior
         "##A"),
        ("###",  # piso 0, inferior
         "###"),
    ), 2, 5),

    # casos simples pero ya sumando más de una pieza

    # con un solo piso
    pytest.param((
        ("CB#",
         "#AA"),
    ), 6, 10),

    # con dos pisos
    pytest.param((
        ("BB#",
         "#AA"),
        ("DC#",
         "D##"),
    ), 6, 10),

    # casos más complicados :D

    pytest.param((
        ("###E",
         "A#EE",
         "AAE#"),
        ("#C##",
         "#C##",
         "#CDD"),
        ("BBFF",
         "BB##",
         "####"),
    ), 8, 60),

))
def test_resultado_es_correcto(jugar, pisos_tablero, pasos_esperados, limite_segs):
    pisos = len(pisos_tablero)
    filas = len(pisos_tablero[0])
    columnas = len(pisos_tablero[0][0])
    salida = 0, 0, 0
    pieza_sacar = "A"
    piezas_by_id = {}
    for idx_piso, piso in enumerate(reversed(pisos_tablero)):  # invertidos para mejor visual
        for idx_fila, fila in enumerate(piso):
            for idx_columna, id_pieza in enumerate(fila):
                if id_pieza != "#":
                    if id_pieza not in piezas_by_id:
                        piezas_by_id[id_pieza] = {"id": id_pieza, "piso": idx_piso, "partes": []}
                    pieza = piezas_by_id[id_pieza]
                    pieza["partes"].append((idx_fila, idx_columna))
    piezas = list(piezas_by_id.values())

    mensaje_si_demora = (f"La prueba con tablero {pisos_tablero} demoró demasiado tiempo "
                         f"(más de {limite_segs} segundos), probablemente algo no está bien")

    with warning_si_demora(limite_segs, mensaje_si_demora):
        secuencia = jugar(filas, columnas, pisos, salida, piezas, pieza_sacar)

    # chequeamos la estructura de datos de forma muy básica
    assert isinstance(secuencia, list), \
           f"El resultado de jugar no fue una lista, sino {type(secuencia)}"
    for paso in secuencia:
        assert isinstance(paso, tuple), f"Un paso del resultado no es una tupla, sino {type(paso)}"
        assert len(paso) == 2, f"Un paso del resultado no es una tupla de 2 elementos, sino {paso}"
        pieza_mover, movimiento = paso
        assert pieza_mover in piezas_by_id, f"Un paso del resultado pide mover un id de pieza inválido: {pieza_mover}"
        assert movimiento in DELTAS, f"Un paso del resultado pide realizar un movimiento inválido: {movimiento}"

    # para simular el resultado, vamos a necesitar un tablero
    tablero = crear_tablero(pisos, filas, columnas, piezas)
    limites = pisos, filas, columnas

    dibujar(tablero, pisos, filas, columnas)

    # por cada paso, hacemos chequeos y vamos simulando todo para ver que sea posible
    for numero_paso, paso in enumerate(secuencia):
        pieza_mover, movimiento = paso

        # movemos la pieza
        try:
            tablero = mover(tablero, pieza_mover, movimiento, limites)
        except NoPuedeMoverException as err:
            pytest.fail(f"El paso {numero_paso} no es posible. Motivo: {err}.")

        print()
        print("PASO", numero_paso, ":", pieza_mover, "→", movimiento)
        dibujar(tablero, pisos, filas, columnas)

    # validamos que la pieza deseada fue sacada
    assert tablero[salida] == pieza_sacar, f"El resultado final de aplicar todos los movimientos no deja a la pieza {pieza_sacar} en la salida {salida}"

    # validamos que la cantidad de pasos sea la esperada para el caso
    if pasos_esperados is not None:
        assert len(secuencia) <= pasos_esperados, \
            f"La secuencia tiene {len(secuencia)} pasos, pero este caso puede resolverse en menos pasos: {pasos_esperados}"
