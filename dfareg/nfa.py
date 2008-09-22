#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-

class NondeterministicFiniteAutomaton(object):
    """
    An nondeterministic finite automaton implementation.
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
        return NFARuntime(self)
