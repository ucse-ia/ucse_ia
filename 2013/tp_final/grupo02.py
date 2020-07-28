# -*- coding: utf-8 -*-
from simpleai.machine_learning.reinforcement_learning import TDQLearner, RLProblem, \
                                                             make_exponential_temperature, \
                                                             PerformanceCounter
import random
import numpy
import matplotlib
import dateutil
from simpleai.environments import RLEnvironment


class NueveProblem(RLProblem):

    def actions(self, state):
        movements = ((1, 2), (3, 4), (4, 5), (3, 4, 5), (6, 7), (7, 8), (8, 9), (6, 7, 8), (7, 8, 9), (6, 7, 8, 9))
        actions = []
        for paper in state:
            actions.append(tuple([paper]))
        for mov in movements:
            possible = True
            for paper in mov:
                if paper not in state:
                    possible = False
            if possible == True:
                actions.append(mov)
        return tuple(actions)


class NuevePlayer(TDQLearner):

    def __init__(self, name):
        self.name = name
        super(NuevePlayer, self).__init__(NueveProblem(),
                                              temperature_function=make_exponential_temperature(1000000, 0.01),
                                              discount_factor=0.4)

class RandomPlayer(NuevePlayer):

    def program(self, perception):
        try:
            return random.choice(self.problem.actions)
        except:
            return None

class HumanPlayer(NuevePlayer):

    def program(self, perception):
        f1 = [1, 2]
        f2 = [3, 4, 5]
        f3 = [6, 7, 8, 9]
        for i, n in enumerate(f1):
            if n not in perception:
                f1[i] = 0
        for i, n in enumerate(f2):
            if n not in perception:
                f2[i] = 0
        for i, n in enumerate(f3):
            if n not in perception:
                f3[i] = 0
        print ('Current board:')
        print '   ', f1
        print ' ', f2
        print f3
        a = input('Make your move (n, n, n):')
        if type(a) == int:
                return tuple([a])
        return tuple(a)

class NueveGame(RLEnvironment):

    def __init__(self, agents):
        super(NueveGame, self).__init__(agents, (1, 2, 3, 4, 5, 6, 7, 8, 9))

    def do_action(self, state, action, agent):
        state = list(state)
        if action is not None:
            for paper in action:
                state.remove(paper)
        return tuple(state)

    def is_completed(self, state):
        if len(state) == 0:
            return True
        return False

    def reward(self, state, agent):
        f1 = [1, 2]
        f2 = [3, 4, 5]
        f3 = [6, 7, 8, 9]
        reco = 0
        cant_fichas = len(state)
        def cantidad_adyascentes(estado):
            cant_adya = 0
            ficha_ant = 0
            for ficha in estado:
                if ficha_ant != 0:
                    if  ficha_ant in f1 and ficha in f1:
                        cant_adya = cant_adya + 1
                    elif ficha_ant in f2 and ficha in f2:
                        if ficha_ant + 1 == ficha:
                            cant_adya = cant_adya + 1
                    elif ficha_ant in f3 and ficha in f3:
                        if ficha_ant + 1 == ficha:
                            cant_adya = cant_adya + 1
                ficha_ant = ficha
            return cant_adya
        cant_adya = cantidad_adyascentes(state)

        if cant_adya == 0 and ((-1)**cant_fichas) == -1:
            reco = reco + cant_fichas
        elif cant_adya == 0 and ((-1)**cant_fichas) == 1:
            reco = reco - cant_fichas
        else:
            cant_movs = 0.0
            cant_movs_win = 0.0
            movements = ((1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (1, 2), (3, 4),
                         (4, 5), (3, 4, 5), (6, 7), (7, 8), (8, 9), (6, 7, 8), (7, 8, 9), (6, 7, 8, 9))
            for mov in movements:
                possible = True
                for paper in mov:
                    if paper not in state:
                        possible = False
                if possible == True:
                    cant_movs = cant_movs + 1
                    state1 = list(state)
                    for paper in mov:
                        state1.remove(paper) 
                    cant_adya = cantidad_adyascentes(state1)
                    if cant_adya == 0  and (-1)**len(state1) == -1:
                        cant_movs_win = cant_movs_win + 1
            if (cant_movs_win / cant_movs) == 0:
                reco = 1
        return reco

def get_agent(name):
    a = NuevePlayer(name)
    b = RandomPlayer('Random')
    c = HumanPlayer('Human')
    game = NueveGame([a, b])
    #print ('Training with a random player, please wait...')
    #per = PerformanceCounter(game.agents, ['QlearnerA', 'QLearnerD'])
    for i in range(10000):
        game.run()
    #per.show_statistics()
    
    

    

##    game.agents = [a, c]
##    print ('Do you like to play?')
##    game.run()
##    print game.state
    return a

if __name__ == '__main__':
    get_agent('Grupo02')
