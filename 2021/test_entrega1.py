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
    with warning_si_demora(1, mensaje_si_demora):
        import entrega1


@pytest.fixture()
def planear_escaneo():
    import entrega1
    funcion_planear = getattr(entrega1, "planear_escaneo", None)

    return funcion_planear


@pytest.mark.dependency(depends=["test_modulo_existe"])
def test_funcion_existe(planear_escaneo):
    assert planear_escaneo is not None, "La función planear_escaneo no existe"


@pytest.mark.dependency(depends=["test_funcion_existe"])
def test_funcion_bien_definida(planear_escaneo):
    parametros = list(signature(planear_escaneo).parameters)

    # los primeros parámetros de la función tienen que ser los pedidos
    assert parametros[:3] == ['tuneles', 'robots'], \
           "La función planear_escaneo no recibe los parámetros definidos en la entrega"




ENTRADA = 5, 0
# ejemplos de robots
E1 = ("e1", "escaneador")
E2 = ("e2", "escaneador")
E3 = ("e3", "escaneador")
S1 = ("s1", "soporte")
S2 = ("s2", "soporte")

# ejemplos de minas super simples

# e[]
MINA_UN_CASILLERO = ((5, 1), )

# e[][][][]
MINA_TUNEL_RECTO = ((5, 1), (5, 2), (5, 3), (5, 4))

# e[][][][]
#  [][][][]
MINA_TUNEL_ANCHO = (
    (5, 1), (5, 2), (5, 3), (5, 4),
    (6, 1), (6, 2), (6, 3), (6, 4),
)

#      []
#      []
# e[][][]
MINA_L = (
    (5, 1), (5, 2), (5, 3),
    (4, 3), (3, 3),
)

#      []
#      []
# e[][][]
#      []
#      []
MINA_T = (
    (5, 1), (5, 2), (5, 3),
    (4, 3), (3, 3), (6, 3), (7, 3),
)

# estas minas requieren recarga o múltiples robots sin recarga

#      []
#      []
# e[][][][][]
#      []
#      []
MINA_CRUZ = (
    (5, 1), (5, 2), (5, 3), (5, 4), (5, 5),
    (4, 3), (3, 3), (6, 3), (7, 3),
)

#    [][][]
#    []
# e[][][][]
#    []
#    [][][]
MINA_E = (
    (5, 1), (5, 2), (5, 3), (5, 4),
    (4, 2), (3, 2), (3, 3), (3, 4),
    (6, 2), (7, 2), (7, 3), (7, 4),
)

#    [][][][]
#    []    []
# e[][][][][]
#    []    []
#    [][][][]
MINA_OCHO = (
    (5, 1), (5, 2), (5, 3), (5, 4), (5, 5),
    (4, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5),
    (6, 2), (7, 2), (7, 3), (7, 4), (7, 5), (6, 5),
)

# estas minas ya son más complicadas

#    [][][][]
#    []    [][]
# e[][][][][]    []
#    []    []    []
#    [][][][][][][]
MINA_GRANDE = (
    (5, 1), (5, 2), (5, 3), (5, 4), (5, 5),
    (4, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5), (4, 6),
    (6, 2), (7, 2), (7, 3), (7, 4), (7, 5),
    (7, 6), (7, 7), (7, 8), (6, 8), (5, 8),
)

@pytest.mark.dependency(depends=["test_funcion_bien_definida"])
@pytest.mark.parametrize("tuneles,robots,pasos_esperados,limite_segs", (
    # casos super básicos

    # micro tunel de un solo casillero, un solo robot escaneador
    pytest.param(MINA_UN_CASILLERO, (E1, ), 1, 3, id="1_casillero_1_explorador"),
    # micro tunel de un solo casillero, un robot de cada tipo
    pytest.param(MINA_UN_CASILLERO, (E1, S1), 1, 3, id="1_casillero_1_explorador_1_soporte"),
    # micro tunel de un solo casillero, dos robots escaneadores
    pytest.param(MINA_UN_CASILLERO, (E1, E2), 1, 3, id="1_casillero_2_exploradores"),

    # casos chicos
    pytest.param(MINA_TUNEL_RECTO, (E1, ), 4, 3, id="tunel_recto_1_explorador"),
    pytest.param(MINA_TUNEL_RECTO, (E1, S1), 4, 3, id="tunel_recto_1_explorador_1_soporte"),
    pytest.param(MINA_TUNEL_RECTO, (E1, E2), 4, 3, id="tunel_recto_2_exploradores"),
    pytest.param(MINA_TUNEL_ANCHO, (E1, ), 8, 3, id="tunel_ancho_1_explorador"),
    pytest.param(MINA_TUNEL_ANCHO, (E1, S1), 8, 3, id="tunel_ancho_1_explorador_1_soporte"),
    pytest.param(MINA_TUNEL_ANCHO, (E1, E2), 8, 3, id="tunel_ancho_2_exploradores"),
    pytest.param(MINA_L, (E1, ), 5, 3, id="mina_L_1_explorador"),
    pytest.param(MINA_L, (E1, S1), 5, 3, id="mina_L_1_explorador_1_soporte"),
    pytest.param(MINA_L, (E1, E2), 5, 3, id="mina_L_2_exploradores"),
    pytest.param(MINA_T, (E1, ), 9, 3, id="mina_T_1_explorador"),
    pytest.param(MINA_T, (E1, S1), 9, 3, id="mina_T_1_explorador_1_soporte"),
    pytest.param(MINA_T, (E1, E2), 9, 3, id="mina_T_2_exploradores"),

    # ejemplos chicos pero ya requiriendo recarga con robot de soporte, o
    # dos robots sin recarga
    pytest.param(MINA_CRUZ, (E1, S1), 18, 5, id="mina_cruz_1_explorador_1_soporte"),
    pytest.param(MINA_CRUZ, (E1, E2), 14, 5, id="mina_cruz_2_exploradores"),
    pytest.param(MINA_E, (E1, S1), 23, 5, id="mina_E_1_explorador_1_soporte"),
    pytest.param(MINA_E, (E1, E2), 16, 5, id="mina_E_2_exploradores"),
    pytest.param(MINA_OCHO, (E1, S1), 23, 5, id="mina_8_1_explorador_1_soporte"),
    pytest.param(MINA_OCHO, (E1, E2), 20, 5, id="mina_8_2_exploradores"),

    # casos grandes
    pytest.param(MINA_GRANDE, (E1, S1), 57, 30, id="mina_grande_1_explorador_1_soporte"),
    pytest.param(MINA_GRANDE, (E1, E2, S1), 43, 30, id="mina_grande_2_exploradores_1_soporte"),
))
def test_plan_es_correcto(planear_escaneo, tuneles, robots, pasos_esperados, limite_segs):
    mensaje_si_demora = (f"La prueba con tuneles {tuneles} y robots {robots} demoró demasiado "
                         f"tiempo (más de {limite_segs} segundos), probablemente algo no está "
                         "demasiado bien")

    with warning_si_demora(limite_segs, mensaje_si_demora):
        plan = planear_escaneo(tuneles, robots)

    # chequeamos la estructura de datos de forma muy básica
    assert isinstance(plan, list), \
           f"El resultado de planear_escaneo no fue una lista, sino {type(plan)}"
    for paso in plan:
        assert isinstance(paso, tuple), f"Un paso del plan no es una tupla, sino {type(paso)}"
        assert len(paso) == 3, f"Un paso del plan no contiene 3 datos: {paso}"

    # para simular el plan, vamos a necesitar ir trackeando la posición y carga de cada robot
    estado_actual = {
        id_robot: {
            "tipo": tipo_robot,
            "coords": ENTRADA,
            "carga": 1000,
        }
        for id_robot, tipo_robot in robots
    }
    # y además, la lista de casilleros pendientes de escaneo
    tuneles_pendientes = set(tuneles)

    # por cada paso, hacemos chequeos y vamos simulando todo para ver que sea posible
    for numero_paso, paso in enumerate(plan):
        id_robot, tipo_accion, target_accion = paso

        # el robot debe existir
        assert id_robot in estado_actual, f"El paso {numero_paso} tiene un id de robot inexistente: {id_robot}"

        # el tipo de acción tiene que ser válido
        assert tipo_accion in ("mover", "cargar"), f"El paso {numero_paso} tiene un tipo de acción inexistente: {tipo_accion}"

        # el parámetro de la acción tiene que ser correcto
        if tipo_accion == "mover":
            assert target_accion in tuneles, f"El paso {numero_paso} (moverse) contiene un destino que no es un túnel válido: {target_accion}"
        else:
            assert target_accion in estado_actual, f"El paso {numero_paso} (cargar) contiene un robot destinatario inexistente: {target_accion}"
            assert estado_actual[target_accion]["tipo"] == "escaneador", \
                f"El paso {numero_paso} (cargar) intenta cargar a un robot que no es escaneador: {target_accion}"
            assert estado_actual[id_robot]["coords"] == estado_actual[target_accion]["coords"], \
                f"El paso {numero_paso} (cargar) intenta cargar a un robot que no está en la misma posición que el robot de soporte: {id_robot} a {target_accion}"

        # actualizamos el estado de la simulación
        if tipo_accion == "mover":
            estado_actual[id_robot]["coords"] = target_accion
            if estado_actual[id_robot]["tipo"] == "escaneador":
                estado_actual[id_robot]["carga"] -= 100
                assert estado_actual[id_robot]["carga"] >= 0, f"El paso {numero_paso} dejaría a un robot con carga de batería negativa: {id_robot}"
                try:
                    tuneles_pendientes.remove(target_accion)
                except KeyError:
                    pass
        elif tipo_accion == "cargar":
            estado_actual[target_accion]["carga"] = 2500

    # validamos que no quedaron tuneles pendientes
    assert len(tuneles_pendientes) == 0, f"El plan construído no termina de escanear todos los túneles, deja pendientes: {tuneles_pendientes}"

    # validamos que la cantidad de viajes sea la esperada para el caso
    if pasos_esperados is not None:
        assert len(plan) <= pasos_esperados, \
            f"El plan construído tiene {len(plan)} pasos, pero este caso puede resolverse en menos pasos: {pasos_esperados}"
