from simpleai.machine_learning.reinforcement_learning import TDQLearner, RLProblem, \
                                                                     make_exponential_temperature, \
                                                                     PerformanceCounter
from simpleai.environments import RLEnvironment
import random
from itertools import combinations

acciones_posibles = [(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (1, 2), (3, 4), (3, 4, 5), (4, 5), (6, 7), (6, 7, 8), (6, 7, 8, 9), (7, 8), (7, 8, 9), (8, 9)]
inicial = (1,2,3,4,5,6,7,8,9)

class PapelitosProblem(RLProblem):
    def actions(self, state):
        acciones =[]
        papeles_faltantes = tuple(set(inicial) - set(state))
        for accion in acciones_posibles:
            band = True
            for papel in accion:
                if papel in papeles_faltantes:
                    band = False
            if band and accion not in acciones:
                acciones.append(accion)

        return map(tuple, acciones)

class PapelitosPlayer(TDQLearner):
    def __init__(self, name):
        super(PapelitosPlayer, self).__init__(PapelitosProblem(), temperature_function=make_exponential_temperature(1000000, 0.01), discount_factor=0.4)
        self.name = name

class HumanPlayer(PapelitosPlayer):

    def __init__(self, name):
        self.name = name

class RandomPlayer(PapelitosPlayer):
    def program(self, perception):
        try:
            return random.choice(self.problem.actions(self.problem.update_state(perception, self)))
        except:
            return None

class PapelitosGame(RLEnvironment):

    def __init__(self, agents):
        super(PapelitosGame, self).__init__(agents, inicial)
        self.last_agent = None

    def is_completed(self, state):
        return len(state) == 0

    def do_action(self, state, action, agent):
        if action is not None:
            self.last_agent = agent
            state = list(state)
            action = list(action)
            return tuple([x for x in state if x not in action])
        return state

    def reward(self, state, agent):
        restantes = len(state)
        if restantes == 0 and self.last_agent != agent:
            return 1
        elif restantes == 0 and self.last_agent == agent:
            return -1
        return 0


def get_agent(name):
        a = PapelitosPlayer(name)
        b = RandomPlayer('Fernando')
        game = PapelitosGame([a, b])
        print ('Training with a random player, please wait...')
        game.agents = [a, b]
        for i in range(3000):
            game.run()
        return a

if __name__ == '__main__':
    a = get_agent('Player 1')
    b = get_agent('Player 2')
    game=PapelitosGame([a,b])
    game.agents = [a, b]
    print game.state