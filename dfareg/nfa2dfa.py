# -*- coding: utf-8 -*-
from dfa import DeterministicFiniteAutomaton
import memoize

class SubsetsIncludingElem(object):
    def __init__(self, sub):
        self.sub   = sub
    def __contains__(self, a_set):
        return a_set & self.sub


def nfa2dfa(nfa):
    @memoize.memoize
    def transition(set_, alpha):
        ret = set()
        for elem in set_:
            ret |= nfa.transition(elem, alpha)
        return nfa.epsilon_expand( frozenset(ret) )

    return DeterministicFiniteAutomaton(
            transition,
            nfa.epsilon_expand( frozenset([ nfa.start ]) ),
            SubsetsIncludingElem(nfa.accepts)
            )
