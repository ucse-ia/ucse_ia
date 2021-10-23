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
def rediseñar_robot():
    import entrega2
    funcion_planear = getattr(entrega2, "rediseñar_robot", None)

    return funcion_planear


@pytest.mark.dependency(depends=["test_modulo_existe"])
def test_funcion_existe(rediseñar_robot):
    assert rediseñar_robot is not None, "La función rediseñar_robot no existe"



@pytest.mark.dependency(depends=["test_funcion_existe"])
def test_resultado_es_correcto(rediseñar_robot):
    limite_segs = 30
    mensaje_si_demora = (
        f"La resolución demoró demasiado tiempo (más de {limite_segs} segundos), probablemente "
        "algo no está demasiado bien"
    )

    with warning_si_demora(limite_segs, mensaje_si_demora):
        mejoras = rediseñar_robot()

    # chequeamos la estructura de datos de forma muy básica
    assert isinstance(mejoras, (list, tuple)), \
           f"El resultado de rediseñar_robot no fue una lista o tupla, sino {type(mejoras)}"

    assert len(mejoras) == 4, f"La solución solo debería contener 4 mejoras, no: {len(mejoras)}"
    assert len(set(mejoras)) == 4, f"La solución contiene mejoras repetidas"

    mejoras_conocidas = (
        "baterias_chicas",
        "baterias_medianas",
        "baterias_grandes",
        "patas_extras",
        "mejores_motores",
        "orugas",
        "caja_superior",
        "caja_trasera",
        "radios",
        "video_llamadas",
    )

    for mejora in mejoras:
        assert isinstance(mejora, str), f"Una mejora devuelta no es un string, sino {type(mejora)}"
        assert mejora in mejoras_conocidas, f"Una mejora devuelta no es conocida: {mejora}"

    # y validamos que se lograron los objetivos
    consumo_base = 100
    baterias_base = 1000
    mejoras_movimientos = "patas_extras", "mejores_motores", "orugas"
    mejoras_cajas = "caja_superior", "caja_trasera"
    mejoras_comunicaciones = "radios", "video_llamadas"
    consumos_extras = {
        "baterias_chicas": 10,
        "baterias_medianas": 20,
        "baterias_grandes": 50,
        "patas_extras": 15,
        "mejores_motores": 25,
        "orugas": 50,
        "caja_superior": 10,
        "caja_trasera": 10,
        "radios": 5,
        "video_llamadas": 10,
    }
    incrementos_baterias = {
        "baterias_chicas": 4000,
        "baterias_medianas": 6500,
        "baterias_grandes": 9000,
    }

    consumo_resultante = consumo_base + sum(consumos_extras[mejora]
                                            for mejora in mejoras)
    baterias_resultantes = baterias_base + sum(incrementos_baterias.get(mejora, 0)
                                               for mejora in mejoras)
    autonomia_resultante = baterias_resultantes / consumo_resultante

    assert autonomia_resultante >= 50, \
           f"La autonomía lograda no es suficiente: {autonomia_resultante} minutos"

    assert any(mejora in mejoras_movimientos for mejora in mejoras), \
           f"La solución no incluye ninguna mejora que permita moverse sobre terreno irregular"
    assert any(mejora in mejoras_cajas for mejora in mejoras), \
           f"La solución no incluye ninguna mejora que permita llevar suministros para sobrevivientes"
    assert any(mejora in mejoras_comunicaciones for mejora in mejoras), \
           f"La solución no incluye ninguna mejora que permita comunicarse con los sobrevivientes"

    assert "baterias_grandes" not in mejoras or "orugas" in mejoras, \
           "No es posible utilizar las baterías grandes sin utilizar las orugas"
    assert not ("caja_trasera" in mejoras and "patas_extras" in mejoras), \
           "No es posible utilizar las patas extras junto con la caja trasera"
    assert not ("mejores_motores" in mejoras and "radios" in mejoras), \
           "No es posible utilizar los motores más potentes junto con el sistema de radio"
    assert not ("video_llamadas" in mejoras and "mejores_motores" in mejoras), \
           "No es posible utilizar los motores más potentes junto con el sistema de video llamadas"


