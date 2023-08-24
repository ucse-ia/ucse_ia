from simpleai.search import (
    SearchProblem,
    breadth_first,
    uniform_cost,
    depth_first,
    limited_depth_first,
    iterative_limited_depth_first,
    greedy,
    astar,
)
from simpleai.search.viewers import BaseViewer, WebViewer


INITIAL = (
    (7, 2, 4),
    (5, "x", 6),
    (8, 3, 1),
)
# INITIAL = (
    # (1, 4, 2),
    # ("x", 5, 8),
    # (3, 6, 7),
# )
GOAL = (
    ("x", 1, 2),
    (3, 4, 5),
    (6, 7, 8),
)


def find_token(state, token_to_find):
    for i_row, row in enumerate(state):
        for i_col, token in enumerate(row):
            if token == token_to_find:
                return i_row, i_col


class EightPuzzleProblem(SearchProblem):
    def actions(self, state):
        empty_row, empty_col = find_token(state, "x")
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
        empty_row, empty_col = find_token(state, "x")
        other_row, other_col = action

        state = [list(row) for row in state]

        state[empty_row][empty_col] = state[other_row][other_col]
        state[other_row][other_col] = "x"

        state = tuple(tuple(row) for row in state)

        return state

    def cost(self, state, action, state2):
        return 1

    def is_goal(self, state):
        return state == GOAL

    def heuristic(self, state):
        total_distance = 0

        for current_row, row in enumerate(state):
            for current_col, token in enumerate(row):
                if token != "x":
                    goal_row, goal_col = find_token(GOAL, token)
                    total_distance += abs(goal_row - current_row) + abs(goal_col - current_col)

        return total_distance




my_problem = EightPuzzleProblem(INITIAL)

v = BaseViewer()
#v = WebViewer()

#result = breadth_first(my_problem)
#result = uniform_cost(my_problem)
#result = depth_first(my_problem, graph_search=True)
#result = limited_depth_first(my_problem, 20, viewer=v)
#result = limited_depth_first(my_problem, 6, viewer=v)
#result = iterative_limited_depth_first(my_problem, viewer=v)
result = astar(my_problem)

if result is None:
    print("No solution")
else:
    for action, state in result.path():
        print("A:", action)
        print("S:")
        print(*state, sep="\n")

    print("Final cost:", result.cost)

# print("Stats:")
# print(v.stats)
