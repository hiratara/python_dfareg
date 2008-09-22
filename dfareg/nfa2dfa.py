#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-

from dfa import DeterministicFiniteAutomaton

def _epsilon_expand(nfa, set_):
    # 空文字を辿るべき状態を集めたキュー
    que = set( set_ )
    # 辿り終わった状態
    done = set()
    while que:
        # キューから取り出す
        stat = que.pop()
        # 空文字によって辿れる遷移を辿る
        nexts = nfa.transition(stat, "")
        # この状態は辿り終わったので、保存
        done.add(stat)
        # 辿って出て来た状態を、さらに空文字で辿るのに、キューに居れる
        for next_stat in nexts:
            # 辿り終わってない要素だけ
            if not next_stat in done: que.add(next_stat)

    return done


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
            ret |= _epsilon_expand(nfa, nfa.transition(elem, alpha) )
        return ret

    return DeterministicFiniteAutomaton(
            transition,
            _epsilon_expand(nfa, set([ nfa.start ]) ),
            SubsetsIncludingElem(nfa.accepts)
            )

if __name__ == '__main__':
    regexp = u"あ(い\|う|え*(かき|くけこ))*お"
    regexp = u"A*(B|C)*"
    nfastate = lexer.compile_to_nfa(regexp)
    for s in nfastate.all_states():
        print s

    nfa2dfa(nfastate)
