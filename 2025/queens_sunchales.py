from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    limited_depth_first,
    uniform_cost,
    iterative_limited_depth_first,
)
from simpleai.search.viewers import BaseViewer, WebViewer

BOARD_SIZE = 8
INITIAL = (0,) * BOARD_SIZE


def queens_attacking(state):
    """
    Helper function to check if any of the queens are attacking each other
    """
    for queen_number, current_row in enumerate(state):
        for other_queen_number, other_current_row in enumerate(state):
            if queen_number != other_queen_number:
                if current_row == other_current_row:
                    # Attacking in the same row
                    return True
                else:
                    # Checking diagonals
                    row_difference = abs(current_row - other_current_row)
                    column_difference = abs(queen_number - other_queen_number)
                    if row_difference == column_difference:
                        return True
    return False


class QueensProblem(SearchProblem):
    def actions(self, state):
        available_actions = []
        for queen_number, current_row in enumerate(state):
            for destination_row in range(BOARD_SIZE):
                if destination_row != current_row:
                    available_actions.append((queen_number, destination_row))

        return available_actions

    def result(self, state, action):
        queen_number, destination_row = action

        # Make the state mutable to change it
        state = list(state)

        state[queen_number] = destination_row

        # Make the state immutable again
        return tuple(state)

    def cost(self, state, action, state2):
        return 1

    def is_goal(self, state):
        return not queens_attacking(state)


# Starts a web browser to see the progress of the search
web_viewer = WebViewer()
# Keeps records of the search to be viewed later
base_viewer = BaseViewer()

problem = QueensProblem(INITIAL)

# result = breadth_first(problem, viewer=base_viewer, graph_search=False)
# result = breadth_first(problem, viewer=base_viewer, graph_search=True)

# result = uniform_cost(problem, viewer=base_viewer, graph_search=False)
# result = uniform_cost(problem, viewer=base_viewer, graph_search=True)

# result = limited_depth_first(problem, 7, viewer=base_viewer, graph_search=False)
# result = limited_depth_first(problem, 7, viewer=base_viewer, graph_search=True)

# result = iterative_limited_depth_first(problem, viewer=base_viewer, graph_search=False)
result = iterative_limited_depth_first(problem, viewer=base_viewer, graph_search=True)

if result is not None:
    print("Goal state:\n", result.state)
    print("Path to solution:\n", result.path())
    print("Stats:\n", base_viewer.stats)
else:
    print("No solution found")
