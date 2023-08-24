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


# pos_araña, tiene_carga, humanos_libres
INITIAL = (2, 1), False, ((0, 0), (0, 2))

WALLS = (1, 0), (1, 1)
JAIL = (1, 2)


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class SpiderProblem(SearchProblem):
    def actions(self, state):
        pos_spider, loaded, free_food = state

        available_actions = []

        spider_row, spider_col = pos_spider
        if spider_row > 0:
            available_actions.append((spider_row - 1, spider_col))
        if spider_row < 2:
            available_actions.append((spider_row + 1, spider_col))
        if spider_col > 0:
            available_actions.append((spider_row, spider_col - 1))
        if spider_col < 2:
            available_actions.append((spider_row, spider_col + 1))

        available_actions = [
            pos for pos in available_actions
            if pos not in WALLS
        ]

        if not loaded and pos_spider in free_food:
            available_actions.append("pick")

        if loaded and pos_spider == JAIL:
            available_actions.append("drop")

        return available_actions

    def result(self, state, action):
        pos_spider, loaded, free_food = state

        if action == "pick":
            loaded = True
            free_food = list(free_food)
            free_food.remove(pos_spider)
            free_food = tuple(free_food)
        elif action == "drop":
            loaded = False
        else:
            pos_spider = action

        return pos_spider, loaded, free_food

    def cost(self, state, action, state2):
        if action == "pick":
            return 15
        elif action == "drop":
            return 5
        else:
            return 10

    def is_goal(self, state):
        pos_spider, loaded, free_food = state
        return not loaded and free_food == ()

    def heuristic(self, state):
        pos_spider, loaded, free_food = state
        # picks y drops de gente en el piso
        total_cost = 20 * len(free_food)
        # distancia a gente más lejos
        if free_food:
            total_cost += max(distance(pos_spider, pos_food)
                              for pos_food in free_food) * 10
        # distancias de gentes a jaula
        total_cost += sum(distance(JAIL, pos_food)
                          for pos_food in free_food) * 10
        # descargar persona en espalda
        if loaded:
            total_cost += 5

        return total_cost


v = BaseViewer()
my_problem = SpiderProblem(INITIAL)

result = astar(my_problem, viewer=v)

if result is None:
    print("No solution")
else:
    for action, state in result.path():
        print("A:", action)
        print("S:")
        print(*state, sep="\n")

    print("Final depth:", len(result.path()))
    print("Final cost:", result.cost)

print("Stats:")
print(v.stats)
