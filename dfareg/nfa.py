#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-

from algebra import expand_set

class NFARuntime(object):
    def __init__(self, NFA):
        self.NFA = NFA
        self.cur_states = self._expand_epsilon( set([ self.NFA.start ]) )

    def _expand_epsilon(self, states):
        """
        与えられた状態集合からε(None)で到達できるsetを得る
        """
        return expand_set(
            states, 
            lambda e: self.NFA.transition(e, None), 
            self.NFA.states
            )

    def do_transition(self, char):
        if not char in self.NFA.alphabet: 
            raise "bad char: %s" % char

        next_states = set()
        for state in self.cur_states:
            next_states = next_states.union(
                self.NFA.transition(state, char)
                )
        next_states = self._expand_epsilon(next_states)

        self.cur_states = next_states

        if not self.cur_states.issubset(self.NFA.states):
            raise "bad state. (maybe bad transition function.)"

    def is_accept_state(self):
        for state in self.cur_states:
            if state in self.NFA.accepts: return True
        return False

    def does_accept(self, input):
        """
        Check whether an input is accepted by this automaton.
        """
        for alphabet in input:
            self.do_transition(alphabet)
        return self.is_accept_state()


class NondeterministicFiniteAutomaton(object):
    """
    An nondeterministic finite automaton implementation.
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
        return NFARuntime(self)
