from itertools import combinations
from contextlib import contextmanager
from datetime import datetime
from inspect import signature
import warnings

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
    # Probablemente el nombre del archivo no es correcto (debe ser entrega2.py), o no está en la
    # raiz del repo, o no se están corriento los tests desde la raiz del repo.
    duration_msg = ("El import de la entrega demora demasiado tiempo, probablemente están "
                    "haciendo búsqueda en el import. Hagan lo del if __name__ ... que se "
                    "recomienda en la consigna")
    with duration_warning(1, duration_msg):
        try:
            import entrega2
        except ModuleNotFoundError:
            pytest.fail("No se encuentra el módulo entrega2.py")


@pytest.fixture()
def build_map():
    import entrega2
    build_map_function = getattr(entrega2, "build_map", None)

    return build_map_function


@pytest.mark.dependency(depends=["test_modulo_existe"])
def test_funcion_existe(build_map):
    assert build_map is not None, "La función build_map no existe"


@pytest.mark.dependency(depends=["test_funcion_existe"])
def test_funcion_bien_definida(build_map):
    params = list(signature(build_map).parameters)
    expected_params = ["map_size", "walls", "droids"]

    # los primeros parámetros de la función tienen que ser los pedidos

    assert params[:len(expected_params)] == expected_params, \
           "La función build_map no recibe los parámetros definidos en la entrega"


@pytest.mark.dependency(depends=["test_funcion_bien_definida"])
@pytest.mark.parametrize("map_size,walls,droids,time_limit_s", (
    # time_limit_s: tiempo máximo en segundos que build_map debería demorar en encontrar solución

    # casos super triviales

    ((3, 3), 0, (), 1),  # solo el jedi el medio
    ((3, 3), 1, (), 1),  # jedi y 1 pared
    ((3, 3), 0, (5,), 1),  # jedi y 1 grupo de droides
    ((3, 3), 1, (5,), 1),  # jedi y 1 grupo de droides y 1 pared

    # casos más normales pero igual fáciles de resolver

    ((3, 3), 4, (1, 1, 1), 3),
    ((4, 6), 8, (5, 5, 3, 3, 1, 1), 10),

    # casos complicados por tener pocas soluciones posibles

    ((3, 3), 7, (), 5),  # pocas formas de no encerrar al jedi
    ((4, 4), 14, (), 5),  # pocas formas de no encerrar al jedi
    ((3, 3), 0, (4, 4, 4, 4, 4, 2, 2, 2, 2), 5),  # pocas formas de que los droides no sumen mas de 6
    ((4, 4), 13, (4, 2, 4), 5),  # pocas formas de no encerrar al jedi y además drones complicados por la suma si están adyacentes
))
def test_resultado_es_correcto(build_map, map_size, walls, droids, time_limit_s):
    # helpers para mensajes de error y warnings
    case_description = f"[{map_size=}|{walls=}|{droids=}]"
    duration_msg = (f"El caso {case_description} demoró demasiado tiempo (más de {time_limit_s} "
                    "segundos), probablemente algo no está bien")

    with duration_warning(time_limit_s, duration_msg):
        print()
        print("Resolviendo caso:")
        print(case_description)
        print("...")
        result = build_map(map_size, walls, droids)
        print("Solución obtenida!")

    error_prefix = f"Error en caso {case_description}:"

    # chequeamos la estructura de datos de forma muy básica
    assert isinstance(result, (list, tuple)), \
        f"{error_prefix} el resultado de build_map no fue una lista, sino {type(result)}"

    # contruimos el tablero con el resultado obtenido, validando entonces que el formato sea
    # correcto y ya algunas de las restricciones que se pueden ir chequeando a medida que armamos
    # el tablero
    droid_positions = {}
    wall_positions = set()
    jedi_pos = None
    rows, cols = map_size

    print("Analizando el resultado obtenido...")
    for idx_item, item in enumerate(result):
        print("Item", idx_item, "=", item)

        # helper para mensajes de error
        item_error_prefix = f"Error en {case_description} item {idx_item}={item}:"

        assert isinstance(item, (list, tuple)), \
            f"{item_error_prefix} el item no es una tupla, sino {type(item)}"
        assert len(item) == 3, \
            f"{item_error_prefix} el item no es una tupla de 2 elementos, sino {item}"

        item_type, row, col = item
        assert item_type in ("jedi", "wall") or isinstance(item_type, int), \
            f"{item_error_prefix} el tipo de item {item_type} no existe"

        assert isinstance(row, int) and isinstance(col, int), \
            f"{item_error_prefix} las coordenadas {row}, {col} no son números enteros"
        item_pos = (row, col)

        if item_type == "jedi":
            assert not jedi_pos, \
                f"{item_error_prefix} ya hay un jedi en el tablero, no se puede agregar otro"

            jedi_pos = item_pos
        elif item_type == "wall":
            assert item_pos not in wall_positions, \
                f"{item_error_prefix} ya hay una pared en la misma posición"

            wall_positions.add(item_pos)
        else:
            # item_type es un número, así que es un grupo de droides
            assert item_pos not in droid_positions, \
                f"{item_error_prefix} ya droides en la posición {item_pos}"

            droid_positions[item_pos] = item_type

    # no puede haber droides y paredes en la misma posición
    for droid_pos in droid_positions.keys():
        assert droid_pos not in wall_positions, \
            f"{error_prefix} hay droides y una pared en la misma posición {droid_pos}"

    # el jedi no puede estar en una pared
    assert jedi_pos not in wall_positions, \
        f"{error_prefix} el jedi no puede estar en una pared"

    # dibujamos el mapa para ayudar
    print("Mapa resultante:")
    for row in range(rows):
        row_items = []
        for col in range(cols):
            pos = (row, col)
            if pos in wall_positions:
                row_items.append("[]")
            else:
                prefix = "J" if pos == jedi_pos else " "
                sufix = str(droid_positions.get(pos, " "))
                row_items.append(f"{prefix}{sufix}")
        print("|".join(row_items))
        if row < rows - 1:
            print(("--+" * cols)[:-1])

    # se tiene que haber ubicado todo lo pedido y en las cantidades correctas
    assert jedi_pos, f"{error_prefix} no se ha colocado el jedi en el tablero"
    assert len(wall_positions) == walls, \
        f"{error_prefix} el caso pedía {walls} paredes pero se han colocado {len(wall_positions)}"
    assert set(droid_positions.values()) == set(droids), \
        f"{error_prefix} el caso pedía grupos de droides {droids} pero se han colocado {tuple(droid_positions.values())}"

    # el jedi no puede estar en el borde
    assert jedi_pos[0] not in (0, rows - 1) and jedi_pos[1] not in (0, cols - 1), \
        f"{error_prefix} el jedi no puede estar en el borde del mapa"
    # el jedi no puede estar rodeado de paredes
    adjacent_cells = [
        (jedi_pos[0] + dr, jedi_pos[1] + dc)
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1))
    ]
    adjacent_walls = [cell in wall_positions for cell in adjacent_cells]
    assert not all(adjacent_walls), \
        f"{error_prefix} el jedi no puede estar rodeado de 4 paredes adyacentes, tiene que tener al menos una salida"

    # los doirdes adyacentes no pueden sumar más de 6
    for (droid_pos1, droid_count1), (droid_pos2, droid_count2) in combinations(droid_positions.items(), 2):
        if (abs(droid_pos1[0] - droid_pos2[0]) + abs(droid_pos1[1] - droid_pos2[1]) == 1):
            # adyacentes, chequear la suma
            assert droid_count1 + droid_count2 <= 6, \
                f"{error_prefix} los droides adyacentes en {droid_pos1} y {droid_pos2} suman más de 6 ({droid_count1} + {droid_count2})"
