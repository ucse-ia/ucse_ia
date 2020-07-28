# -*- TP Final Inteligencia Artificial - Denardi - Carrizzo - Luna -*-
from simpleai.machine_learning.reinforcement_learning import TDQLearner, RLProblem, \
                                                             make_exponential_temperature, \
                                                             PerformanceCounter
import random
from simpleai.environments import RLEnvironment


class TpFinalProblem(RLProblem):
    def actions(self, state):
        #Posibles combinaciones de numero a quitar
        actions = []
        posibles = [(1,), (1, 2), (2,), (3,), (3, 4), (4,), (3, 4, 5), (5,), (4, 5), (6,), (7,), (8,), (9,), (6, 7), (7, 8), (8, 9), (6, 7, 8), (7, 8, 9), (6, 7, 8, 9)]
        actions = posibles[:]
        for jugada in posibles:
            for nro in jugada:
                if nro not in state and jugada in actions:
                    actions.remove(jugada)
        return actions


class TpFinalPlayer(TDQLearner):
    def __init__(self, name):
        super(TpFinalPlayer, self).__init__(TpFinalProblem(),
                                              temperature_function=make_exponential_temperature(1000000, 0.01),
                                              discount_factor=0.4)
        self.name = name


class RandomPlayer(TpFinalPlayer):
    def program(self, perception):
        try:
            return random.choice(self.problem.actions(perception))
        except:
            return None


class TpFinalGame(RLEnvironment):
    def __init__(self, agents):
        super(TpFinalGame, self).__init__(agents, tuple(range(1, 10)))
        self.last_agent = None

    def do_action(self, state, action, agent):
        state = list(state)
        self.last_agent = agent
        if len(state) >= len(action):
            for numero in action:
                state.remove(numero)
        return tuple(state)

    def is_completed(self, state):
        return len(state) == 0

    def reward(self, state, agent):
        restantes = len(state)
        if restantes == 0 and not self.last_agent == agent:
            return 10
        elif restantes == 0 and self.last_agent == agent:
            return -10
        return 0


def get_agent(name):

    a = TpFinalPlayer(name)
    b = RandomPlayer('PC')
    game = TpFinalGame([a, b])
    print ('Training with a random player, please wait...')
    game.agents = [a, b]
    for i in range(3000):
        game.run()

    return a

if __name__ == '__main__':
    get_agent('Player')