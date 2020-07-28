from simpleai.search import SearchProblem, breadth_first, depth_first, uniform_cost, greedy, astar
from simpleai.search.viewers import WebViewer, BaseViewer

# from breath_first_casero import breadth_first


# rapido
# INITIAL = '''1 4 2
# 3 7 5
# 6 0 8'''
# lento
INITIAL = '''7 2 4
5 0 6
8 3 1'''

GOAL = '''0 1 2
3 4 5
6 7 8'''


def str2list(state):
    return [[int(n) for n in row.split(' ')] for row in state.split('\n')]


def list2str(state):
    return '\n'.join([' '.join([str(n) for n in row]) for row in state])


def manhattan(pos_a, pos_b):
    row_a, col_a = pos_a
    row_b, col_b = pos_b

    diff_rows = abs(row_a - row_b)
    diff_cols = abs(col_a - col_b)

    return diff_rows + diff_cols


def find(number, state):
    for i_row, row in enumerate(state):
        for i_col, n in enumerate(row):
            if n == number:
                return (i_row, i_col)


class PuzzleProblem(SearchProblem):
    def is_goal(self, state):
        return state == GOAL

    def cost(self, state1, action, state2):
        return 1

    def actions(self, state):
        r = []
        st = str2list(state)
        r_0, c_0  = find(0, st)
        if r_0 > 0:
            r.append(st[r_0 - 1][c_0])
        if r_0 < 2:
            r.append(st[r_0 + 1][c_0])
        if c_0 > 0:
            r.append(st[r_0][c_0 - 1])
        if c_0 < 2:
            r.append(st[r_0][c_0 + 1])
        return r

    def result(self, state, action):
        st = str2list(state)
        r0, c0 = find(0, st)
        rn, cn = find(action, st)

        st[r0][c0] = action
        st[rn][cn] = 0
        return list2str(st)

    def heuristic(self, state):
        st = str2list(state)
        goal = str2list(GOAL)
        total_distance = 0
        for number in range(1, 9):
            current_position = find(number, st)
            target_position = find(number, goal)
            number_distance = manhattan(current_position, target_position)
            total_distance += number_distance

        return total_distance

if __name__ == '__main__':
    print(INITIAL)
    viewer = WebViewer()
    result = astar(PuzzleProblem(INITIAL), graph_search=True, viewer=viewer)
    for step in result.path():
        print(step)

    print('solution length:', len(result.path()))
    print(viewer.stats)


# viewer = WebViewer()
# result = breadth_first(PuzzleProblem(INITIAL), graph_search=True)
# print('Result state:')
# print(result.state)
# print('Result path:')
# for action, state in result.path():
    # print('Action:', action)
    # print(state)

# print('Solution at depth:', len(result.path()))
