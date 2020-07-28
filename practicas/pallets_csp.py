import datetime
import itertools
import random

from simpleai.search import CspProblem, min_conflicts
from simpleai.search.csp import _find_conflicts

# vamos a tomar como variables a las cajas y como dominios las columnas de los racks
# como el enunciado no definía cuales eran las cajas, vamos a recibir esa lista como parametro para
# poder hacer mas de una prueba


def generar_problema_csp_para_pallets(pallets):
    variables = pallets
    dominios = {}

    tamanio_depositos = [(5, 5), (5, 5), (7, 7)]

    for pallet in variables:
        tipo_pallet, _ = pallet
        dominios[pallet] = []
        for deposito, (n_filas, n_columnas) in zip(range(1, 4), tamanio_depositos):
            if tipo_pallet == 'Explosivo' and deposito not in (1, 2):
                # salteamos estos casos para ya validar la resriccion unaria
                # de que los explosicos solo deben ir en los depositos 1 o 2
                continue
            for fila in range(n_filas):
                for columna in range(n_columnas):
                    dominios[pallet].append((deposito, (fila, columna)))

    restricciones = []
    # no debe haber pallets toxicos adyacentes a pallets de comida
    # es lo mismo que decir que para cada par posible entre toxico y comida no sean adyacentes
    for pallet_toxico in pallets:
        for pallet_comestible in pallets:
            if pallet_toxico[0] == 'Tóxico' and pallet_comestible[0] == 'Comida':
                restricciones.append(((pallet_toxico, pallet_comestible), no_adyacentes))

    # los depositos no soportan mas de 1000 toneladas
    # no queda otra que hacer una restriccion global
    # vamos si a chequear cada deposito por separado
    for deposito in range(1, 4):
        restricciones.append((pallets, deposito_no_supera_x_toneladas(deposito, 1000)))

    # los depositos no soportan mas de 100 toneladas de exlosivos
    # no queda otra que hacer una restriccion global
    # vamos si a chequear cada deposito por separado
    pallets_explosivos = [pallet for pallet in pallets if pallet[0] == 'Explosivo']
    for deposito in range(1, 4):
        restricciones.append((pallets_explosivos, deposito_no_supera_x_toneladas(deposito, 100)))

    # No se pueden apilar pallets, ergo, todos los valores deben ser unicos
    for par_de_pallets in itertools.combinations(pallets, 2):
        restricciones.append((par_de_pallets, distinto_valor))

    return CspProblem(variables, dominios, restricciones)


def no_adyacentes(vars, vals):
    (dep_1, (fila_1, columna_1)), (dep_2, (fila_2, columna_2)) = vals

    # Si estan en distinto deposito son No Adyacentes
    if dep_1 != dep_2:
        return True

    delta_fila = abs(fila_1 - fila_2)
    delta_col = abs(columna_1 - columna_2)

    if delta_fila == 1 and delta_col in (0, 1) or delta_col == 1 and delta_fila in (0, 1):
        # estan adyacentes
        return False

    # los demas casos estan en el mismo deposito pero no adyacentes
    return True


def deposito_no_supera_x_toneladas(deposito, toneladas):
    def restriccion_real(vars, vals):
        total = 0
        for (_, peso), (deposito_asignado, _) in zip(vars, vals):
            if deposito_asignado == deposito:
                total += peso
        return total <= toneladas
    return restriccion_real


def distinto_valor(vars, vals):
    return len(vals) == len(set(vals))


def resolver(pallets):
    problema = generar_problema_csp_para_pallets(pallets)

    inicio = datetime.datetime.now()
    asignacion = min_conflicts(problema, iterations_limit=100)
    tiempo = (datetime.datetime.now() - inicio).total_seconds()

    conflictos = _find_conflicts(problema, asignacion)
    print("Numero de conflictos en la solucion: {}".format(len(conflictos)))
    print("Tiempo transcurrido: {} segundos".format(tiempo))


def probar_con_n_pallets(n_pallets):
    print('#' * 80)
    pallets = []
    for _ in range(n_pallets):
        tipo_pallet = random.choice(['Tóxico', 'Explosivo', 'Comida'])
        peso = random.randint(1, 50)
        pallets.append((tipo_pallet, peso))

    print('Ejemplo random con {} pallets'.format(len(pallets)))
    resolver(pallets)
    print('#' * 80)


def main():
    for n in [10, 20, 30]:
        probar_con_n_pallets(n)


if __name__ == '__main__':
    main()
