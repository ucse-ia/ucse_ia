from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    limited_depth_first,
    uniform_cost,
    iterative_limited_depth_first,
    greedy,
    astar,
)
from simpleai.search.viewers import BaseViewer, WebViewer


# complicado
INICIAL = (
    (7, 2, 4),
    (5, 0, 6),
    (8, 3, 1),
)

# facil
# INICIAL = (
    # (4, 1, 3),
    # (0, 2, 5),
    # (7, 8, 6),
# )


GOAL = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0),
)


def find_piece(state, piece):
    for idx_row, row in enumerate(state):
        for idx_col, current_piece in enumerate(row):
            if current_piece == piece:
                return idx_row, idx_col



class EightPuzzleProblem(SearchProblem):
    def cost(self, state, action, state2):
        return 1

    def is_goal(self, state):
        return state == GOAL

    def actions(self, state):
        zero_row, zero_col = find_piece(state, 0)
        available_actions = []

        moves = [
            (zero_row - 1, zero_col),  # up
            (zero_row + 1, zero_col),  # down
            (zero_row, zero_col - 1),  # left
            (zero_row, zero_col + 1),  # right
        ]

        for new_row, new_col in moves:
            if 0 <= new_row <= 2 and 0 <= new_col <= 2:
                piece = state[new_row][new_col]
                available_actions.append(piece)

        return available_actions

    def result(self, state, action):
        zero_row, zero_col = find_piece(state, 0)
        piece_row, piece_col = find_piece(state, action)

        state = list(list(row) for row in state)

        state[zero_row][zero_col] = action
        state[piece_row][piece_col] = 0

        state = tuple(tuple(row) for row in state)

        return state

    def heuristic(self, state):
        total_distance = 0
        for piece in range(1, 9):
            row, col = find_piece(state, piece)
            goal_row, goal_col = find_piece(GOAL, piece)

            distance = abs(row - goal_row) + abs(col - goal_col)
            total_distance += distance

        return total_distance



problem = EightPuzzleProblem(INICIAL)
#result = depth_first(problem, graph_search=True)
#result = breadth_first(problem)
result = astar(problem)

for action, state in result.path():
    print(action)
    for row in state:
        print(row)

print("Depth:", len(list(result.path())))
