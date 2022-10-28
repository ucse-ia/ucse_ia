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
    # Probablemente el nombre del archivo no es correcto (debe ser entrega2.py), o no está en la
    # raiz del repo, o no se están corriento los tests desde la raiz del repo.
    mensaje_si_demora = ("El import de la entrega demora demasiado tiempo, probablemente están "
                         "haciendo búsqueda en el import. Hagan lo del if __name__ ... que se "
                         "recomienda en la consigna")
    with warning_si_demora(1, mensaje_si_demora):
        import entrega2


@pytest.fixture()
def armar_mapa():
    import entrega2
    funcion_armar_mapa = getattr(entrega2, "armar_mapa", None)

    return funcion_armar_mapa


@pytest.mark.dependency(depends=["test_modulo_existe"])
def test_funcion_existe(armar_mapa):
    assert armar_mapa is not None, "La función armar_mapa no existe"


@pytest.mark.dependency(depends=["test_funcion_existe"])
def test_funcion_bien_definida(armar_mapa):
    parametros = list(signature(armar_mapa).parameters)

    # los primeros parámetros de la función tienen que ser los pedidos
    assert parametros[:4] == ['filas', 'columnas', 'cantidad_paredes', 'cantidad_cajas_objetivos'], \
           "La función armar_mapa no recibe los parámetros definidos en la entrega"


def posicion_ok(cosa, filas, columnas):
    return (
        isinstance(cosa, tuple)
        and len(cosa) == 2
        and all(isinstance(coordenada, int) for coordenada in cosa)
        and 0 <= cosa[0] <= filas
        and 0 <= cosa[1] <= columnas
    )


@pytest.mark.dependency(depends=["test_funcion_bien_definida"])
@pytest.mark.parametrize("filas,columnas,cantidad_paredes,cantidad_cajas_objetivos,limite_segs", (
    # super simple, una caja en 3x3 y una sola pared
    pytest.param(3, 3, 1, 1, 1, id="caso_super_simple"),
    # caso más mediano, varias cajas y paredes en 5x5
    pytest.param(5, 5, 4, 3, 10, id="caso_mediano"),
    # caso más grande, como de la consigna
    pytest.param(9, 8, 12, 7, 60, id="caso_consigna"),
))
def test_resultado_es_correcto(armar_mapa, filas, columnas, cantidad_paredes, cantidad_cajas_objetivos, limite_segs):
    mensaje_si_demora = (
        f"La resolución demoró demasiado tiempo (más de {limite_segs} segundos), probablemente "
        "algo no está demasiado bien"
    )

    with warning_si_demora(limite_segs, mensaje_si_demora):
        resultado = armar_mapa(filas, columnas, cantidad_paredes, cantidad_cajas_objetivos)

    # chequeamos la estructura de datos de forma muy básica
    assert isinstance(resultado, (list, tuple)), \
           f"El resultado de armar_mapa no fue una lista o tupla, sino {type(resultado)}"

    assert len(resultado) == 4, f"El resultado debe solo contener 4 elementos, no: {len(resultado)}"
    res_paredes, res_cajas, res_objetivos, res_jugador = resultado

    assert len(res_paredes) == cantidad_paredes, f"El resultado no tiene la cantidad esperada de paredes: {len(res_paredes)}"
    assert all(posicion_ok(pared, filas, columnas) for pared in res_paredes), f"El resultado contiene paredes que no son posiciones válidas: {res_paredes}"
    assert all(posicion_ok(caja, filas, columnas) for caja in res_cajas), f"El resultado contiene cajas que no son posiciones válidas: {res_cajas}"
    assert all(posicion_ok(objetivo, filas, columnas) for objetivo in res_objetivos), f"El resultado contiene objetivos que no son posiciones válidas: {res_objetivos}"
    assert posicion_ok(res_jugador, filas, columnas), f"El resultado contiene una posición inválida para el jugador: {res_jugador}"

    assert len(set(res_paredes)) == cantidad_paredes, f"El resultado contiene paredes en posiciones repetidas: {res_paredes}"
    assert len(set(res_cajas)) == cantidad_cajas_objetivos, f"El resultado contiene cajas en posiciones repetidas: {res_cajas}"
    assert len(set(res_objetivos)) == cantidad_cajas_objetivos, f"El resultado contiene objetivos en posiciones repetidas: {res_objetivos}"

    assert res_jugador not in res_cajas, f"El jugador comienza en una posicion ocupada por una caja: {res_jugador}"
    assert res_jugador not in res_paredes, f"El jugador comienza en una posicion ocupada por una pared: {res_jugador}"

    esquinas = (
        (0, 0),
        (0, columnas - 1),
        (filas - 1, 0),
        (filas - 1, columnas - 1),
    )
    for esquina in esquinas:
        assert esquina not in res_cajas, f"El resultado posee una caja en una esquina: {esquina}"

    for caja in res_cajas:
        adyacentes = []
        for pared in res_paredes:
            if abs(caja[0] - pared[0]) + abs(caja[1] - pared[1]) == 1:
                adyacentes.append(pared)
        if caja[0] in (0, filas - 1) or caja[1] in (0, columnas - 1):
            assert len(adyacentes) == 0, f"La caja que está en el borde {caja} tiene paredes adyacentes: {adyacentes}, pero no debería tener ninguna"
        else:
            assert len(adyacentes) < 2, f"La caja {caja} tiene demasiadas paredes adyacentes: {adyacentes}, no debería tener más de una."

    assert set(res_cajas) != set(res_objetivos), f"El resultado es un mapa ya ganado: cajas en {res_cajas} y objetivos en {res_objetivos}"
