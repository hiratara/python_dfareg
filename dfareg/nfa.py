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
            )

    def do_transition(self, char):
        next_states = set()
        for state in self.cur_states:
            next_states = next_states.union(
                self.NFA.transition(state, char)
                )
        next_states = self._expand_epsilon(next_states)

        self.cur_states = next_states

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
