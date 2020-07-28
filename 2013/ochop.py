# para usarse requiere tener instalados:
# usando pip:
#   simpleai
#   pyparsing==1.5.7
#   pydot
#   flask
# usando apt-get en linux, o el instalador en windows:
#   graphviz
#   (el instalador de windows esta en http://www.graphviz.org/Download_windows.php)

from simpleai.search import SearchProblem, greedy, astar
from simpleai.search.viewers import WebViewer


GOAL = 'e12\n345\n678'
INITIAL = '724\n5e6\n831'


def str2list(state):
    return [list(row) for row in state.split()]


def list2str(state):
    return '\n'.join(''.join(row) for row in state)


def find(state, element):
    for row_index, row in enumerate(state):
        for col_index, current_element in enumerate(row):
            if element == current_element:
                return row_index, col_index


class OchoProblem(SearchProblem):
    def is_goal(self, state):
        return state == GOAL

    def cost(self, state1, action, state2):
        return 1

    def actions(self, state):
        movements = [
            (0, 1),
            (0, -1),
            (-1, 0),
            (1, 0)
        ]

        state = str2list(state)
        actions = []

        row_e, col_e = find(state, 'e')

        for movement_r, movement_c in movements:
            new_row_e = row_e + movement_r
            new_col_e = col_e + movement_c

            if 0 <= new_row_e <= 2 and 0 <= new_col_e <= 2:
                actions.append(state[new_row_e][new_col_e])

        return actions

    def result(self, state, action):
        state = str2list(state)

        row_e, col_e = find(state, 'e')
        row_n, col_n = find(state, action)

        state[row_e][col_e] = state[row_n][col_n]
        state[row_n][col_n] = 'e'

        return list2str(state)

    def heuristic(self, state):
        state = str2list(state)
        goal = str2list(GOAL)

        distance = 0

        for number in '12345678':
            row_n, col_n = find(state, number)
            row_g, col_g = find(goal, number)

            distance += abs(row_n - row_g) + abs(col_n - col_g)

        return distance


result = astar(OchoProblem(INITIAL), viewer=WebViewer())
#result = astar(OchoProblem(INITIAL))

print result.path()
print len(result.path())
