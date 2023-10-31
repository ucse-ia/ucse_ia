import argparse
import importlib.util
import logging
import os
import sys
import warnings
from contextlib import contextmanager
from datetime import datetime
from inspect import signature
from itertools import combinations, chain

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
    # Probablemente el nombre del archivo no es correcto (debe ser entrega2.py), o no está en la
    # raiz del repo, o no se están corriento los tests desde la raiz del repo.
    mensaje_si_demora = ("El import de la entrega demora demasiado tiempo, probablemente están "
                         "haciendo búsqueda en el import. Hagan lo del if __name__ ... que se "
                         "recomienda en la consigna")
    with warning_si_demora(1, mensaje_si_demora):
        import entrega2


@pytest.fixture()
def armar_tablero():
    import entrega2
    funcion_armar_tablero = getattr(entrega2, "armar_tablero", None)

    return funcion_armar_tablero


@pytest.mark.dependency(depends=["test_modulo_existe"])
def test_funcion_existe(armar_tablero):
    assert armar_tablero is not None, "La función armar_tablero no existe"


@pytest.mark.dependency(depends=["test_funcion_existe"])
def test_funcion_bien_definida(armar_tablero):
    parametros = list(signature(armar_tablero).parameters)

    # los primeros parámetros de la función tienen que ser los pedidos
    assert parametros[:6] == ["filas", "columnas", "pisos", "salida", "piezas", "pieza_sacar"], \
           "La función armar_tablero no recibe los parámetros definidos en la entrega"


DELTAS_PARTES = {
    # delta fila, delta columna
    "L": ((0, 0), (1, 0), (1, 1)),
    "T": ((0, 0), (0, 1), (0, 2), (1, 1)),
    "O": ((0, 0), (0, 1), (1, 0), (1, 1)),
    "I": ((0, 0), (1, 0), (2, 0)),
    "-": ((0, 0), (0, 1), (0, 2)),
    "Z": ((0, 0), (0, 1), (1, 1), (1, 2)),
    ".": ((0, 0),),
}


def posiciones_actuales(posicion_esquina, forma):
    piso, fila, columna = posicion_esquina
    return tuple(
        (piso, fila + delta_fila, columna + delta_columna)
        for delta_fila, delta_columna in DELTAS_PARTES[forma]
    )


@pytest.mark.dependency(depends=["test_funcion_bien_definida"])
@pytest.mark.parametrize("pisos,filas,columnas,formas_piezas,limite_segs", (
    # la salida siempre es 0,0,0 y la pieza a sacar siempre es p0

    # casos super simples con dos piezas y espacio de sobra
    # (no se puede resolver de ninguna forma un caso con una sola pieza)

    (2, 2, 2, "..", 5),
    (2, 3, 3, "LL", 5),
    (2, 3, 3, "TT", 5),
    (2, 3, 3, "OO", 5),
    (2, 3, 3, "II", 5),
    (2, 3, 3, "--", 5),
    (2, 3, 3, "ZZ", 5),

    # casos con combinaciones un poco más difíciles de piezas, pero que deberían salir muy rápido

    (2, 3, 4, "TOZ.-", 10),
    (3, 3, 4, "TTZZ", 10),
    (3, 4, 4, "OOOOOO", 10),
    (2, 4, 4, "------", 10),
    (2, 4, 5, "ZZZZZZ", 10),
    (2, 5, 3, "LT---.", 10),

    # caso que puede llevar un poco más de tiempo si no tienen suerte o no está tan bien hecho

    (3, 4, 5, "OOLLTIIZZ--.", 60),
))
def test_resultado_es_correcto(armar_tablero, pisos, filas, columnas, formas_piezas, limite_segs):
    salida = 0, 0, 0
    pieza_sacar = "p0"
    piezas = {
        f"p{n_pieza}": forma
        for n_pieza, forma in enumerate(formas_piezas)
    }
    piezas_param = tuple(piezas.items())

    mensaje_si_demora = (f"La prueba con piezas {formas_piezas} demoró demasiado tiempo "
                         f"(más de {limite_segs} segundos), probablemente algo no está bien")

    print("Piezas a utilizar:", piezas_param)
    print("Salida:", salida)
    print("Pieza a sacar:", pieza_sacar)
    print("Tamaño tablero (pisos filas columnas):", pisos, filas, columnas)
    with warning_si_demora(limite_segs, mensaje_si_demora):
        resultado = armar_tablero(filas, columnas, pisos, salida, piezas_param, pieza_sacar)

        print("Resultado obtenido:", resultado)

    # chequeamos la estructura de datos de forma muy básica
    assert isinstance(resultado, dict), \
           f"El resultado de armar_tablero no fue un diccionario, sino {type(resultado)}"
    for id_pieza, posicion_esquina in resultado.items():
        assert id_pieza in piezas, f"El resultado contiene una pieza que no existe: {id_pieza}"
        assert isinstance(posicion_esquina, tuple), f"El resultado contiene una posición que no es una tupla: {posicion_esquina}"
        assert len(posicion_esquina) == 3, f"Una posición del resultado no es una tupla de 3 elementos: {posicion_esquina}"

    partes = {
        id_pieza: posiciones_actuales(posicion_esquina, piezas[id_pieza])
        for id_pieza, posicion_esquina in resultado.items()
    }

    for pieza1, pieza2 in combinations(piezas, 2):
        assert not (set(partes[pieza1]) & set(partes[pieza2])), f"El resultado tiene piezas pisándose: {pieza1} y {pieza2}"

    piezas_por_piso = {
        piso: 0
        for piso in range(pisos)
    }
    partes_por_piso = piezas_por_piso.copy()
    max_casilleros_piso = (filas * columnas) * (2/3)

    for id_pieza in piezas:
        piso_pieza = resultado[id_pieza][0]
        assert 0 <= piso_pieza < pisos, f"El resultado tiene una pieza ({id_pieza}) un piso inexistente: {piso_pieza}"

        piezas_por_piso[piso_pieza] += 1

        if id_pieza == pieza_sacar:
            assert piso_pieza != salida[0], f"El resultado tiene la pieza a sacar ({id_pieza}) en el piso de la salida {salida}"

        for parte in partes[id_pieza]:
            _, fila, columna = parte
            partes_por_piso[piso_pieza] += 1
            assert parte != salida, f"El resultado tiene una pieza ({id_pieza}) con una parte sobre el casillero de salida {salida}"
            assert 0 <= fila < filas, f"El resultado tiene una pieza ({id_pieza}) con una parte en una fila inexistente: {piso_pieza, fila, columna}"
            assert 0 <= columna < columnas, f"El resultado tiene una pieza ({id_pieza}) con una parte en una columna inexistente: {piso_pieza, fila, columna}"

    for piso in range(pisos):
        piezas_en_piso = piezas_por_piso[piso]
        partes_en_piso = partes_por_piso[piso]
        assert piezas_en_piso > 0, f"El resultado deja el piso {piso} sin piezas, todos los pisos deben tener piezas"
        assert partes_en_piso <= max_casilleros_piso, f"El resultado deja un piso con más casilleros ocupados que el máximo permitido (dos tercios): piso {piso} con {partes_en_piso} casilleros usados"

    for (piso_a, piezas_piso_a), (piso_b, piezas_piso_b) in combinations(piezas_por_piso.items(), 2):
        assert 0.5 <= piezas_piso_a / piezas_piso_b <= 2, f"El resultado deja un piso con más del doble de piezas que otro piso (piso {piso_a} con {piezas_piso_a}, {piso_b} con {piezas_piso_b}"
