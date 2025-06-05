import warnings
from contextlib import contextmanager
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
def play_game():
    import entrega1
    play_game_function = getattr(entrega1, "play_game", None)

    return play_game_function


@pytest.mark.dependency(depends=["test_modulo_existe"])
def test_funcion_existe(play_game):
    assert play_game is not None, "La función play_game no existe"


@pytest.mark.dependency(depends=["test_funcion_existe"])
def test_funcion_bien_definida(play_game):
    params = list(signature(play_game).parameters)
    expected_params = ["jedi_at", "jedi_concentration", "walls", "droids"]

    # los primeros parámetros de la función tienen que ser los pedidos

    assert params[:len(expected_params)] == expected_params, \
           "La función play_game no recibe los parámetros definidos en la entrega"


@pytest.mark.dependency(depends=["test_funcion_bien_definida"])
@pytest.mark.parametrize("jedi_at,jedi_concentration,walls,droids,expected_cost,time_limit_s", (
    # expected_cost: costo de la solución esperada (óptima)
    # time_limit_s: tiempo máximo en segundos que play_game debería demorar en encontrar solución

    # casos super simples donde hay que ir directo a atacar

    # jedi con un solo droide en su casillero y concentración suficiente para slash:
    # slash
    ((0, 0), 1, [], [(0, 0, 1)], 1, 1),

    # jedi con un droide adyacente y concentración suficiente para slash:
    # move, slash
    ((0, 0), 1, [], [(0, -1, 1)], 2, 1),

    # jedi con muchos droides en su casillero y concentración suficiente para force:
    # force
    ((0, 0), 5, [], [(0, 0, 50)], 2, 1),

    # jedi con muchos droides adyacentes y concentración suficiente para force:
    # move, force
    ((0, 0), 5, [], [(0, 1, 50)], 3, 1),

    # jedi en diagonal a un droide y concentración suficiente para slash:
    # jump, slash
    ((0, 0), 2, [], [(1, 1, 1)], 2, 1),

    # jedi en diagonal a muchos droides y concentración suficiente para force:
    # jump, slash
    ((0, 0), 6, [], [(-1, 1, 50)], 3, 1),

    # jedi con varios droides en su casillero pero no pudiendo hacer force:
    # slash, slash, slash, slash
    ((0, 0), 4, [], [(0, 0, 4)], 4, 5),

    # jedi en diagonal a un droide pero sin concentración suficiente para salto:
    # move, move, slash
    ((0, 0), 1, [], [(1, 1, 1)], 3, 5),

    # casos con un poquito más de complejidad, donde requiere algo extra antes de ir a atacar
    # ciegamente

    # jedi con varios droides en diagonal, pero que necesita descansar antes de meterse a pelearlos
    # por falta de concentración:
    # rest, jump, force
    ((0, 0), 1, [], [(1, 1, 4)], 6, 10),

    # jedi con varios droides en su casillero que necesita alejarse y descansar para tener
    # concentración para pelearlos:
    # move, move, rest, jump, force
    ((0, 0), 0, [], [(0, 0, 6)], 8, 10),

    # jedi con un grupo de droides cercano, pero con una pared en el medio que debe ser esquivada
    # move x 6, force
    ((0, 0), 5, [(-1, 1), (0, 1), (1, 1)], [(0, 2, 5)], 8, 10),

    # casos medianos

    # 1 grupo de droides donde está el jedi, y 2 grupos más en las cercanias, con una pared
    # molesta que obliga a hacer un par de saltos:
    # force, rest, jump, jump, force, move, slash
    ((0, 0), 5, [(0, 1)], [(0, 0, 10), (0, 2, 10), (1, 2, 1)], 11, 30),

    # frente a una masa grande de droides pero super cargado de fuerza:
    # force, (move, force) x 3
    ((0, 0), 999, [], [(0, 0, 10), (0, 1, 10), (1, 0, 10), (1, 1, 10)], 11, 30),

    # lejos de una masa grande de droides pero super cargado de fuerza:
    # jump x 4, force, (move, force) x 3
    ((0, 0), 999, [], [(4, 4, 10), (4, 5, 10), (5, 4, 10), (5, 5, 10)], 15, 30),

    # droides repartidos en 3 diagonales, pero super cargado de fuerza
    ((0, 0), 999, [], [(-1, -1, 3), (-1, 1, 3), (1, -1, 3)], 11, 30),

    # un laberinto hasta un grupo de droides, super cargado de fuerza
    #    0 1 2 3 4 5
    # 0 []        []
    # 1 [][] J[][][]
    # 2 []    [] D[]
    # 3   [][][]  []
    # 4 []        []
    ((1, 2), 999,
     [(0, 0), (0, 5),
      (1, 0), (1, 1), (1, 3), (1, 4), (1, 5),
      (2, 0), (2, 3), (2, 5),
      (3, 1), (3, 2), (3, 3), (3, 5),
      (4, 0), (4, 5)],
     [(2, 4, 1)], 8, 30),

    # casos complicados

    # un laberinto, sin fuerza pero si descansa va saltando, y con muchos grupos de droides
    #    0 1 2 3 4 5
    # 0 []        []
    # 1 [][] J[][][]
    # 2 [] D  [] D[]
    # 3   [][][]  []
    # 4 []       D[]
    ((1, 2), 0,
     [(0, 0), (0, 5),
      (1, 0), (1, 1), (1, 3), (1, 4), (1, 5),
      (2, 0), (2, 3), (2, 5),
      (3, 1), (3, 2), (3, 3), (3, 5),
      (4, 0), (4, 5)],
     [(2, 1, 2), (2, 4, 1), (4, 4, 10)], 17, 300),
))
def test_resultado_es_correcto(
    play_game, jedi_at, jedi_concentration, walls, droids, expected_cost, time_limit_s,
):
    # helpers para mensajes de error y warnings
    case_description = f"[{jedi_at=}|{jedi_concentration=}|{walls=}|{droids=}]"
    duration_msg = (f"El caso {case_description} demoró demasiado tiempo (más de {time_limit_s} "
                    "segundos), probablemente algo no está bien")

    with duration_warning(time_limit_s, duration_msg):
        print()
        print("Resolviendo caso:")
        print(case_description)
        print("...")
        result = play_game(jedi_at, jedi_concentration, walls, droids)
        print("Solución obtenida!")

    # otros helpers
    duration = {
        "move": 1,
        "jump": 1,
        "slash": 1,
        "force": 2,
        "rest": 3,
    }
    concentration_cost = {
        "move": 0,
        "jump": 1,
        "slash": 1,
        "force": 5,
        "rest": -10,
    }
    error_prefix = f"Error en caso {case_description}:"

    # chequeamos la estructura de datos de forma muy básica
    assert isinstance(result, (list, tuple)), \
        f"{error_prefix} el resultado de play_game no fue una lista, sino {type(result)}"

    # simulamos el resultado del juego usando un mundo mutable
    droids = {
        (f_droid, c_droid): droid_q for (f_droid, c_droid, droid_q) in droids
    }
    walls = set(walls)
    total_cost = 0  # in seconds

    print("Simulando pasos obtenidos...")
    # por cada accion, hacemos chequeos y vamos simulando todo para ver que sea posible
    for idx_action, action in enumerate(result):
        print(jedi_at, jedi_concentration, droids, "-->", action)

        # helper para mensajes de error
        action_error_prefix = f"Error en {case_description} acción {idx_action}={action}:"

        assert isinstance(action, (list, tuple)), \
            f"{action_error_prefix} la acción no es una tupla, sino {type(action)}"
        assert len(action) == 2, \
            f"{action_error_prefix} la acción no es una tupla de 2 elementos, sino {action}"

        action_type, target = action
        assert action_type in duration, \
            f"{action_error_prefix} el tipo de acción {action_type} no existe"

        jedi_concentration -= concentration_cost[action_type]
        assert jedi_concentration >= 0, \
            f"{action_error_prefix} la acción consume más concentración de la disponible"

        total_cost += duration[action_type]
        assert total_cost <= expected_cost, \
            f"{action_error_prefix} la acción hace que el tiempo total sea {total_cost}, pero no puede ser mayor a {expected_cost}"

        if action_type in ("move", "jump"):
            assert isinstance(target, (list, tuple)), \
                f"{action_error_prefix} el destino no es una tupla de posición, sino {type(target)}"
            assert len(action) == 2, \
                f"{action_error_prefix} el destino no es una coordenada de 2 elementos, sino {target}"

            assert target not in walls, \
                f"{action_error_prefix} el destino {target} es una pared"

            jedi_r, jedi_c = jedi_at

            if action_type == "move":
                move_valid_targets = [
                    (jedi_r + 1, jedi_c),
                    (jedi_r - 1, jedi_c),
                    (jedi_r, jedi_c + 1),
                    (jedi_r, jedi_c - 1),
                ]
                assert target in move_valid_targets, \
                    f"{action_error_prefix} movimiento hacia una casilla que no es adyacente de {jedi_at}"
            elif action_type == "jump":
                jump_valid_targets = [
                    (jedi_r + 1, jedi_c + 1),
                    (jedi_r + 1, jedi_c - 1),
                    (jedi_r - 1, jedi_c + 1),
                    (jedi_r - 1, jedi_c - 1),
                ]
                assert target in jump_valid_targets, \
                    f"{action_error_prefix} salto hacia una casilla que no es diagonal de {jedi_at}"

            jedi_at = target
        elif action_type in ("slash", "force"):
            assert target is None, \
                f"{action_error_prefix} la acción no puede tener un destino diferente a None"

            assert jedi_at in droids, \
                f"{action_error_prefix} no hay droides para atacar en la posición {jedi_at}"

            if action_type == "slash" and droids[jedi_at] > 1:
                droids[jedi_at] -= 1
            else:
                del droids[jedi_at]
        elif action_type == "rest":
            assert target is None, \
                f"{action_error_prefix} la acción no puede tener un destino diferente a None"

            jedi_r, jedi_c = jedi_at
            disrupting_tiles = [
                jedi_at,
                (jedi_r + 1, jedi_c),
                (jedi_r - 1, jedi_c),
                (jedi_r, jedi_c + 1),
                (jedi_r, jedi_c - 1),
            ]
            for tile in disrupting_tiles:
                assert tile not in droids, \
                    f"{action_error_prefix} no se puede descansar en {jedi_at} porque hay droides en {tile}"

    print("Simulación de pasos finalizada!")

    # al final, el jedi debería haber eliminado todos los droides
    assert not droids, f"{error_prefix} al final del juego quedan droides vivos: {droids}"

    # por las dudas, si lo resolvió mejor de lo esperado, revisar!
    if total_cost < expected_cost:
        pytest.fail(
        # warnings.warn(
            f"La solución para {case_description} fue mejor de lo esperado: {total_cost}s, pero"
            f"se esperaba {expected_cost}s"
        )
