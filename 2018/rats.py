from simpleai.search.models import SearchProblem
from simpleai.search import astar, breadth_first, depth_first, greedy, uniform_cost
from simpleai.search.viewers import WebViewer, BaseViewer

EXIT = (2, 3)
WALLS = ((0, 1), (1, 1), (3, 2))

INITIAL = (EXIT, ((0, 2), (3, 1)))


def valid_position(row, col):
    if row > 3 or row < 0:
        return False
    if col > 3 or col < 0:
        return False
    if (row, col) in WALLS:
        return False

    return True


def manhattan(pos_a, pos_b):
    return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])


class RatsProblem(SearchProblem):
    def cost(self, state1, action, state2):
        return 1

    def is_goal(self, state):
        return state == (EXIT, tuple())

    def actions(self, state):
        rat_pos, foods = state
        rat_row, rat_col = rat_pos

        available_actions = []
        for delta_row, delta_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_rat_row = rat_row + delta_row
            new_rat_col = rat_col + delta_col

            if valid_position(new_rat_row, new_rat_col):
                available_actions.append((new_rat_row, new_rat_col))

        return available_actions

    def result(self, state, action):
        rat_pos, foods = state
        return (action, tuple([food_pos for food_pos in foods
                               if food_pos != action]))

    def heuristic(self, state):
        rat_pos, foods = state
        distances = [manhattan(rat_pos, EXIT)]
        for food_pos in foods:
            distances.append(manhattan(rat_pos, food_pos) +
                             manhattan(food_pos, EXIT))

        return max(distances)


print('Searching for a solution...')
# result = astar(RatsProblem(INITIAL), graph_search=True,
               # viewer=WebViewer())
viewer = BaseViewer()
# result = astar(RatsProblem(INITIAL), graph_search=True, viewer=viewer)
result = depth_first(RatsProblem(INITIAL), graph_search=True, viewer=viewer)

print('Solution found!')
print('State:', result.state)
print('Solution cost:', result.cost)
print('Stats:', viewer.stats)
print('Path from initial:')

for action, resulting_state in result.path():
    print('action:', action)
    print('state:', resulting_state)
    print('-' * 40)
