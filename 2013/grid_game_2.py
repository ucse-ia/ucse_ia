# -*- coding: utf-8 -*-
from simpleai.machine_learning.reinforcement_learning import TDQLearner, SARSALearner, \
                                                             make_exponential_temperature, \
                                                             PerformanceCounter, \
                                                             RLProblem
from random import random, choice
from simpleai.environments import RLEnvironment, Viewer


class GridGame(RLEnvironment):

    def __init__(self, agent):
        super(RLEnvironment, self).__init__([agent], (1, 1))
        self.action_dict = {'up': (1, 0), 'down': (-1, 0), 'left': (0, -1), 'rigth': (0, 1)}
        self.rewards = {(3, 4): 1, (2, 4): -1}

    def do_action(self, state, action, agent):
        if random() > 0.95:
            action = choice(self.action_dict.keys())
        r1, c1 = state
        r2, c2 = self.action_dict[action]
        rn = r1 + r2
        cn = c1 + c2
        _next = (rn, cn)
        if _next != (2, 2) and (1 <= rn <= 3) and (1 <= cn <= 4):
            return _next
        return state

    def is_completed(self, state):
        return state in self.rewards.keys()

    def make_reward(self, state, agent):
        return self.rewards.get(state, -0.08)


class GridProblem(RLProblem):

    def actions(self, state):
        actions = ['up', 'down', 'left', 'rigth']
        return actions

if __name__ == '__main__':
    agent = TDQLearner(GridProblem(),
                       temperature_function=make_exponential_temperature(1000, 0.005),
                       discount_factor=0.9)
    game = GridGame(agent)

    p = PerformanceCounter([agent], ['Q-learner Agent'])

    for i in range(3000):
        game.run()

    p.show_statistics()

    game.run(viewer=Viewer())


