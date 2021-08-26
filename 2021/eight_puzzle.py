from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    limited_depth_first,
    iterative_limited_depth_first,
)

# 1 4 2
#   3 5
# 6 7 8
INITIAL = (
    (1, 4, 2),
    (0, 3, 5),
    (6, 7, 8),
)

#   1 2
# 3 4 5
# 6 7 8
GOAL = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
)


def where_is(piece, state):
    """
    Find a piece in the board, and return the row and column indexes.
    """
    for row_index, row in enumerate(state):
        for col_index, current_piece in enumerate(row):
            if current_piece == piece:
                return row_index, col_index



class EightPuzzle(SearchProblem):
    def cost(self, state1, action, state2):
        return 1

    def is_goal(self, state):
        return state == GOAL

    def actions(self, state):
        empty_row, empty_col = where_is(0, state)

        available_actions = []

        # the piece above
        if empty_row > 0:
            available_actions.append(state[empty_row - 1][empty_col])
        # the piece below
        if empty_row < 2:
            available_actions.append(state[empty_row + 1][empty_col])
        # the piece to the left
        if empty_col > 0:
            available_actions.append(state[empty_row][empty_col - 1])
        # the piece to the right
        if empty_col < 2:
            available_actions.append(state[empty_row][empty_col + 1])

        return available_actions

    def result(self, state, action):
        empty_row, empty_col = where_is(0, state)
        piece_row, piece_col = where_is(action, state)

        state_as_lists = list(list(row) for row in state)

        state_as_lists[empty_row][empty_col] = action
        state_as_lists[piece_row][piece_col] = 0

        new_state = tuple(tuple(row) for row in state_as_lists)

        return new_state



problem = EightPuzzle(INITIAL)

result = limited_depth_first(problem, depth_limit=5)

print("Goal node:", result)

print("Path from initial to goal:")
for action, state in result.path():
    print("Action:", action)
    print("State:", state)
