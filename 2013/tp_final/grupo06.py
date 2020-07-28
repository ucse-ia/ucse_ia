from simpleai.machine_learning.reinforcement_learning import TDQLearner, RLProblem, \
                                                             make_exponential_temperature, \
                                                             PerformanceCounter
from simpleai.environments import Environment

import random
from random import shuffle
from simpleai.environments import RLEnvironment
import importlib
import sys
import traceback

class PapelitosGame(RLEnvironment):

    def __init__(self, agents):
        super(PapelitosGame, self).__init__(agents, tuple(range(1,10)))

    def do_action(self, state, action, agent):
        action = list(action)

        self.last_agent = agent

        #apply action
        return tuple([x for x in state if x not in action])

    def is_completed(self, state):
        return len(state) == 0

    def reward(self, state, agent):
        if len(state)==0 and agent==self.last_agent:
            return -1000
        elif len(state)==0 and agent!=self.last_agent:
            return 1000
        else:
            return 0

class PapelitosProblem(RLProblem):
    def actions(self, state):
        valid_ranges=[(1,2), (3,4,5), (6,7,8,9)]
        #print 'Estado en actions ---->',state
        acciones_aux=[]
        actions = []
        valores_que_no_estan=[]
        action=[]
        #print 'En ACTIONS - State',state
        #Agregamos de a un solo numero
        for numero in state:
            acciones_aux.append((numero,))

        for x in valid_ranges:
            if len(x)==2:
                acciones_aux.append(x)
            elif len(x)== 3:
                acciones_aux.append((x[0],x[1]))
                acciones_aux.append((x[1],x[2]))
                acciones_aux.append((x))
            elif len(x)==4:
                acciones_aux.append((x))
                acciones_aux.append((x[0],x[1]))
                acciones_aux.append((x[1],x[2]))
                acciones_aux.append((x[2],x[3]))
                acciones_aux.append((x[0],x[1],x[2]))
                acciones_aux.append((x[1],x[2],x[3]))

        # eliminar actions invalidas - que son las que tienen numeros faltantes en el state
        for x in range(1,10):
            if not(x in state):
                valores_que_no_estan.append(x)

        #print 'Valores que no estan',valores_que_no_estan

        for x in valores_que_no_estan:
            #print 'valor que no esta',x
            for y in acciones_aux:
                if not (x in y):
                    #print 'meto y',y
                    actions.append(y)
            #print '----- actions hasta ahora: ', actions
            acciones_aux=actions
            actions=[]

        return acciones_aux

class PapelitosPlayer(TDQLearner):
    def __init__(self, name):
        super(PapelitosPlayer, self).__init__(PapelitosProblem(),
                                              temperature_function=make_exponential_temperature(1000000, 0.01),
                                              discount_factor=0.4)
        self.name=name

class RandomPlayer(PapelitosPlayer):

    def program(self, perception):
        try:
            return random.choice(self.problem.actions(self.problem.update_state(perception, self)))

        except:
            return None

def get_agent(name):
    #aca tiene que entrenar este nabo.
    agente_entrenado = PapelitosPlayer(name)
    agente_para_que_entrene = RandomPlayer('a2')
    #c = HumanPlayer('O')
    game = PapelitosGame([agente_entrenado, agente_para_que_entrene])
    print 'Entrenando el agente...... espere por favor'
    for i in range(10000):
        game.run()

    return agente_entrenado


if __name__ == '__main__':
    a = PapelitosPlayer('X')
    b = RandomPlayer('O')
    #c = HumanPlayer('O')
    game = PapelitosGame([a, b])
    game.run()