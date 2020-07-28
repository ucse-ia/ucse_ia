# -*- coding: utf-8 -*-
from random import shuffle
from simpleai.environments import Environment
import importlib
import sys
import traceback
import random
from simpleai.machine_learning.reinforcement_learning import \
                                        TDQLearner, RLProblem, \
                                        make_exponential_temperature, \
                                        PerformanceCounter
from simpleai.environments import RLEnvironment


INITIAL = (1, 2, 3, 4, 6, 7, 8, 9)


def tuple2list(state):
    return list(state)


def list2tuple(state):
    return tuple(state)


#------------------------------>>> PROBLEM <<----------------------------------
class PapelitosProblem(RLProblem):
    def actions(self, state):
        fila1 = []
        fila2 = []
        fila3 = []
        actions = []

        #if state == ():
        #    return []
        if len(state) > 1:    # state con mas de un elemento
            for x in state:
                actions.append((x,))

                if (x == 1) or (x == 2):
                    fila1.append(x)
                elif (x == 3) or (x == 4) or (x == 5):
                    fila2.append(x)
                else:
                    fila3.append(x)

            tablero = []

            tablero.append(fila1)
            tablero.append(fila2)
            tablero.append(fila3)

            adya = []
            anterior = 0

            for fila in tablero:
                for x in range(len(fila)):
                    adya = []
                    adya.append(fila[x])
                    anterior = fila[x]

                    for y in range((x + 1), len(fila)):
                        resta = fila[y] - anterior

                        if (resta == 1):
                            adya.append(fila[y])
                            actions.append(tuple(adya))
                            anterior = fila[y]
                            resta = 0
        else:    # state de un solo elemento (integer)
            actions.append(tuple(state,))

        return actions


#--------------------------->>> AMBIENTE <<<-----------------------------------
class PapelitosGame(RLEnvironment):
    def __init__(self, agents):
        shuffle(agents)
        super(PapelitosGame, self).__init__(agents, tuple(range(1, 10)))
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
        ## True si son adyacentes y en igual fila
        if not (1 <= len(action) <= 4):
            return False

        # Numero validos
        if not all(x in range(1, 10) for x in action):
            return False

        # Todos en la misma fila
        valid_ranges = [(1, 2), (3, 5), (6, 9)]
        a_min = min(action)
        a_max = max(action)

        for r_min, r_max in valid_ranges:
            if a_min <= r_max:
                break

        if not (a_min >= r_min and a_max <= r_max):
            return False

        # Adyacente
	action = list(action)
        action.sort()
        return all(y - x == 1 for x, y in zip(action[:-1], action[1:]))

    def applicable_action(self, state, action):
        ## True si las acciones estan en el estado
        return all(x in state for x in action)

    def is_completed(self, state):
        # True si el tablero queda vacio
        return len(state) == 0

    def load_agent(module):
       m = importlib.import_module(module)

       return m.get_agent(module)

    def play_againts(agent1, agent2):
        game = PapelitosGame([agent1, agent2])
        winner = game.play()
        print 'And the winner is: %s' % winner.name

        return winner

    def reward(self, state, agent):
        # Recibe el estado con la accion aplicada , y el agente que la realizo
        if len(state) == 0 and agent == self.last_agent:
            # Tablero vacio y movida del ultimo agente
            return -1    # Pierde
        elif len(state) == 0 and agent != self.last_agent:
            # Tablero vacio pero el agente no es el ultimo que movio
            return 1    # Gana
        elif len(state) != 0:
        # Mientras queden fichas en el tablero
            return 0    # Neutro


#------------------------------->>> AGENTE <<----------------------------------
# Agente que entrenamos
class botplayer(TDQLearner):
    def __init__(self, name):
        super(botplayer, self).__init__(PapelitosProblem(),
            temperature_function=make_exponential_temperature(1000000, 0.01),
            discount_factor=0.4)
	self.name = name


#----------------->> AGENTE RANDOM PARA ENTRENAR CON BOT <<--------------------
class RandomPlayer(botplayer):
    def program(self, perception):
        try:
            return random.choice(self.problem.actions(self.problem.update_state(perception, self)))
        except:
            return None


class HumanPlayer(object):
    def __init__(self, name):
        self.name = name

    def program(self, percept):
        print '======================================='
        print 'Tablero actual: ', percept
        a = input('%s, hacer movimiento: ' % self.name)
        if type(a) == int:
            return [a]
        return list(a)


def get_agent(name):
    a = botplayer('grupo01')    # Agente de la maquina
    b = RandomPlayer('PC')    # Agente para entrenar
    # c = HumanPlayer('grupo01')    # Agente para nosotros
    game = PapelitosGame([a, b])    # Para recibir las coordenadas
    print ('Entrenando con Jugador Random...')
    for i in range(3000):    # Veces que va a entrenar
    	game.run()

    #return HumanPlayer(name)
    return a

#------------------------------->>> MAIN <<------------------------------------
'''if __name__ == '__main__':
    a = botplayer()    # Agente de la maquina
    b = RandomPlayer()    # Agente para entrenar
    # c = HumanPlayer()    # Agente para nosotros
    game = PapelitosGame([a, b])    # Para recibir las coordenadas
    print ('Entrenando con Jugador Random...')
    for i in range(3000):    # Veces que va a entrenar
        game.run()
'''
