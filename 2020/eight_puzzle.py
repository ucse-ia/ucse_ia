from simpleai.search import SearchProblem, breadth_first, depth_first, uniform_cost
from simpleai.search.viewers import WebViewer, BaseViewer


INITIAL_STATE = (
    (1, 4, 2),
    (0, 3, 5),
    (6, 7, 8),
)

GOAL_STATE = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
)


def find(n, state):
    """
    Find the row and column of the piece "n" inside the state.
    """
    for row_index, row in enumerate(state):
        for col_index, value in enumerate(row):
            if value == n:
                return row_index, col_index


class EightPuzzle(SearchProblem):
    def is_goal(self, state):
        """
        Is the state a goal state or not?
        """
        return state == GOAL_STATE

    def actions(self, state):
        """
        What actions can I do in a state?
        The actions are numbers, indicating the piece that must be moved to the place of the zero.
        Example, the action 3 means "move the number 3 to where the zero is".
        """
        row_zero, col_zero = find(0, state)
        available_actions = []

        if row_zero > 0:
            available_actions.append(state[row_zero - 1][col_zero])
        if row_zero < 2:
            available_actions.append(state[row_zero + 1][col_zero])
        if col_zero > 0:
            available_actions.append(state[row_zero][col_zero - 1])
        if col_zero < 2:
            available_actions.append(state[row_zero][col_zero + 1])

        return available_actions

    def result(self, state, action):
        """
        What is the result of applying a given action, to a given state?
        This must return the resulting state after the action was applied.
        """
        row_zero, col_zero = find(0, state)
        row_piece, col_piece = find(action, state)

        # convert tuples to lists
        state_modifiable = list(list(row) for row in state)

        state_modifiable[row_zero][col_zero] = action
        state_modifiable[row_piece][col_piece] = 0

        # convert lists to tuples
        state_modifiable = tuple(tuple(row) for row in state_modifiable)

        return state_modifiable

    def cost(self, state1, action, state2):
        """
        How much does an action cost?
        In this problem, every action (moving a number) costs the same: 1
        """
        return 1


problem = EightPuzzle(INITIAL_STATE)
result = depth_first(problem, graph_search=True, viewer=WebViewer())
