#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-
"""
An joke deterministic finite automaton implementation.

"""

class DFARuntime(object):
    def __init__(self, DFA):
        self.DFA = DFA
        self.cur_state = self.DFA.start

    def do_transition(self, char):
        self.cur_state = self.DFA.transition(self.cur_state, char)

    def is_accept_state(self):
        return self.cur_state in self.DFA.accepts

    def does_accept(self, input):
        """
        Check whether an input is accepted by this automaton.
        """
        for alphabet in input:
            self.do_transition(alphabet)
        return self.is_accept_state()

class DeterministicFiniteAutomaton(object):
    """
    An deterministic finite automaton implementation.
    It's just for fun. So, you shouldn't use this in your products.
    """
    def __init__(self, 
                 transition , # a transition function
                 start      , # a start state
                 accepts    , # a set of accept states
                 ):
        """
        Instanciate new deterministic finite automaton 
        from 5-tuple.
        """
        self.transition = transition
        self.start      = start
        self.accepts    = accepts

    def get_runtime(self):
        return DFARuntime(self)

if __name__ == '__main__':
    pass



