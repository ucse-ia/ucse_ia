from simpleai.machine_learning.reinforcement_learning import TDQLearner, RLProblem, \
                                                             make_exponential_temperature, \
                                                             PerformanceCounter
import random
from simpleai.environments import RLEnvironment

def get_agent(name):
    a = FizaPlayer(1)
    a.name=name
    b = RandomPlayer(0)
    game = FizaGame([a, b])
    for i in range(7500):
        game.run()
        random.shuffle(game.agents)
    return a

class FizaProblem(RLProblem):
    def __init__(self):
        self.acciones=[
                        (1,),(2,),(3,),(4,),(5,),(6,),(7,),(8,),(9,),(1,2),(3,4),(4,5),(6,7),(7,8),
                        (8,9),(3,4,5),(6,7,8),(7,8,9),(6,7,8,9),
                        ]

    def actions(self, state):
        #devuelve las acciones que puede hacer segun el estado
        actions = self.acciones[:]
        for indice in range(1,10):
            if not indice in state:
                for action in actions[:]:
                    if indice in action:
                        actions.remove(action)
        return tuple(actions)



class FizaPlayer(TDQLearner):

    def __init__(self, play_with):
        super(FizaPlayer, self).__init__(FizaProblem(),
                                              temperature_function=make_exponential_temperature(1000, 0.001),
                                              discount_factor=0.4)
        self.play_with = play_with
        self.name = ''

class RandomPlayer(FizaPlayer):

   def program(self, perception):
       try:
           return random.choice(self.problem.actions(self.problem.update_state(perception, self)))
       except:
           return None


class FizaGame(RLEnvironment):

    def __init__(self, agents):
        super(FizaGame, self).__init__(agents, (1,2,3,4,5,6,7,8,9))

    def do_action(self, state, action, agent):
        temp = list(state)
        act = list(action)
        for numero in act:
            temp.remove(numero)
        self.ultimo_agente = agent.play_with #guardo el agente que realiza la accion
        return tuple(temp)

    def is_completed(self, state):
        return not ((len(state) != 0) and all([self.reward(state, x) == 0 for x in self.agents])) #se fija si el len del estado es igual a 0 y todos los agentes tienen recompenza 

    def reward(self, state, agent):
        if len(state) == 0:
            if agent.play_with == self.ultimo_agente:
                return -1
            else:
                return 1
        else:
            return 0

if __name__ == '__main__':
    a = FizaPlayer(1)
    b = RandomPlayer(0)
    game = FizaGame([a, b])
    print ('Training with a random player, please wait...')
    for i in range(6000):
        game.run()
        random.shuffle(game.agents)
    per = PerformanceCounter(game.agents, ['QLearnerA', 'QLearnerD'])
    for i in range(6000):
        game.run()
    per.show_statistics()
