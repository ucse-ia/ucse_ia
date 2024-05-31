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
        try:
            import entrega1
        except ImportError:
            pytest.fail("No se encuentra el módulo entrega1.py")


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
    parametros_esperados = ["frascos", "dificil"]

    # los primeros parámetros de la función tienen que ser los pedidos

    assert parametros[:len(parametros_esperados)] == parametros_esperados, \
           "La función jugar no recibe los parámetros definidos en la entrega"


CAPACIDAD_FRASCOS = 4

def dibujar(frascos):
    """Utilidad simple para dibujar frascos fácilmente."""
    # números de frascos
    lineas = ["".join(str(n + 1).center(3)
                      for n in range(len(frascos)))]

    # contenidos de los frascos
    for linea_actual in range(CAPACIDAD_FRASCOS):
        linea = ""
        for frasco in frascos:
            if len(frasco) > linea_actual:
                linea += f"[{frasco[linea_actual][0].upper()}]"
            else:
                linea += "[ ]"
        lineas.append(linea)

    # tapas
    lineas.append("".join(
        "<=>" if len(frasco) == CAPACIDAD_FRASCOS and len(set(frasco)) == 1 else "   "
        for frasco in frascos
    ))

    lineas.reverse()
    print(*lineas, sep="\n")


@pytest.mark.dependency(depends=["test_funcion_bien_definida"])
@pytest.mark.parametrize("frascos,dificil,pasos_esperados,limite_segs", (
    # en cada caso los frascos están especificados usando una letra para cada color en un string
    # por cada frasco, para mayor facilidad de lectura (luego en el test se "expanden")

    # casos artificiales super simples donde un solo movimiento alcanza
    # ...con un solo color
    (("RRR", "R"), False, 1, 3),
    (("RR", "RR"), False, 1, 3),
    (("RRR", "R", ""), False, 1, 3),
    # ...con tres colores
    (("RRR", "R", "VVVV", "AAAA"), False, 1, 3),
    (("RR", "RR", "VVVV", "AAAA"), False, 1, 3),
    (("RRR", "R", "VVVV", "AAAA", ""), False, 1, 3),

    # casos artificiales que requieren muy pocos pasos, casi listos de resolver
    (("RRR", "R", "VV", "AA", "VV", "AA"), False, 3, 5),
    (("RRR", "R", "VV", "AA", "VVAA"), False, 3, 5),
    (("RRRV", "RVVV", ""), False, 3, 5),
    (("VVV", "AAA", "NNNN", "", "RRRR", "VOOO", "AO", "LLLL", "BBBB"), False, 4, 10),

    # casos artificiales chicos pero ya requiriendo un poco más de pensar a futuro
    (("VVVR", "AAAR", "LLLR", "LVAR", ""), False, 7, 15),
    (("RVVV", "RAAA", "RLLL", "RLVA", "", ""), False, 9, 20),

    # casos reales
    # ...re simple de niel 5
    (("NNNA", "VVNA", "VSVA", "SLLA", "SSLL", "", ""), False, 11, 20),
    # ...simple de nivel 10
    (("NNCN", "SVNC", "ARSC", "ARVS", "RARV", "ALCL", "VSLL", "", ""), True, None, 30),
    # ...medio de nivel 51
    (("ANSA", "NLVA", "CRNR", "SNAV", "RVLS", "VCRL", "SCLC", "", ""), True, None, 60),
    # ...complicado de nivel 100
    (("BCOS", "OLOB", "LVCR", "VRLS", "SCNL", "CNSN", "ANAV", "AMRM", "BVAM", "MROB", "", ""), True, None, 120),
    # ...super complicado de nivel 414
    (("VACN", "ORLN", "OBCS", "SANS", "MSVO", "RMBC", "VARL", "OBNL", "MBAR", "CVLM", "", ""), True, None, 300),
))
def test_resultado_es_correcto(jugar, frascos, dificil, pasos_esperados, limite_segs):
    # convertimos los frascos en formato simplificado al formato de la consigna
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
    frascos = tuple(
        tuple(letras_a_colores[letra] for letra in frasco)
        for frasco in frascos
    )

    mensaje_si_demora = (f"La prueba con frascos {frascos} demoró demasiado tiempo "
                         f"(más de {limite_segs} segundos), probablemente algo no está bien")

    with warning_si_demora(limite_segs, mensaje_si_demora):
        pasos = jugar(frascos, dificil)

    # chequeamos la estructura de datos de forma muy básica
    frascos_validos = set(range(1, len(frascos) + 1))
    assert isinstance(pasos, (list, tuple)), \
           f"El resultado de jugar no fue una lista, sino {type(pasos)}"
    for paso in pasos:
        assert isinstance(paso, (list, tuple)), f"Un paso del resultado no es una tupla, sino {type(paso)}"
        assert len(paso) == 2, f"Un paso del resultado no es una tupla de 2 elementos, sino {paso}"
        origen, destino = paso
        assert origen in frascos_validos, f"Un paso del resultado pide transferir desde un frasco inválido: {origen}"
        assert destino in frascos_validos, f"Un paso del resultado pide transferir hacia un frasco inválido: {destino}"
        assert origen != destino, f"Un paso del resultado pide transferir desde un frasco hacia si mismo: {origen}"

    # para simular el resultado, vamos a necesitar frascos mutables
    frascos = [list(frasco) for frasco in frascos]
    dibujar(frascos)

    # por cada paso, hacemos chequeos y vamos simulando todo para ver que sea posible
    for numero_paso, paso in enumerate(pasos):
        origen, destino = paso

        # realizamos la transferencia
        frasco_origen = frascos[origen - 1]
        frasco_destino = frascos[destino - 1]

        if len(frasco_origen) == 0:
            pytest.fail(
                f"El paso {numero_paso} no es posible, intenta mover líquido desde el frasco "
                f"{origen} que está vacío."
            )

        if len(frasco_origen) == CAPACIDAD_FRASCOS and len(set(frasco_origen)) == 1:
            pytest.fail(
                f"El paso {numero_paso} no es posible, intenta mover líquido desde el frasco "
                f"{origen} que ya está lleno de un solo color y tapado."
            )

        if len(frasco_destino) == CAPACIDAD_FRASCOS:
            pytest.fail(
                f"El paso {numero_paso} no es posible, intenta mover líquido hacia el frasco "
                f"{destino} que ya está lleno."
            )

        color = frasco_origen[-1]

        if frasco_destino and frasco_destino[-1] != color:
            pytest.fail(
                f"El paso {numero_paso} no es posible, intenta mover líquido de color {color} "
                f"desde el frasco {origen}, hacia el {destino} que tiene color {frasco_destino[-1]}"
            )

        while len(frasco_destino) < CAPACIDAD_FRASCOS and frasco_origen and frasco_origen[-1] == color:
            frasco_origen.pop()
            frasco_destino.append(color)

        print()
        print("PASO", numero_paso, ":", origen, "→", destino)
        print()
        dibujar(frascos)

    # validamos que todos los frascos están o vacíos o llenos de un solo color
    for frasco in frascos:
        frasco_vacio = len(frasco) == 0
        frasco_completado = len(frasco) == CAPACIDAD_FRASCOS and len(set(frasco)) == 1
        mensaje_si_frasco_mal = (
            "El resultado final de aplicar todos los pasos deja un frasco que no está ni "
            f"vacío ni completo con un solo color: {frasco}"
        )
        assert frasco_vacio or frasco_completado, mensaje_si_frasco_mal

    # validamos que la cantidad de pasos sea la esperada para el caso
    if pasos_esperados is not None:
        assert len(pasos) <= pasos_esperados, \
            f"La secuencia tiene {len(pasos)} pasos, pero este caso puede resolverse en menos pasos: {pasos_esperados}"
