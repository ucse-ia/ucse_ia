import warnings
from contextlib import contextmanager
from collections import namedtuple
from datetime import datetime
from inspect import signature

import pytest


# test names, comments and printable error messages in spanish to help students


@contextmanager
def duration_warning(time_limit_s, message):
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
    # raiz del repo, o no se están corriendo los tests desde la raiz del repo.
    duration_msg = (
        "El import de la entrega demora demasiado tiempo, probablemente están "
        "ejecutando el CSP al importar el módulo. Toda la lógica de resolución "
        "debe estar dentro de la función build_camp, no a nivel de módulo."
    )
    with duration_warning(1, duration_msg):
        try:
            import entrega2
        except ModuleNotFoundError:
            pytest.fail("No se encuentra el módulo entrega2.py")


@pytest.fixture()
def build_camp():
    import entrega2

    fn = getattr(entrega2, "build_camp", None)
    return fn


@pytest.mark.dependency(depends=["test_modulo_existe"])
def test_funcion_existe(build_camp):
    assert build_camp is not None, "La función build_camp no existe en entrega2.py"


@pytest.mark.dependency(depends=["test_funcion_existe"])
def test_funcion_bien_definida(build_camp):
    params = list(signature(build_camp).parameters)
    expected_params = [
        "camp_size",
        "habs",
        "generators",
        "labs",
        "deposits",
        "airlocks",
        "craters",
    ]
    assert params[: len(expected_params)] == expected_params, (
        "La función build_camp no recibe los parámetros definidos en la entrega"
    )


Case = namedtuple(
    "Case",
    [
        "id",
        "description",
        "camp_size",
        "habs",
        "generators",
        "labs",
        "deposits",
        "airlocks",
        "craters",
        "is_possible",
        "time_limit_s",
    ],
)


def validate_result(
    result, camp_size, habs, generators, labs, deposits, airlocks, craters, case_name
):
    rows, cols = camp_size
    craters_set = set(craters)

    assert isinstance(result, (list, tuple)), (
        f"{case_name}: el resultado de build_camp no es una lista sino {type(result)}"
    )

    valid_types = {"hab", "gen", "lab", "dep", "air"}
    positions = {}

    for item in result:
        assert isinstance(item, (list, tuple)) and len(item) == 3, (
            f"{case_name}: cada elemento debe ser una tupla (tipo, fila, columna), se obtuvo {item}"
        )
        tipo, r, c = item

        assert tipo in valid_types, (
            f"{case_name}: tipo de módulo inválido '{tipo}', debe ser uno de {valid_types}"
        )
        assert 0 <= r < rows, (
            f"{case_name}: fila {r} fuera de la cuadrícula (rango válido: 0 a {rows - 1})"
        )
        assert 0 <= c < cols, (
            f"{case_name}: columna {c} fuera de la cuadrícula (rango válido: 0 a {cols - 1})"
        )

        pos = (r, c)

        # Restricción 1: sin superposición
        assert pos not in positions, (
            f"{case_name}: superposición en la celda {pos} ('{tipo}' y '{positions[pos]}')"
        )
        positions[pos] = tipo

        # Restricción 2: no en cráteres
        assert pos not in craters_set, (
            f"{case_name}: el módulo '{tipo}' está ubicado en el cráter {pos}"
        )

    # Verificar que se colocaron exactamente las cantidades pedidas
    counts = {t: 0 for t in valid_types}
    for tipo, r, c in result:
        counts[tipo] += 1

    assert counts["hab"] == habs, (
        f"{case_name}: se esperaban {habs} habitacional(es), se obtuvieron {counts['hab']}"
    )
    assert counts["gen"] == generators, (
        f"{case_name}: se esperaban {generators} generador(es), se obtuvieron {counts['gen']}"
    )
    assert counts["lab"] == labs, (
        f"{case_name}: se esperaban {labs} laboratorio(s), se obtuvieron {counts['lab']}"
    )
    assert counts["dep"] == deposits, (
        f"{case_name}: se esperaban {deposits} depósito(s), se obtuvieron {counts['dep']}"
    )
    assert counts["air"] == airlocks, (
        f"{case_name}: se esperaban {airlocks} esclusa(s), se obtuvieron {counts['air']}"
    )

    def is_border(r, c):
        return r == 0 or r == rows - 1 or c == 0 or c == cols - 1

    def adjacent(r1, c1, r2, c2):
        return abs(r1 - r2) + abs(c1 - c2) == 1

    def neighbors(r, c):
        return [
            (r + dr, c + dc)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if 0 <= r + dr < rows and 0 <= c + dc < cols
        ]

    habs_pos = [(r, c) for t, r, c in result if t == "hab"]
    gens_pos = [(r, c) for t, r, c in result if t == "gen"]
    labs_pos = [(r, c) for t, r, c in result if t == "lab"]
    deps_pos = [(r, c) for t, r, c in result if t == "dep"]

    # Restricción 3: esclusas en el borde
    for t, r, c in result:
        if t == "air":
            assert is_border(r, c), (
                f"{case_name}: esclusa en ({r},{c}) no está en el borde del mapa"
            )

    # Restricción 4: habitacionales al interior
    for r, c in habs_pos:
        assert not is_border(r, c), (
            f"{case_name}: módulo habitacional en ({r},{c}) está en el borde del mapa"
        )

    # Restricción 5: generador no adyacente a habitacional
    for gr, gc in gens_pos:
        for hr, hc in habs_pos:
            assert not adjacent(gr, gc, hr, hc), (
                f"{case_name}: generador en ({gr},{gc}) es adyacente al habitacional en ({hr},{hc})"
            )

    # Restricción 6: generadores no adyacentes entre sí
    for i, (gr1, gc1) in enumerate(gens_pos):
        for gr2, gc2 in gens_pos[i + 1 :]:
            assert not adjacent(gr1, gc1, gr2, gc2), (
                f"{case_name}: generadores en ({gr1},{gc1}) y ({gr2},{gc2}) son adyacentes entre sí"
            )

    # Restricción 7: laboratorio adyacente a al menos un depósito
    for lr, lc in labs_pos:
        assert any(adjacent(lr, lc, dr, dc) for dr, dc in deps_pos), (
            f"{case_name}: laboratorio en ({lr},{lc}) no tiene ningún depósito adyacente"
        )

    # Restricción 8: habitacional con al menos una celda adyacente libre (ruta de evacuación)
    occupied = set((r, c) for t, r, c in result) | craters_set
    for hr, hc in habs_pos:
        adj_cells = neighbors(hr, hc)
        assert any((ar, ac) not in occupied for ar, ac in adj_cells), (
            f"{case_name}: habitacional en ({hr},{hc}) no tiene ninguna celda adyacente libre para evacuación"
        )


@pytest.mark.dependency(depends=["test_funcion_bien_definida"])
@pytest.mark.parametrize(
    "case",
    (
        # Casos simples: restricciones básicas, respuesta rápida esperada

        Case(
            id="s1",
            description="sin módulos: debe retornar lista vacía",
            camp_size=(4, 4),
            habs=0, generators=0, labs=0, deposits=0, airlocks=0,
            craters=[],
            is_possible=True,
            time_limit_s=2,
        ),
        Case(
            id="s2",
            description="una sola esclusa debe quedar en el borde",
            camp_size=(4, 4),
            habs=0, generators=0, labs=0, deposits=0, airlocks=1,
            craters=[],
            is_possible=True,
            time_limit_s=5,
        ),
        Case(
            id="s3",
            description="habitacionales deben quedar al interior del mapa",
            camp_size=(5, 5),
            habs=2, generators=0, labs=0, deposits=0, airlocks=0,
            craters=[],
            is_possible=True,
            time_limit_s=10,
        ),
        Case(
            id="s4",
            description="generador no puede ser adyacente a habitacional",
            camp_size=(4, 5),
            habs=1, generators=1, labs=0, deposits=0, airlocks=0,
            craters=[],
            is_possible=True,
            time_limit_s=15,
        ),
        Case(
            id="s5",
            description="laboratorio debe quedar adyacente a al menos un depósito",
            camp_size=(4, 5),
            habs=0, generators=0, labs=1, deposits=1, airlocks=0,
            craters=[],
            is_possible=True,
            time_limit_s=15,
        ),
        Case(
            id="s6",
            description="caso completo con todos los tipos de módulos en grilla chica",
            camp_size=(5, 5),
            habs=1, generators=1, labs=1, deposits=1, airlocks=1,
            craters=[],
            is_possible=True,
            time_limit_s=60,
        ),

        # Casos medianos: combinaciones de restricciones más exigentes

        Case(
            id="m1",
            description="dos generadores no pueden ser adyacentes entre sí",
            camp_size=(5, 5),
            habs=0, generators=2, labs=0, deposits=0, airlocks=0,
            craters=[],
            is_possible=True,
            time_limit_s=30,
        ),
        Case(
            id="m2",
            description="dos laboratorios, cada uno debe tener su depósito adyacente",
            camp_size=(5, 6),
            habs=0, generators=0, labs=2, deposits=2, airlocks=0,
            craters=[],
            is_possible=True,
            time_limit_s=60,
        ),
        Case(
            id="m3",
            description="cráteres que restringen la ubicación de los módulos",
            camp_size=(5, 6),
            habs=2, generators=1, labs=1, deposits=2, airlocks=1,
            craters=[(2, 2), (2, 3)],
            is_possible=True,
            time_limit_s=120,
        ),
        Case(
            id="m4",
            description="múltiples módulos de cada tipo, todas las restricciones activas",
            camp_size=(6, 7),
            habs=3, generators=2, labs=2, deposits=3, airlocks=2,
            craters=[(1, 3), (4, 5)],
            is_possible=True,
            time_limit_s=300,
        ),

        # Casos imposibles: el CSP no debe encontrar solución

        Case(
            id="i1",
            description="grilla de 2 filas no tiene celdas interiores para habitacionales",
            camp_size=(2, 6),
            habs=1, generators=0, labs=0, deposits=0, airlocks=0,
            craters=[],
            is_possible=False,
            time_limit_s=10,
        ),
        Case(
            id="i2",
            description="todas las celdas del borde son cráteres, la esclusa no puede ubicarse",
            camp_size=(3, 3),
            habs=0, generators=0, labs=0, deposits=0, airlocks=1,
            craters=[(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
            is_possible=False,
            time_limit_s=10,
        ),
    ),
)
def test_resultado_es_correcto(build_camp, case):
    (
        id_,
        description,
        camp_size,
        habs,
        generators,
        labs,
        deposits,
        airlocks,
        craters,
        is_possible,
        time_limit_s,
    ) = case

    craters = tuple(craters)
    case_name = f"[{id_}: {description}]"
    duration_msg = (
        f"El caso {case_name} demoró demasiado tiempo (más de {time_limit_s} segundos), "
        "probablemente algo no está bien con la implementación del CSP"
    )

    with duration_warning(time_limit_s, duration_msg):
        print()
        print("Resolviendo caso", case_name)
        print(
            f"{camp_size=} {habs=} {generators=} {labs=} {deposits=} {airlocks=} {craters=}"
        )
        result = build_camp(camp_size, habs, generators, labs, deposits, airlocks, craters)
        print(f"Resultado obtenido: {result}")

    if not is_possible:
        assert result is None, (
            f"{case_name}: se esperaba None (caso sin solución posible) pero se obtuvo: {result}"
        )
        print(f"Caso {case_name} correctamente identificado como imposible.")
        return

    validate_result(
        result, camp_size, habs, generators, labs, deposits, airlocks, craters, case_name
    )
    print(f"Caso {case_name} resuelto correctamente con {len(result)} módulos ubicados.")
