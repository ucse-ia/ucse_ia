# -*- coding: utf-8 -*-
from simpleai.environments import Environment
import importlib
import sys
import traceback
import os
import itertools


class PapelitosGame(Environment):

    def __init__(self, agents):
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

    def step(self, viewer=None):
        "This method evolves one step in time"
        if not self.is_completed(self.state):
            for agent in self.agents:
                self.last_agent = agent
                action = agent.program(self.percept(agent, self.state))
                next_state = self.do_action(self.state, action, agent)
                if viewer:
                    viewer.event(self.state, action, next_state, agent)
                self.state = next_state
                if self.is_completed(self.state):
                    return

    def winner(self):
        a0, a1 = self.agents
        return a0 if a1 is self.last_agent else a1

    def do_action(self, state, action, agent):
        action = list(action)
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


def load_agent(module):
    print 'loading agent: ', module
    m = importlib.import_module(module)
    return m.get_agent(module)


def play_againts(agent1, agent2):
    game = PapelitosGame([agent1, agent2])
    winner = game.play()
    return winner


def championship():
    teams = {}

    for f in os.listdir(os.path.dirname(os.path.abspath(__file__))):
        if f.startswith('grupo') and f[-2:] == 'py' and int(f[5:7]) < 20:
            name = f[:7]
            teams[name] = (None, 0)

    for j in range(3):
        print 'Training number:', j
        for name in teams.keys():
            teams[name] = (load_agent(name), teams[name][1])
        for i in range(10):
            print 'Round', i
            for name1, name2 in itertools.permutations(teams.keys(), 2):
                a1, s1 = teams[name1]
                a2, s2 = teams[name2]

                #print '%s (%d) againts %s (%d)' % (a1.name, s1, a2.name, s2),
                winner = play_againts(a1, a2)
                if winner is a1:
                    teams[a1.name] = (a1, s1 + 1)
                else:
                    teams[a2.name] = (a2, s2 + 1)

    #results
    positions = teams.values()
    positions.sort(key=lambda x: -x[1])
    linea = '+%s+%s+%s+' % ('-' * 3, '-' * 10, '-' * 3)
    print linea
    print '|Pos|Grupo     |Pts|'
    print linea
    for pos, (agent, score) in enumerate(positions):
        print '|%3d|%10s|%3d|' % (pos + 1, agent.name, score)
        print linea


if __name__ == '__main__':
    if len(sys.argv) == 1:
        championship()
    elif len(sys.argv) == 3:
        print 'And the winner is: %s' % play_againts(load_agent(sys.argv[1]), load_agent(sys.argv[2])).name
    else:
        print 'Use sin argumentos para campeonato o pase el nombre de 2 modulos para jugar en contra'
