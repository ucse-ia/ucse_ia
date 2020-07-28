# -*- coding: utf-8 -*-
from simpleai.machine_learning.reinforcement_learning import TDQLearner, RLProblem, \
                                                             make_exponential_temperature, \
                                                             PerformanceCounter
import random
from simpleai.environments import RLEnvironment
from itertools import combinations


class NineProblem(RLProblem):

    def actions(self, state):
        actions = []
        ranges = [(1, 3), (3, 6), (6, 10)]

        for x in ranges:
            r = range(*x)
            for i in range(1, len(r) + 1):
                for action in combinations(r, i):
                    if self.valid_action(action) and self.applicable_action(state, action):
                        actions.append(action)
        return actions

    def valid_action(self, action):
        if not (1 <= len(action) <= 4):
            return False

        #valid numbers
        if not all(x in range(1, 10) for x in action):
            return False

        #all in same row
        valid_ranges = [(1, 2), (3, 5), (6, 9)]
        a_min = min(action)
        a_max = max(action)

        for r_min, r_max in valid_ranges:
            if a_min <= r_max:
                break

        if not (a_min >= r_min and a_max <= r_max):
            return False

        #adjacent
        l_action = list(action)
        l_action.sort()
        return all(y - x == 1 for x, y in zip(l_action[:-1], l_action[1:]))

    def applicable_action(self, state, action):
        return all(x in state for x in action)


class Player(TDQLearner):

    def __init__(self, name):
        super(Player, self).__init__(NineProblem(),
                                     temperature_function=make_exponential_temperature(1000000, 0.01),
                                     discount_factor=0.9)
        self.name = name


class RandomPlayer(Player):

    def program(self, percept):
        return random.choice(self.problem.actions(percept))


class TrainingEnvironment(RLEnvironment):

    def __init__(self, agents):
        super(TrainingEnvironment, self).__init__(agents, tuple(range(1, 10)))
        self.last_agent = None

    def do_action(self, state, action, agent):
        self.last_agent = agent
        return tuple([x for x in state if x not in action])

    def is_completed(self, state):
        return len(state) == 0

    def play(self):
        self.last_agent = None
        random.shuffle(self.agents)
        self.run()

    def reward(self, state, agent):
        if self.is_completed(state):
            if self.last_agent is agent:
                return -1
            else:
                return 1
        return 0


def get_agent(name):
    res = Player(name)
    rand = RandomPlayer('random')
    env = TrainingEnvironment([res, rand])
    for i in range(3000):
        env.play()
    return res


if __name__ == '__main__':
    res = Player('name')
    rand = RandomPlayer('random')
    env = TrainingEnvironment([res, rand])
    per = PerformanceCounter(env.agents, ['q', 'random'])
    for i in range(3000):
        env.play()
    per.show_statistics()

