from simpleai.search import SearchProblem, breadth_first, depth_first, astar, greedy
from simpleai.search.viewers import ConsoleViewer, WebViewer, BaseViewer


def string2list(data):
    return [[int(n) for n in fila.split(",")]
            for fila in data.split("|")]


def list2string(data):
    return "|".join(",".join([str(n)
                              for n in fila])
                    for fila in data)


GOAL = "0,1,2|3,4,5|6,7,8"


def find_number(state, number):
    for fila in range(3):
        for columna in range(3):
            if state[fila][columna] == number:
                return fila, columna


GOAL_POSITIONS = dict((number, find_number(string2list(GOAL), number))
                      for number in range(1, 9))


class EightPuzzleProblem(SearchProblem):
    def is_goal(self, state):
        return state == GOAL

    def cost(self, state1, action, state2):
        return 1

    def actions(self, state):
        state = string2list(state)
        fila_0, columna_0 = find_number(state, 0)

        acciones = []

        fila_arriba = fila_0 - 1
        fila_abajo = fila_0 + 1
        columna_derecha = columna_0 + 1
        columna_izquierda = columna_0 - 1

        if fila_arriba >= 0:
            acciones.append(state[fila_arriba][columna_0])
        if fila_abajo <= 2:
            acciones.append(state[fila_abajo][columna_0])
        if columna_derecha <= 2:
            acciones.append(state[fila_0][columna_derecha])
        if columna_izquierda >= 0:
            acciones.append(state[fila_0][columna_izquierda])

        return acciones

    def result(self, state, action):
        state = string2list(state)
        f_0, c_0 = find_number(state, 0)
        f_a, c_a = find_number(state, action)

        state[f_0][c_0] = state[f_a][c_a]
        state[f_a][c_a] = 0

        return list2string(state)

    def heuristic(self, state):
        state = string2list(state)
        cost = 0
        for number, correct_position in GOAL_POSITIONS.items():
            current_position = find_number(state, number)
            diff_x = abs(current_position[0] - correct_position[0])
            diff_y = abs(current_position[1] - correct_position[1])
            cost += diff_x + diff_y

        return cost

    def heuristic_MALA(self, state):
        cost = 0
        for i in range(len(state)):
            if state[i] != '0' and state[i] != GOAL[i]:
                cost += 1

        return cost


visor = BaseViewer()  # o WebViewer() o ConsoleViewer()

result = astar(EightPuzzleProblem("7,2,4|5,0,6|8,3,1"),
               viewer=visor,
               graph_search=True)

print result.state
print result.path()
print len(result.path())

print visor.stats
