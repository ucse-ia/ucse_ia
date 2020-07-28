from simpleai.search import (SearchProblem, breadth_first, depth_first,
                             iterative_limited_depth_first, greedy,
                             astar)
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer


GOAL = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
)

INITIAL = (
    (7, 2, 4),
    (5, 0, 6),
    (8, 3, 1),
)


def find_number(board, number):
    for row_index, row in enumerate(board):
        for col_index, current_number in enumerate(row):
            if current_number == number:
                return row_index, col_index


class PuzzleProblem(SearchProblem):
    def cost(self, state1, action, state2):
        return 1

    def is_goal(self, state):
        return state == GOAL

    def actions(self, state):
        row_0, col_0 = find_number(state, 0)
        actions = []

        if row_0 > 0:
            actions.append(state[row_0 - 1][col_0])
        if row_0 < 2:
            actions.append(state[row_0 + 1][col_0])
        if col_0 > 0:
            actions.append(state[row_0][col_0 - 1])
        if col_0 < 2:
            actions.append(state[row_0][col_0 + 1])

        return actions

    def result(self, state, action):
        state_modificable = [list(row) for row in state]

        row_a, col_a = find_number(state, action)
        row_0, col_0 = find_number(state, 0)

        state_modificable[row_0][col_0] = action
        state_modificable[row_a][col_a] = 0

        return tuple(tuple(row) for row in state_modificable)

    def heuristic(self, state):
        total_difference = 0
        for row_index, row in enumerate(state):
            for col_index, current_number in enumerate(row):
                row_goal, col_goal = find_number(GOAL, current_number)
                difference = abs(row_index - row_goal) + abs(col_index - col_goal)
                total_difference += difference
        return total_difference


viewer = BaseViewer()
result = astar(PuzzleProblem(INITIAL), graph_search=True, viewer=viewer)

for action, state in result.path():
    print action
    print "\n".join(' '.join(map(str, row)) for row in state)

print viewer.stats
print 'costo solucion', result.cost
