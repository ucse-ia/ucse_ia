# -*- coding: utf-8 -*-
from simpleai.machine_learning.reinforcement_learning import TDQLearner, RLProblem, \
                                                             make_exponential_temperature, \
                                                             PerformanceCounter
from random import shuffle
import importlib
import sys
import traceback
import random
import numpy
import matplotlib
import dateutil
from simpleai.environments import RLEnvironment
from itertools import combinations


class ProblemaPapelitos(RLProblem):

    def actions(self, state):
        'acciones posibles de cada estado'
        actions = []
        acciones = []
        filas = [[x for x in state if 1 <= x <= 2],[x for x in state if 3 <= x <= 5],[x for x in state if 6 <= x <= 9]]
        for fila in filas:
            for cantidad in range(1,5):
                for combinacion in combinations(fila, cantidad):
                        acciones.append(list(combinacion))
        for accion in acciones:
            if len(accion) != 1:
                if sum(accion) in [3,7,9,12,13,15,17,21,24,30]:
                    if sum(accion) == 15:
                        if accion[0] != 6:
                            actions.append(tuple(accion))
                    else:
                        actions.append(tuple(accion))
            else:
                actions.append(tuple(accion))
        return actions


class PapelitosPlayer(TDQLearner):

    def __init__(self, name):
        super(PapelitosPlayer, self).__init__(ProblemaPapelitos(),
                                              temperature_function=make_exponential_temperature(1000000, 0.01),
                                              discount_factor=0.4)
        self.name = name

class RandomPlayer(PapelitosPlayer):

    def program(self, perception):
        try:
            return random.choice(self.problem.actions(self.problem.update_state(perception, self)))
        except:
            return None


class JuegoPapelitos(RLEnvironment):

    def __init__(self, agents):
        shuffle(agents)
        super(JuegoPapelitos, self).__init__(agents, tuple(range(1, 10)))
        self.last_agent = None

    def play(self):
        self.last_agent = None
        try:
            self.run()
            return self.winner()
        except:
            traceback.print_exc()
            return self.winner()

    def winner(self):
        a0, a1 = self.agents
        return a0 if a1 is self.last_agent else a1

    def do_action(self, state, action, agent):
        action = list(action)
        self.last_agent = agent
        #test valid action
        if not self.valid_action(action):
            raise Exception('Invalid action')
        #test applicable action
        if not self.applicable_action(self.state, action):
            raise Exception('Inapplicable action')
        #apply action
        return tuple([x for x in state if x not in action])

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
        action.sort()
        return all(y - x == 1 for x, y in zip(action[:-1], action[1:]))

    def applicable_action(self, state, action):
        return all(x in state for x in action)

    def is_completed(self, state):
        return len(state) == 0

    def reward(self, state, agent):
        if self.last_agent == agent:
            if len(state) == 0 or len(state) == 2:
                return -1
            elif len(state) == 1:
                return 1
            else:
                return 0
        else:
            if len(state) == 0 or len(state) == 2:
                return 1
            elif len(state) == 1:
                return -1
            else:
                return 0

def get_agent(name):
    agente_aux = PapelitosPlayer('aux')
    agente_random = RandomPlayer('random')
    game = JuegoPapelitos([agente_aux, agente_random])
    game.agents = [agente_aux, agente_random]
    for i in range(3000):
        game.run()
    agente = PapelitosPlayer(name)
    game = JuegoPapelitos([agente, agente_random])
    game.agents = [agente, agente_random]
    for i in range(3000):
        game.run()
    game = JuegoPapelitos([agente, agente_aux])
    game.agents = [agente, agente_aux]
    for i in range(7000):
        game.run()
    game = JuegoPapelitos([agente_aux, agente])
    game.agents = [agente_aux, agente]
    for i in range(7000):
        game.run()
    return agente
