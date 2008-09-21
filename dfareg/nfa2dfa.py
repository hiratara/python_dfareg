#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-

from dfa import DeterministicFiniteAutomaton
from algebra import power, subsets_including_elem, expand_set

def nfa2dfa(nfa):
    def epsilon_expand(set_):
        return expand_set(
            set_, 
            lambda e: nfa.transition(e, None), 
            nfa.states
            )

    def transition(set_, alpha):
        ret = set()
        for elem in set_:
            ret |= epsilon_expand( nfa.transition(elem, alpha) )
        return ret

    return DeterministicFiniteAutomaton(
            power(nfa.states),
            nfa.alphabet,
            transition,
            epsilon_expand( set([ nfa.start ]) ),
            subsets_including_elem(nfa.states, nfa.accepts)
            )


if __name__ == '__main__':
    regexp = u"あ(い\|う|え*(かき|くけこ))*お"
    regexp = u"A*(B|C)*"
    nfastate = lexer.compile_to_nfa(regexp)
    for s in nfastate.all_states():
        print s

    nfa2dfa(nfastate)
