from simpleai.search import SearchProblem, astar, greedy


INICIAL = ((0, 0), )
SIZE = 5


class HorseProblem(SearchProblem):
    def actions(self, state):
        current_pos = state[-1]
        possible_moves = (
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2),
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
        )

        valid_actions = []

        for move in possible_moves:
            new_pos = (
                current_pos[0] + move[0],
                current_pos[1] + move[1],
            )

            if 0 <= new_pos[0] <= (SIZE - 1) and 0 <= new_pos[1] <= (SIZE - 1):
                # estamos dentro del tablero!
                if new_pos not in state:
                    # y no lo visitamos!
                    valid_actions.append(new_pos)

        return valid_actions

    def result(self, state, action):
        return state + (action,)

    def is_goal(self, state):
        return len(state) == (SIZE * SIZE)

    def cost(self, state1, action, state2):
        return 1

    def heuristic(self, state):
        return (SIZE * SIZE) - len(state)


if __name__ == "__main__":
    p = HorseProblem(INICIAL)
    result = greedy(p, graph_search=True)

    for action, state in result.path():
        print("move to:", action)
        #print(state)

    print("Depth:", len(list(result.path())))


