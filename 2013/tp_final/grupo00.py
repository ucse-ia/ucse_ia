# -*- coding: utf-8 -*-


class HumanPlayer(object):

    def __init__(self, name):
        self.name = name

    def program(self, percept):
        print '======================================='
        print 'Current board:', percept
        a = input('%s, make your move:' % self.name)
        if type(a) == int:
            return [a]
        return tuple(a)


def get_agent(name):
    return HumanPlayer(name)