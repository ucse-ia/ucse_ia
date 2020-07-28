from simpleai.search import SearchProblem, breadth_first, depth_first, uniform_cost, greedy, astar
from simpleai.search.viewers import WebViewer, BaseViewer


INITIAL = (
    (7, 2, 4),
    (5, 0, 6),
    (8, 3, 1),
)

GOAL = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
)


def tuple2list(t):
    return [list(row) for row in t]


def list2tuple(t):
    return tuple(tuple(row) for row in t)


def find_number(number, state):
    for row_index, row in enumerate(state):
        for column_index, piece in enumerate(row):
            if piece == number:
                return row_index, column_index


class PuzzleProblem(SearchProblem):
    def is_goal(self, state):
        return state == GOAL

    def cost(self, state1, action, state2):
        return 1

    def actions(self, state):
        zero_row, zero_column = find_number(0, state)

        available_actions = []
        if zero_row > 0:
            available_actions.append(state[zero_row - 1][zero_column])
        if zero_row < 2:
            available_actions.append(state[zero_row + 1][zero_column])
        if zero_column > 0:
            available_actions.append(state[zero_row][zero_column - 1])
        if zero_column < 2:
            available_actions.append(state[zero_row][zero_column + 1])

        return available_actions

    def result(self, state, action):
        zero_row, zero_column = find_number(0, state)
        action_row, action_column = find_number(action, state)

        state = tuple2list(state)

        state[zero_row][zero_column] = action
        state[action_row][action_column] = 0

        return list2tuple(state)

    def heuristic(self, state):
        # h2, manhattan distance
        total = 0
        for number in range(1, 9):
            current_row, current_column = find_number(number, state)
            goal_row, goal_column = find_number(number, GOAL)
            distance = abs(current_row - goal_row) + abs(current_column - goal_column)
            total += distance

        return total


viewer = WebViewer()
# result = breadth_first(PuzzleProblem(INITIAL), graph_search=True)
# result = depth_first(PuzzleProblem(INITIAL), graph_search=True)
# result = uniform_cost(PuzzleProblem(INITIAL), graph_search=True, viewer=WebViewer())
# result = greedy(PuzzleProblem(INITIAL), graph_search=True, viewer=viewer)
result = astar(PuzzleProblem(INITIAL), graph_search=True, viewer=viewer)


print('Result state:')
print(result.state)
print('Result path:')
for action, state in result.path():
    print('Action:', action)
    print('State:', state)

print('Solution at depth:', len(result.path()))

print(viewer.stats)
