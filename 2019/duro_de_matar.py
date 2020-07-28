from simpleai.search import SearchProblem, depth_first, uniform_cost, greedy, astar
from simpleai.search.viewers import WebViewer, BaseViewer

from breath_first_casero import breadth_first


# c3, c5
INITIAL = (0, 0)

MAX_CAPACITY = (3, 5)


class BombProblem(SearchProblem):
    def is_goal(self, state):
        c3, c5 = state
        return c5 == 4

    def cost(self, state1, action, state2):
        return 1

    def actions(self, state):
        c3, c5 = state
        available_actions = []
        if c3 > 0:
            available_actions.append(('empty', 0))
        if c5 > 0:
            available_actions.append(('empty', 1))
        if c3 < 3:
            available_actions.append(('fill', 0))
        if c5 < 5:
            available_actions.append(('fill', 1))
        if c3 > 0 and c5 < 5:
            available_actions.append(('pass', 0))
        if c5 > 0 and c3 < 3:
            available_actions.append(('pass', 1))

        return available_actions

    def result(self, state, action):
        c3, c5 = state
        new_state = [c3, c5]
        action_type, origin = action
        if action_type == 'empty':
            new_state[origin] = 0
        elif action_type == 'fill':
            new_state[origin] = MAX_CAPACITY[origin]
        elif action_type == 'pass':
            destination = 0 if origin == 1 else 1

            can_pass = new_state[origin]
            can_receive = MAX_CAPACITY[destination] - new_state[destination]

            to_pass = min([can_pass, can_receive])

            new_state[origin] -= to_pass
            new_state[destination] += to_pass

        return tuple(new_state)


if __name__ == '__main__':
    result = breadth_first(BombProblem(INITIAL))
    for step in result.path():
        print(step)
