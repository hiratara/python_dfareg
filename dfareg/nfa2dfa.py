#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-

from dfa import DeterministicFiniteAutomaton

class SubsetsIncludingElem(object):
    """
    the set of subsets of "super_" including an element of "sub".

    >>> from dfareg import algebra
    >>> s = algebra.subsets_including_elem(set([1,2,3]), set([1,3]))
    >>> for i in s: 
    ...     print i
    ... 
    frozenset([3])
    frozenset([1, 2])
    frozenset([2, 3])
    frozenset([1])
    frozenset([1, 3])
    frozenset([1, 2, 3])
    >>> set([1,2]) in s
    True
    >>> set([2]) in s
    False
    """
    def __init__(self, sub):
        self.sub   = sub
    def __contains__(self, a_set):
        return a_set & self.sub

def nfa2dfa(nfa):

    def transition(set_, alpha):
        ret = set()
        for elem in set_:
            ret |= nfa.transition(elem, alpha)
        return nfa.epsilon_expand(ret)

    return DeterministicFiniteAutomaton(
            transition,
            nfa.epsilon_expand(set([ nfa.start ]) ),
            SubsetsIncludingElem(nfa.accepts)
            )

if __name__ == '__main__':
    regexp = u"あ(い\|う|え*(かき|くけこ))*お"
    regexp = u"A*(B|C)*"
    nfastate = lexer.compile_to_nfa(regexp)
    for s in nfastate.all_states():
        print s

    nfa2dfa(nfastate)
