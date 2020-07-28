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
        all_movements = ((1,),(2,),(3,),(4,),(5,),(6,),(7,),(8,),(9,),(1, 2), (3, 4), (4, 5), (3, 4, 5), (6, 7), (7, 8), (8, 9), (6, 7, 8), (7, 8, 9), (6, 7, 8, 9))
        actions = []
        #for paper in state:
        #    actions.append(tuple([paper]))
        for mov in all_movements:
            if ( self.valid_action(mov) and self.applicable_action(state, mov)):
                actions.append(mov)
        return actions

    def valid_action(self, action):
#ESTA FUNCION ES SACADA DEL AMBIENTE DE ARIEL COMPRUEBA ACCIONES VALIDAS
        action= list(action)
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
        action.sort()#ordena la lista
        #devuelve V si todos los elementos de la lista ACTION son adjascentes
        return all(y - x == 1 for x, y in zip(action[:-1], action[1:]))

    def applicable_action(self, state, action):
#ESTA FUNCION ES SACADA DEL AMBIENTE DE ARIEL, CONTROLA SI UNA ACCION ES APLICABLE
        return all(x in state for x in action)

class NuevePlayer(TDQLearner):

    def __init__(self, play_with):
        super(NuevePlayer, self).__init__(NueveProblem(),
                                              temperature_function=make_exponential_temperature(1000000, 0.01),
                                              discount_factor=0.4)
        self.name= play_with

    def program(self, perception): #sacado de REINFORCEMENT_LEARNING
        #print 'ESTOY EN 9 PLAYER'
        s = self.last_state
        #print s , 'ultimo estado'
        a = self.last_action
        #print a    , 'ultima accion'

        #state = self.problem.update_state(percept, self)
        state = perception
        #print perception , 'percepcion agente'
        actions = self.problem.actions(state)
        #print actions
        if len(actions) > 0:
            #print 'entre'
            current_action = self.exploration_function(actions, self.Q[state],
                                                       self.temperature_function(self.trials),
                                                       self.counter[state])
            #print current_action , 'ACCION TOMADA'
        else:
            current_action = None

        if s is not None and current_action:
            #print 'ENTRO  PRIMER ACCION'
            self.counter[s][a] += 1
            self.update_rule(s, a, self.last_reward, state, current_action)

        self.last_state = state
        self.last_action = current_action
        return current_action


class RandomPlayer(NuevePlayer): #ANDA

    def program(self, perception):
        #print 'percepcion  RANDOM '
        #print  perception

        try:
            return random.choice(self.problem.actions(perception))
        except:
            return None

class HumanPlayer(NuevePlayer):
    def program(self, perception):
        print perception
        a = input('Make your move (n, n, n):')
        if type(a) == int:
                return tuple([a])
        return tuple(a)

class NueveGame(RLEnvironment):

    def __init__(self, agents):
        super(NueveGame, self).__init__(agents, (1, 2, 3, 4, 5, 6, 7, 8, 9))

    def do_action(self, state, action, agent):
# ESTA FUNCION ESTA MODIFICADA COMO EN EL AMBIENTE DE ARIEL
        #print 'do_action'
        #print action, 'accion elegida'
        #state = list(state)
        #print action
        #if type(action) is tuple:
            #action = list(action)
        #self.last_agent = agent
        ##test valid action
        if not self.valid_action(action):
            raise Exception('Invalid action')
        ##test applicable action
        if not self.applicable_action(self.state, action):
            raise Exception('Inapplicable action')

        #apply action
        if type(action) is tuple:
            #print tuple([x for x in state if x not in action])
            return tuple([x for x in state if x not in action])

    def valid_action(self, action):
#ESTA FUNCION ES SACADA DEL AMBIENTE DE ARIEL COMPRUEBA ACCIONES VALIDAS
        if type(action) is tuple:
            action = list(action)
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
            action.sort()#ordena la lista
            #devuelve V si todos los elementos de la lista ACTION son adjascentes
            return all(y - x == 1 for x, y in zip(action[:-1], action[1:]))

    def applicable_action(self, state, action):
#ESTA FUNCION ES SACADA DEL AMBIENTE DE ARIEL, CONTROLA SI UNA ACCION ES APLICABLE
        if type(action) is tuple:
            return all(x in state for x in action)

    def is_completed(self, state):
        #print state
        if len(state) == 0:
            return True
        return False

    def reward(self, state, agent):
        #print  'AGENTE'
        #print agent.action.len()
        if len(state) == 0:
            if agent.last_action == agent.last_state and agent.last_state != ():
                return -100
            else:
                return 100
        else:
            return 0
        #return 0

def get_agent(name):
    return NuevePlayer(name)

if __name__ == '__main__':

    a = NuevePlayer('Agente')
    b = RandomPlayer('Random')
    c = HumanPlayer('Human')
    game = NueveGame([a, b])
    print ('Training with a random player, please wait...')
    game.agents = [a, b]
    for i in range(5000):
        game.run()

    a.dump('qlearner_agent')

    d = NuevePlayer.load('qlearner_agent')

    game.agents = [a, d]
    per = PerformanceCounter(game.agents, ['QLearnerA', 'QLearnerD'])
    for i in range(5000):
        game.run()
    #per.show_statistics()

    game.agents = [a, c]
    print ('Do you like to play?')
    game.run()
    print game.state
    if a.last_action == a.last_state and a.last_state != ():
        print 'Gana Humano'
    else:
        print 'Gana Maquina'