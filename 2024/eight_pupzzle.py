from simpleai.search import (
    SearchProblem,
    breadth_first, depth_first, uniform_cost, limited_depth_first,
    iterative_limited_depth_first,
)
from simpleai.search.viewers import WebViewer


# INITIAL_STATE = (
    # (1, 4, 2),
    # (0, 3, 5),
    # (6, 7, 8),
# )


INITIAL_STATE = (
    (3, 2, 8),
    (5, 0, 6),
    (7, 1, 4),
)


GOAL_STATE = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
)


def position(state, n):
    for row_index, row in enumerate(state):
        for col_index, value in enumerate(row):
            if value == n:
                return row_index, col_index


class EightPuzzleProblem(SearchProblem):
    def is_goal(self, state):
        return state == GOAL_STATE

    def actions(self, state):
        zero_row, zero_col = position(state, 0)
        available_actions = []

        if zero_col > 0:
            available_actions.append(state[zero_row][zero_col - 1])
        if zero_col < 2:
            available_actions.append(state[zero_row][zero_col + 1])
        if zero_row > 0:
            available_actions.append(state[zero_row - 1][zero_col])
        if zero_row < 2:
            available_actions.append(state[zero_row + 1][zero_col])

        return available_actions

    def result(self, state, action):
        zero_row, zero_col = position(state, 0)
        piece_row, piece_col = position(state, action)

        state = [list(row) for row in state]

        state[zero_row][zero_col] = action
        state[piece_row][piece_col] = 0

        state = tuple(tuple(row) for row in state)

        return state

    def cost(self, state, action, state2):
        return 1


#result = breadth_first(EightPuzzleProblem(INITIAL_STATE))
#result = depth_first(EightPuzzleProblem(INITIAL_STATE), viewer=WebViewer(), graph_search=True)
result = depth_first(EightPuzzleProblem(INITIAL_STATE), graph_search=True)
#result = uniform_cost(EightPuzzleProblem(INITIAL_STATE))
#result = limited_depth_first(EightPuzzleProblem(INITIAL_STATE), 50)
#result = iterative_limited_depth_first(EightPuzzleProblem(INITIAL_STATE))


print("Solution node state:")
print(result.state)
print("Depth:", result.depth)
print()

for action, state in result.path():
    print("Move:", action)
    print(state)





