#!/usr/bin/env python
# -*- coding: utf-8 -*-

from simpleai.machine_learning.reinforcement_learning import TDQLearner, RLProblem, \
                                                             make_exponential_temperature, \
                                                             PerformanceCounter
from simpleai.environments import RLEnvironment
from itertools import combinations
from random import choice, shuffle


def get_agent(name):
    theProblem = Fisa9Problem()

    thePlayer = GenericPlayer(name, theProblem)
    randomPlayer = RandomPlayer("FisaBot", theProblem)  # Formerly called "MullerBot" but because now it actually trains our
                                                        #   bot, we changed its name

    theGame = Fisa9Game([randomPlayer, thePlayer], tuple(range(1, 10)))

    for i in range(8000):
        shuffle(theGame.agents)
        theGame.run()

    return thePlayer

REMOVE_MARK = 'X'

class Fisa9Problem(RLProblem):

    def actions(self, state):

        # Tuple to "Legacy" adapter
        strState = ''
        for number in range(1, 10):
            if number not in state:
                strState += REMOVE_MARK
            else:
                strState += str(number)

        # === "Legacy" spaghetti actions ======
        actions = []
        allClusters = []

        lanes = (strState[:2], strState[2:5], strState[5:],)

        for lane in lanes:
            allClusters += [cluster for cluster in lane.split(REMOVE_MARK) if cluster is not '']

        if len(allClusters) == 1:
            # This prevents bot suicides!
            for amount in range(1, len(allClusters[0]) + 1):
                for combination in combinations(list(allClusters[0]), amount):
                    notAllowed = (
                        ('3', '5'),
                        ('6', '8'),
                        ('6', '9'),
                        ('7', '9'),
                        ('6', '8', '9'),
                        ('6', '7', '9'),
                    )
                    if combination not in notAllowed:
                        actions.append(combination)
        else:
            # Normal actions
            for cluster in allClusters:
                for amount in range(1, len(cluster) + 1):
                    for combination in combinations(list(cluster), amount):
                        notAllowed = (
                            ('3', '5'),
                            ('6', '8'),
                            ('6', '9'),
                            ('7', '9'),
                            ('6', '8', '9'),
                            ('6', '7', '9'),
                        )
                        if combination not in notAllowed:
                            actions.append(combination)

        # "Legacy" to tuple
        def conversor(tup):
            return tuple(map(int, tup))

        return map(conversor, actions)


class GenericPlayer(TDQLearner):

    def __init__(self, agentName, problem):
        super(GenericPlayer, self).__init__(problem,
                                            temperature_function=make_exponential_temperature(100, 0.0019),
                                            discount_factor=0.4)
        self.name = agentName


class HumanPlayer(GenericPlayer):

    def program(self, perception):
        """We define here how the agent interfaces with the human"""
        print perception
        a = input('Write the adjacent number(s) to remove:')
        return tuple(map(int, str(a)))


class RandomPlayer(GenericPlayer):

    def program(self, perception):
        try:
            lista = self.problem.actions(perception)
            a = choice(lista)
            return a
        except:
            return None


class Fisa9Game(RLEnvironment):

    def __init__(self, agents, initialState):
        super(Fisa9Game, self).__init__(agents, initialState)
        self.lastPlayer = None

    def do_action(self, state, action, agent):
        self.lastPlayer = agent

        if action is not None:
            state = list(state)
            for number in action:
                state.remove(number)
        return tuple(state)

    def is_completed(self, state):
        return len(state) == 0

    def reward(self, state, agent):
        if self.is_completed(state):
            if self.lastPlayer == agent:
                return -1
            else:
                return 1
        else:
            return 0


if __name__ == '__main__':

    theProblem = Fisa9Problem()

    thePlayer = GenericPlayer("Trained Bot", theProblem)
    randomPlayer = RandomPlayer("FisaBot", theProblem)  # Formerly called "MullerBot" but because now it actually trains our
                                                        #   bot, we changed its name

    theGame = Fisa9Game([randomPlayer, thePlayer], tuple(range(1, 10)))

    per = PerformanceCounter(theGame.agents, [a.name for a in theGame.agents])
    print ('Training with a random player, please wait...')
    contador = 0
    for i in range(8000):
        shuffle(theGame.agents)
        theGame.run()


    per.show_statistics()

    humanPlayer = HumanPlayer("Human Player", theProblem)
    theGame.agents = [humanPlayer, thePlayer]
    while True:
        shuffle(theGame.agents)
        print ('Do you like to play?')
        theGame.run()
        print theGame.state
