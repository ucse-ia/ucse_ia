# -*- coding: utf-8 -*-
from simpleai.machine_learning.reinforcement_learning import TDQLearner, RLProblem, \
                                                                     make_exponential_temperature, \
                                                                     PerformanceCounter
from simpleai.environments import RLEnvironment
import random
from itertools import combinations

state_initial = (1,2,3,4,5,6,7,8,9)

class PapelitosProblem(RLProblem):
    def actions(self, state):
        actions = []
        stateaux= []
        x1=0
        x2=2
        y=0
        if state == ():
            return ()
        for x in range(9):
            try:
                if state[y]-1==x:
                    stateaux.append(x+1)
                    y=y+1
                else:
                    stateaux.append(0)
            except:
                    stateaux.append(0)
        for position in range (3):
            w=1
            while w <= len(stateaux[x1:x2+position]):
                laux=[]
                for x in stateaux[x1:x2+position]:
                    laux.append(x)
                    if w==len(laux) and 0 not in laux:
                        actions.append(laux)
                        laux=[]
                    if 0 in laux:
                        laux=[]
                laux=[]
                if stateaux[x1+1:x2+position] not in actions and 0 not in stateaux[x1+1:x2+position]:
                    actions.append(stateaux[x1+1:x2+position])
                w=w+1
            if x1==0:
                x1=x2
            else:
                if x1%2==0:
                    x1=x2+1
                else:
                    x1=x2
            x2=x2*2-position
        return map(tuple,actions)

class PapelitosPlayer(TDQLearner):
    def __init__(self, name):
        super(PapelitosPlayer, self).__init__(PapelitosProblem(), temperature_function=make_exponential_temperature(1000000, 0.01), discount_factor=0.4)
        self.name = name

class HumanPlayer(PapelitosPlayer):

    def __init__(self, name):
        self.name = name

    def program(self, perception):
        print perception
        a = input('%s, make your move:' % self.name)
        if type(a) == int:
            return [a]
        return list(a)

class RandomPlayer(PapelitosPlayer):
    def program(self, perception):
        try:
            return random.choice(self.problem.actions(self.problem.update_state(perception, self)))
        except:
            return None

class PapelitosGame(RLEnvironment):

    def __init__(self, agents):
        super(PapelitosGame, self).__init__(agents, state_initial)
        self.last_agent = None
        self.last_action = None

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

    def is_completed(self, state):
        return len(state) == 0

    def do_action(self, state, action, agent ):
        if action is not None:
            self.last_agent = agent
            self.last_action = action
            state = list(state)
            action = list(action)
            return tuple([x for x in state if x not in action])
        return state

    def reward(self, state, agent):
        x=self.last_action
        a=0
        if x is not None:
            a=len(x)
            if set(self.last_action) ==4:
                a=a+5
        if len(state)%2==0:
            b=0
        else:
            b=2
        if len(state)==0:
            if self.last_agent==agent:
                return -10
            else:
                return 1+a+b
        else:
            return 0

def get_agent(name):
        a = PapelitosPlayer(name)
        b = RandomPlayer('Fisa')
        game = PapelitosGame([a, b])
        print ('Training with a random player, please wait...')
        game.agents = [a, b]
        for i in range(3000):
            game.run()
        #a.dump('qlearner_agent')
        return a

if __name__ == '__main__':
    c = HumanPlayer('grupo04')
    b = get_agent('grupo04')
    game=PapelitosGame([b,c])
    game.agents = [b, c]
    winner = game.play()
    print 'And the winner is: %s' % winner.name
    print ('Do you like to play?')
    game.run()
    print game.state




