import warnings
from contextlib import contextmanager
from collections import namedtuple
from datetime import datetime
from inspect import signature

import pytest


# test names, comments and printable error messages in spanish to help students


@contextmanager
def duration_warning(time_limit_s, message):
    """
    Context manager to check the duration of a piece of executed code, and trigger a warning if
    it's too much.
    """
    start = datetime.now()

    yield

    end = datetime.now()

    seconds = int((end - start).total_seconds())
    if time_limit_s is not None and seconds > time_limit_s:
        warnings.warn(message + f" [duración: {seconds} segundos]")


@pytest.mark.dependency()
def test_modulo_existe():
    # Si falla este test es porque no se pudo encontrar el código python de la entrega.
    # Probablemente el nombre del archivo no es correcto (debe ser entrega1.py), o no está en la
    # raiz del repo, o no se están corriento los tests desde la raiz del repo.
    duration_msg = ("El import de la entrega demora demasiado tiempo, probablemente están "
                    "haciendo búsqueda en el import. Hagan lo del if __name__ ... que se "
                    "recomienda en la consigna")
    with duration_warning(1, duration_msg):
        try:
            import entrega1
        except ModuleNotFoundError:
            pytest.fail("No se encuentra el módulo entrega1.py")


@pytest.fixture()
def planear_rover():
    import entrega1
    planeaar_rover_function = getattr(entrega1, "planear_rover", None)

    return planeaar_rover_function


@pytest.mark.dependency(depends=["test_modulo_existe"])
def test_funcion_existe(planear_rover):
    assert planear_rover is not None, "La función planear_rover no existe"


@pytest.mark.dependency(depends=["test_funcion_existe"])
def test_funcion_bien_definida(planear_rover):
    params = list(signature(planear_rover).parameters)
    expected_params = [
        "rover_inicio",
        "bateria_inicial",
        "capsulas_equipo",
        "zonas_sombra",
        "muestras_igneas",
        "muestras_sedimentarias",
        "punto_extraccion",
    ]

    # los primeros parámetros de la función tienen que ser los pedidos
    assert params[:len(expected_params)] == expected_params, \
           "La función planear_rover no recibe los parámetros definidos en la entrega"


Case = namedtuple("Case", [
    "description",
    "rover",
    "battery",
    "capsules",
    "shadows",
    "igneous",
    "sediments",
    "exfil",
    "expected_cost",  # costo de la solución esperada (óptima)
    "time_limit_s",  # tiempo máximo en segundos que planear_rover debería demorar en encontrar solución
])

@pytest.mark.dependency(depends=["test_funcion_bien_definida"])
@pytest.mark.parametrize("case", (
    # casos super simples donde hay que hacer casi nada

    Case(description="sin muestras a recolectar, ya es meta",
         rover=(0, 0), battery=20, capsules=[], shadows=[], igneous=[], sediments=[], exfil=(0, 0),
         expected_cost=0, time_limit_s=1),

    Case(description="una sola muestra a recolectar, con capsula super cerca y bateria de sobra",
         rover=(0, 0), battery=20, capsules=[(0, 1)], shadows=[], igneous=[(0, 2)], sediments=[], exfil=(0, 3),
         expected_cost=9, time_limit_s=1),

    Case(description="una sola muestra a recolectar del otro tipo",
         rover=(0, 0), battery=20, capsules=[(0, 1)], shadows=[], igneous=[], sediments=[(0, 2)], exfil=(0, 3),
         expected_cost=9, time_limit_s=1),

    Case(description="una sola muestra a recolectar, pero se entrega en la misma casilla que de salida",
         rover=(0, 0), battery=20, capsules=[(0, 1)], shadows=[], igneous=[(0, 2)], sediments=[], exfil=(0, 0),
         expected_cost=9, time_limit_s=1),

    Case(description="una sola muestra a recolectar, pero hace falta cargar bateria antes",
         rover=(0, 0), battery=1, capsules=[(0, 1)], shadows=[], igneous=[(0, 2)], sediments=[], exfil=(0, 3),
         expected_cost=13, time_limit_s=1),

    Case(description="una sola muestra a recolectar, pero lo ideal es con overdive",
         rover=(0, 0), battery=20, capsules=[(0, 2)], shadows=[], igneous=[(0, 4)], sediments=[], exfil=(0, 6),
         expected_cost=9, time_limit_s=1),

    Case(description="una sola muestra a recolectar, pero hace falta cargar bateria y no en el lugar donde estamos",
         rover=(0, 0), battery=2, capsules=[(0, 1)], shadows=[(0, 0)], igneous=[(0, 2)], sediments=[], exfil=(0, 3),
         expected_cost=13, time_limit_s=1),

    # casos probablemente imposibles con SimpleAI por performance vs tamaño del árbol

    # Case(description="caso del dibujo en la consigna",
    #      rover=(0, 0), battery=20, capsules=[(-3, 1), (-2, -1), (-1, -3), (3 , -1)], shadows=[(-2, 2), (-1, 3)],
    #      igneous=[(0, -5), (2, 1)], sediments=[(0, 5), (2, 2)], exfil=(2, -4),
    #      expected_cost=10000, time_limit_s=60),
))
def test_resultado_es_correcto(planear_rover, case):
    description, rover, battery, capsules, shadows, igneous, sediments, exfil, expected_cost, time_limit_s = case

    # helpers para mensajes de error y warnings
    case_description = f"[{rover=}|{battery=}|{capsules=}|{shadows=}|{igneous=}|{sediments=}|{exfil=}]"
    duration_msg = (f"El caso {case_description} demoró demasiado tiempo (más de {time_limit_s} "
                    "segundos), probablemente algo no está bien")

    with duration_warning(time_limit_s, duration_msg):
        print()
        print("Resolviendo caso:", description)
        print(case_description)
        print("...")
        result = planear_rover(rover, battery, tuple(capsules), tuple(shadows), tuple(igneous), tuple(sediments), exfil)
        print("Solución obtenida!")

    # otros helpers
    times = {
        "moverse": 1,
        "sobremarcha": 1,
        "equipar": 3,
        "recolectar": 2,
        "entregar": 1,
        "recargar": 4,
    }
    batt_consumptions = {
        "moverse": 1,
        "sobremarcha": 4,
        "equipar": 1,
        "recolectar": 3,
        "entregar": 1,
        "recargar": -10,  # consumo negativo = recarga
    }
    error_prefix = f"Error en caso {case_description}:"

    # chequeamos la estructura de datos de forma muy básica
    assert isinstance(result, (list, tuple)), \
        f"{error_prefix} el resultado de planear_rover no fue una lista, sino {type(result)}"

    # simulamos el resultado del juego usando un mundo mutable
    load = 0
    drill = "ninguno"
    max_batt = 20
    max_load = 2
    total_cost = 0  # in minutes

    print("Simulando pasos obtenidos...")
    # por cada accion, hacemos chequeos y vamos simulando todo para ver que sea posible
    for idx_action, action in enumerate(result):
        print(rover, load, drill, igneous, sediments, "-->", action)

        # helper para mensajes de error
        action_error_prefix = f"Error en {case_description} acción {idx_action}={action}:"

        assert isinstance(action, (list, tuple)), \
            f"{action_error_prefix} la acción no es una tupla, sino {type(action)}"
        assert len(action) == 2, \
            f"{action_error_prefix} la acción no es una tupla de 2 elementos, sino {action}"

        action_type, target = action
        assert action_type in times, \
            f"{action_error_prefix} el tipo de acción {action_type} no existe"

        battery = min(max_batt, battery - batt_consumptions[action_type])
        assert battery >= 0, \
            f"{action_error_prefix} la acción consume más batería de la disponible"
        assert battery > 0, \
            f"{action_error_prefix} el rover se quedó sin batería después de esta acción, nunca debe quedar sin batería"

        total_cost += times[action_type]
        assert total_cost <= expected_cost, \
            f"{action_error_prefix} la acción hace que el tiempo total sea {total_cost}, pero no puede ser mayor a {expected_cost}"

        if action_type in ("moverse", "sobremarcha"):
            assert isinstance(target, (list, tuple)), \
                f"{action_error_prefix} el destino no es una tupla de posición, sino {type(target)}"
            assert len(action) == 2, \
                f"{action_error_prefix} el destino no es una coordenada de 2 elementos, sino {target}"

            rover_r, rover_c = rover

            if action_type == "moverse":
                move_valid_targets = [
                    (rover_r + 1, rover_c),
                    (rover_r - 1, rover_c),
                    (rover_r, rover_c + 1),
                    (rover_r, rover_c - 1),
                ]
                assert target in move_valid_targets, \
                    f"{action_error_prefix} movimiento hacia una casilla que no es adyacente de {rover}"
            elif action_type == "sobremarcha":
                overdrive_valid_targets = [
                    (rover_r + 2, rover_c),
                    (rover_r - 2, rover_c),
                    (rover_r, rover_c + 2),
                    (rover_r, rover_c - 2),
                ]
                assert target in overdrive_valid_targets, \
                    f"{action_error_prefix} sobremarcha hacia una casilla que no es destino válido desde {rover}"

            rover = target
        elif action_type == "equipar":
            assert target in ("termico", "percusion"), \
                "{action_error_prefix} el tipo de taladro a equipar no es válido: {target}"

            assert rover in capsules, \
                "{action_error_prefix} no hay cápsula para equipar taladro en la posición del rover {rover}"

            drill = target
        elif action_type == "recolectar":
            assert target in ("ignea", "sedimentaria"), \
                f"{action_error_prefix} el tipo de muestra a recolectar no es válido: {target}"

            assert load < max_load, \
                f"{action_error_prefix} el rover ya tiene la carga máxima de 2 muestras, no puede recolectar más sin entregar"

            if target == "ignea":
                assert drill == "termico", \
                    f"{action_error_prefix} para recolectar muestra ígnea se necesita el taladro térmico equipado"
                assert rover in igneous, \
                    f"{action_error_prefix} no hay muestra ígnea para recolectar en la posición del rover {rover}"

                igneous = tuple(m for m in igneous if m != rover)
            elif target == "sedimentaria":
                assert drill == "percusion", \
                    f"{action_error_prefix} para recolectar muestra sedimentaria se necesita el taladro de percusión equipado"
                assert rover in sediments, \
                    f"{action_error_prefix} no hay muestra sedimentaria para recolectar en la posición del rover {rover}"

                sediments = tuple(m for m in sediments if m != rover)

            load += 1
        elif action_type == "entregar":
            assert rover == exfil, \
                f"{action_error_prefix} para entregar las muestras el rover debe estar en el punto de extracción {exfil}, pero está en {rover}"

            assert load > 0, \
                f"{action_error_prefix} no hay muestras para entregar"

            load = 0
        elif action_type == "recargar":
            assert rover not in shadows, \
                f"{action_error_prefix} no se puede recargar en una zona de sombra: {rover}"
            # no hay otro cambio más que actualizar battery, que ya se hizo arriba

    print("Simulación de pasos finalizada!")

    # al final, el rover debería haber recolectado todas las muestras y dejado todas en el punto de extracción
    assert not load, f"{error_prefix} al final del proceso quedan cargas en el rover: {load}"
    assert not igneous, f"{error_prefix} al final del proceso quedan muestras ígneas por recolectar: {igneous}"
    assert not sediments, f"{error_prefix} al final del proceso quedan muestras sedimentarias por recolectar: {sediments}"

    # por las dudas, si lo resolvió mejor de lo esperado, revisar!
    if total_cost < expected_cost:
        warnings.warn(
            f"La solución para {case_description} fue mejor de lo esperado: {total_cost} mins, pero"
            f"se esperaba {expected_cost} mins"
        )
