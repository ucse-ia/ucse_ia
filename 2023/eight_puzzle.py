from simpleai.search import SearchProblem, iterative_limited_depth_first


#INITIAL = ((7, 2, 4), (5, None, 6), (8, 3, 1))
INITIAL = ((1, 4, 2), (3, 5, 8), (6, 7, None))
GOAL = ((None, 1, 2), (3, 4, 5), (6, 7, 8))


def find_token(state, token_to_find):
    for i_row, row in enumerate(state):
        for i_col, token in enumerate(row):
            if token == token_to_find:
                return i_row, i_col


class EightPuzzleProblem(SearchProblem):
    def actions(self, state):
        empty_row, empty_col = find_token(state, None)
        actions = []

        if empty_row > 0:
            actions.append((empty_row - 1, empty_col))
        if empty_row < 2:
            actions.append((empty_row + 1, empty_col))
        if empty_col > 0:
            actions.append((empty_row, empty_col - 1))
        if empty_col < 2:
            actions.append((empty_row, empty_col + 1))

        return actions

    def result(self, state, action):
        empty_row, empty_col = find_token(state, None)
        other_row, other_col = action

        state = [list(row) for row in state]

        state[empty_row][empty_col] = state[other_row][other_col]
        state[other_row][other_col] = None

        state = tuple(tuple(row) for row in state)

        return state

    def cost(self, state, action, state2):
        return 1

    def is_goal(self, state):
        return state == GOAL


my_problem = EightPuzzleProblem(INITIAL)
result = iterative_limited_depth_first(my_problem)

for action, state in result.path():
    print("A:", action)
    print("S:")
    print(*state, sep="\n")
