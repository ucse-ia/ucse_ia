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
        try:
            import entrega2
        except ModuleNotFoundError:
            pytest.fail("No se encuentra el módulo entrega2.py")


@pytest.fixture()
def armar_nivel():
    import entrega2
    funcion_armar_nivel = getattr(entrega2, "armar_nivel", None)

    return funcion_armar_nivel


@pytest.mark.dependency(depends=["test_modulo_existe"])
def test_funcion_existe(armar_nivel):
    assert armar_nivel is not None, "La función armar_nivel no existe"


@pytest.mark.dependency(depends=["test_funcion_existe"])
def test_funcion_bien_definida(armar_nivel):
    parametros = list(signature(armar_nivel).parameters)
    parametros_esperados = ["colores", "contenidos_parciales"]

    # los primeros parámetros de la función tienen que ser los pedidos
    assert parametros[:len(parametros_esperados)] == parametros_esperados, \
           "La función armar_nivel no recibe los parámetros definidos en la entrega"



@pytest.mark.dependency(depends=["test_funcion_bien_definida"])
@pytest.mark.parametrize("colores,contenidos_parciales,limite_segs", (
    # en cada caso los frascos están especificados usando una letra para cada color en un string
    # por cada frasco, para mayor facilidad de lectura (luego en el test se "expanden")

    # ejemplos bien chicos con solo 4 colores
    ("RVAC", [], 5),
    ("RVAC", ["RR"], 5),
    ("RVAC", ["RRVA", "RVC", "AA"], 5),

    # casos medianos con 5 colores
    ("RVACL", [], 30),
    ("RVACL", ["AC"], 30),
    ("RVACL", ["RRVA"], 30),

    # caso bastente más complejo con 8 colores
    ("RVACLNMO", ["ROOO", "CAA", "NOVA", "MM", "C"], 60),
))
def test_resultado_es_correcto(armar_nivel, colores, contenidos_parciales, limite_segs):
    letras_a_colores = {
        "R": "rojo",
        "V": "verde",
        "A": "azul",
        "C": "celeste",
        "L": "lila",
        "N": "naranja",
        "M": "amarillo",
        "B": "beige",
        "S": "rosado",
        "O": "verde_oscuro",
    }
    colores = tuple(letras_a_colores[letra] for letra in colores)
    contenidos_parciales = tuple(
        tuple(letras_a_colores[letra] for letra in frasco)
        for frasco in contenidos_parciales
    )

    mensaje_si_demora = (f"La prueba con colores {colores} y contenidos parciales {contenidos_parciales} "
                         f"demoró demasiado tiempo (más de {limite_segs} segundos), probablemente "
                         "algo no está bien")

    print()
    print("Colores:", colores)
    print("Contenidos parciales:", contenidos_parciales)
    with warning_si_demora(limite_segs, mensaje_si_demora):
        resultado = armar_nivel(colores, contenidos_parciales)

        print("Resultado obtenido:", resultado)

    print()

    # chequeamos la estructura de datos de forma muy básica

    assert isinstance(resultado, (list, tuple)), \
           f"El resultado de armar_nivel no fue una lista, sino {type(resultado)}"
    assert len(resultado) == len(colores), \
           f"El resultado tiene una cantidad incorrecta de frascos: {len(resultado)}, {resultado}"

    for frasco in resultado:
        assert isinstance(frasco, (list, tuple)), \
               f"El resultado de armar_nivel contiene un frasco que no es una tupla, sino {type(frasco)}: {frasco}"
        assert len(frasco) == 4, \
               f"El resultado tiene un frasco con una cantidad incorrecta de segmentos: {len(frasco)} {frasco}"
        for color in frasco:
            assert color in colores, \
                   f"El resultado de armar_nivel contiene un color que no es válido: {color}"

    cantidad_por_color = {color: 0 for color in colores}
    fondos_por_color = {color: 0 for color in colores}

    for frasco in resultado:
        fondos_por_color[frasco[0]] += 1

        cantidad_colores = len(set(frasco))
        assert cantidad_colores != 1, f"El resultado contiene un frasco resuelto: {frasco}"

        for color in frasco:
            cantidad_por_color[color] += 1

    for color, cantidad in cantidad_por_color.items():
        assert cantidad <= 4, \
               f"El resultado tiene demasiados segmentos de color {color}: {cantidad}"

    for color, cantidad in fondos_por_color.items():
        assert cantidad < cantidad_por_color[color], \
               f"El color {color} tiene todos sus segmentos en el fondo de frascos"

    for frasco1, frasco2 in zip(resultado, resultado[1:]):
        assert any((color1 in frasco2) for color1 in frasco1), \
               f"El resultado contiene frascos adyacentes que no comparten ningún color: {frasco1} vs {frasco2}"

        cantidad_colores = len(set(frasco1 + frasco2))
        assert cantidad_colores <= 6, \
               f"El resultado contiene frascos adyacentes que suman más de 6 colores diferentes entre si: {frasco1} vs {frasco2}"

    for frasco1, frasco2 in combinations(resultado, 2):
        assert frasco1 != frasco2, f"El resultado contiene dos frascos iguales: {frasco1} vs {frasco2}"

    if contenidos_parciales:
        for idx, (template, frasco) in enumerate(zip(contenidos_parciales, resultado)):
            assert tuple(frasco[:len(template)]) == template, \
                   f"El frasco {idx + 1} no respeta los contenidos parciales pedidos: {frasco} vs {template}"
