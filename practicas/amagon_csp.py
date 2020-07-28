import datetime
import random

from simpleai.search import CspProblem, min_conflicts
from simpleai.search.csp import _find_conflicts

# vamos a tomar como variables a las cajas y como dominios las columnas de los racks
# como el enunciado no definía cuales eran las cajas, vamos a recibir esa lista como parametro para
# poder hacer mas de una prueba


def generar_problema_csp_para_amagon(cajas):
    variables = cajas
    dominios = {}

    for caja in variables:
        tipo_caja, peso = caja
        dominios[caja] = []
        for rack in range(6):
            for columna in range(3):
                if tipo_caja == 'Explosivo' and rack not in (1, 2):
                    # salteamos estos casos para ya validar la resriccion unaria
                    # de que los explosicos solo deben ir en los racks 1 o 2
                    continue
                dominios[caja].append((rack, columna))

    restricciones = []
    # no debe haber cajas con contenido toxico y comestible en el mismo racks
    # es lo mismo que decir que para cada par posible entre toxico y comida no compartan rack
    for caja_toxica in cajas:
        for caja_comestible in cajas:
            if caja_toxica[0] == 'Tóxico' and caja_comestible[0] == 'Comida':
                restricciones.append(((caja_toxica, caja_comestible), distinto_rack))

    # los racks no soportan mas de 1000 kilos
    # no queda otra que hacer una restriccion global
    # vamos si a chequear cada rack por separado
    for rack in range(6):
        restricciones.append((cajas, rack_no_supera_1000_kilos(rack)))

    # cada columna puede apilar hasta 10 cajas
    # es casi igual a la anterior
    for rack in range(6):
        for columna in range(3):
            restricciones.append((cajas, columna_no_apila_mas_de_10(rack, columna)))

    return CspProblem(variables, dominios, restricciones)


def distinto_rack(vars, vals):
    racks_in_vals = set([rack for rack, col in vals])
    return len(vals) == len(racks_in_vals)


def rack_no_supera_1000_kilos(rack):
    def restriccion_real(vars, vals):
        total = 0
        for (_, peso), (rack_asignado, _) in zip(vars, vals):
            if rack_asignado == rack:
                total += peso
        return total <= 1000
    return restriccion_real


def columna_no_apila_mas_de_10(rack, columna):
    def restriccion_real(vars, vals):
        total = 0
        for (rack_asignado, columna_asignada) in vals:
            if rack_asignado == rack and columna_asignada == columna:
                total += 1
        return total <= 10
    return restriccion_real


def resolver(cajas):
    problema = generar_problema_csp_para_amagon(cajas)

    inicio = datetime.datetime.now()
    asignacion = min_conflicts(problema, iterations_limit=100)
    tiempo = (datetime.datetime.now() - inicio).total_seconds()

    conflictos = _find_conflicts(problema, asignacion)
    print("Numero de conflictos en la solucion: {}".format(len(conflictos)))
    print("Tiempo transcurrido: {} segundos".format(tiempo))


def probar_con_n_cajas(n_cajas):
    print('#' * 80)
    cajas = []
    for _ in range(n_cajas):
        tipo_caja = random.choice(['Tóxico', 'Explosivo', 'Comida'])
        peso = random.randint(1, 100)
        cajas.append((tipo_caja, peso))

    print('Ejemplo random con {} cajas'.format(len(cajas)))
    resolver(cajas)
    print('#' * 80)


def main():
    for n in [10, 60, 100, 200]:
        probar_con_n_cajas(n)


if __name__ == '__main__':
    main()
