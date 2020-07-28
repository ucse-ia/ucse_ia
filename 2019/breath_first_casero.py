
class SearchNode:
    def __init__(self, parent, state, action):
        self.parent = parent
        self.state = state
        self.action = action

    def path(self):
        actions = []
        node = self
        while node is not None:
            actions.append(node.action)
            node = node.parent

        actions = actions[:-1]
        return reversed(actions)


def breadth_first(problem):
    fringe = []
    seen = set()

    initial_node = SearchNode(
        parent=None,
        state=problem.initial_state,
        action=None,
    )
    fringe.append(initial_node)

    while fringe:
        current_node = fringe.pop(0)
        seen.add(current_node.state)

        if problem.is_goal(current_node.state):
            return current_node
        else:
            actions = problem.actions(current_node.state)
            for action in actions:
                child_state = problem.result(current_node.state, action)
                if child_state not in seen:
                    fringe.append(SearchNode(
                        parent=current_node,
                        state=child_state,
                        action=action,
                    ))





