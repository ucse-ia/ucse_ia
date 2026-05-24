from simpleai.search import SearchProblem, astar, iterative_limited_depth_first, uniform_cost

# Estado --> ((objetos),(cajas))
# Con cajas --> ((objetos_por_empacar,),((objetos_en_caja_1,),(objetos_en_caja_2,)))

CAPACIDAD_MAXIMA = 10


def espacio_libre(caja):
    return CAPACIDAD_MAXIMA - sum(caja)


class Mudanza(SearchProblem):
    def is_goal(self, state):
        objetos_por_empacar = state[0]
        return len(objetos_por_empacar) == 0

    def actions(self, state):
        # accion = (objeto_a_empacar, caja_destino)
        acciones_disponibles = set()

        objetos_pendientes, cajas = state
        for objeto in objetos_pendientes:
            entra_en_alguna_caja = False

            for indice, caja in enumerate(cajas):
                if espacio_libre(caja) >= objeto:
                    acciones_disponibles.add((objeto, indice))
                    entra_en_alguna_caja = True

            # restringir el agregado de cajas nuevas a sólo cuando
            # NO entra en ninguna no deja soluciones de lado
            if not entra_en_alguna_caja:
                acciones_disponibles.add((objeto, len(cajas)))

        return tuple(acciones_disponibles)

    def result(self, state, action):
        objeto_a_empacar, indice_caja_destino = action

        # saco el objeto de los objetos pendientes
        objetos_pendientes = list(state[0])
        objetos_pendientes.remove(objeto_a_empacar)

        cajas = list(state[1])
        # si la caja_destino no existe
        if len(cajas) <= indice_caja_destino:
            # creo la caja con el objeto adentro
            cajas.append((objeto_a_empacar,))
        else:
            # meto el objeto en la caja correspondiente
            cajas[indice_caja_destino] += (objeto_a_empacar,)

        return (tuple(objetos_pendientes), tuple(cajas))

    def cost(self, state, action, state2):
        # el costo es 1 por empacar un objeto, o 2 si eso requiere agregar una caja nueva
        if len(state[1]) < len(state2[1]):
            return 2
        return 1

    def heuristic(self, state):
        # la heuristica estima:
        # + 1 por cada objeto que falta empacar
        # + 1 adicional por cada caja nueva que mínimamente vamos a necesitar
        objetos_por_empacar, cajas = state

        suma_de_pesos_de_objetos_restantes = sum(objetos_por_empacar)
        suma_de_espacio_libre = sum(espacio_libre(caja) for caja in cajas)

        diferencia_de_peso = max(0, suma_de_pesos_de_objetos_restantes - suma_de_espacio_libre)
        cajas_adicionales = diferencia_de_peso // CAPACIDAD_MAXIMA
        resto = diferencia_de_peso % CAPACIDAD_MAXIMA

        if resto > 0:
            cajas_adicionales += 1

        return len(objetos_por_empacar) + cajas_adicionales


def main():
    INITIAL_STATE = ((1, 2, 6, 4, 2, 5, 2, 4, 7, 3, 5, 1, 8, 9, 2), ())
    problema = Mudanza(INITIAL_STATE)
    resultado = astar(problema, graph_search=True)
    #resultado = uniform_cost(problema, True)

    print(resultado)


if __name__ == '__main__':
    main()
