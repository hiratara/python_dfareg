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
        if not char in self.DFA.alphabet: 
            raise "bad char: %s" % char
        self.cur_state = self.DFA.transition(self.cur_state, char)
        if not self.cur_state in self.DFA.states:
            raise "bad state. (maybe bad transition function.)"

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
                 states     , # a finite set of states
                 alphabet   , # a finite set called the alphabet
                 transition , # a transition function
                 start      , # a start state
                 accepts    , # a set of accept states
                 ):
        """
        Instanciate new deterministic finite automaton 
        from 5-tuple.
        """
        self.states     = states
        self.alphabet   = alphabet
        self.transition = transition
        self.start      = start
        self.accepts    = accepts
        self._check_parameter()

    def _check_parameter(self):
        """
        check whether params inputted are correct type.
        """
        if not self.start in self.states: 
            raise "bad start parameter."
        if not self.accepts.issubset(self.states): 
            raise "bad accepts parameter."

    def get_runtime(self):
        return DFARuntime(self)

if __name__ == '__main__':
    pass



