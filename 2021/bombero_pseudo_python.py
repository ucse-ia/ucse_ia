# el estado es una tupla de dos cosas: habitación actual del bombero, y diccionario de segundos de fuego restante en cada habitación
INNITIAL_STATE = ("E", {"E": 0, "L": 10, "D": 10, "B": 30, "C": 600})

ACCESIBLES = {
    "E": ["L"],
    "L": ["E", "C", "D",],
    "D": ["L"],
    "B": ["C"],
    "C": ["B", "L"],
}


class BomberoProblem:
    def actions(state):
        # las acciones son una tupla, que puede ser de dos formas distintas:
        # ("Ir", <habitación>)
        # ("Rociar", <cantidad segundos>)
        available_actions = []

        habitacion_bombero, fuegos_restantes = state

        # agregamos la accion de rociar si hay fuego en el lugar del bombero
        if fuegos_restantes[habitacion_bombero] > 0:
            available_actions.append(("Rociar", fuegos_restantes[habitacion_bombero]))

        # y agregamos una accion de moverse por cada habitación accesible desde donde está
        # el bombero
        for habitacion_accesible in ACCESIBLES[habitacion_bombero]:
            available_actions.append(("Ir", habitacion_accesible))

        return available_actions

    def result(state, action):
        # si la acción es rociar, descontamos segundos de fuego de la habitacion actual
        habitacion_bombero, fuegos_restantes = state
        tipo_accion, parametro_accion = action

        if tipo_accion == "Ir":
            habitacion_bombero = parametro_accion
        elif tipo_accion == "Rociar":
            fuegos_restantes[habitacion_bombero] = 0

        return (habitacion_bombero, fuegos_restantes)

    def is_goal(state):
        # llegamos a la solución si todos los fuegos se apagaron
        habitacion_bombero, fuegos_restantes = state

        for habitacion, fuego_restante in fuegos_restantes.items():
            if fuego_restante > 0:
                # hay una habitación con fuego, nos frenamos acá y ya sabemos que no es meta
                return False

        # porque no nos frenamos en ninguna habitación, ninguna tenía fuego
        return True

    def cost(state1, action, state2):
        # el costo de moverse es 5 segundos, y el de rociar es lo que diga la acción de rociar
        tipo_accion, parametro_accion = action
        if tipo_accion == "Ir":
            return 5
        elif tipo_accion == "Rociar":
            return parametro_accion

    def heuristic(state):
        # estimamos que como mínimo nos falta este tiempo:
        # - la duración de todos los fuegos activos sumados
        # - 5 segundos por cada habitación con fuego que no sea la actual
        estimacion = 0
        habitacion_bombero, fuegos_restantes = state

        for habitacion, fuego_restante in fuegos_restantes.items():
            estimacion += fuego_restante

            if habitacion != habitacion_bombero and fuego_restante > 0:
                estimacion += 5

        return estimacion
