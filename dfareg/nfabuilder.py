#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-

import nfa

class NFAFragment(object):
    """
    >>> b = nfa.NFABuilder("abcde")
    >>> b.start
    1
    >>> s1 = b.new_state()
    >>> s2 = b.new_state()
    >>> b.connect(b.start, None, s2)
    >>> b.connect(b.start, "b", s1)
    >>> b.accepting_state(b.start)
    >>> b.accepting_state(s2)
    >>> am = b.build()
    >>> am.start
    1
    >>> am.accepts
    frozenset([1, 3])
    >>> am.states
    frozenset([1, 2, 3])
    >>> am.transition(1, None)
    frozenset([3])
    >>> am.transition(3, None)
    frozenset([])
    >>> am.transition(1, "b")
    frozenset([2])
    >>> 
    """
    def __init__(self):
        self.accepts = set()
        self.states  = set()
        self.map     = dict()
        self.start   = None  # should be set later

    def connect(self, from_, char, to):
        if from_ not in self.states: self.states.add(from_)
        if to    not in self.states: self.states.add(to)
        slot = self.map.setdefault( (from_, char), set() )
        slot.add(to)

    def build(self):
        def transition(state, char):
            return frozenset(self.map.get( (state, char), []))

        return nfa.NondeterministicFiniteAutomaton(
            transition,
            self.start,
            frozenset(self.accepts)
            )


state_count = 0
def new_state():
    global state_count
    state_count += 1
    return state_count

def new_fragment():
    return NFAFragment()

def merge_fragment(frag1, frag2):
    new_frag = new_fragment()

    new_frag.accepts = frag1.accepts.union(frag2.accepts)
    new_frag.states  = frag1.states.union(frag2.states)
    new_frag.map     = dict()
    for k, v in frag1.map.iteritems():
        new_frag.map[k] = v
    for k, v in frag2.map.iteritems():
        new_frag.map[k] = v

    return new_frag


class Union(object):
    def __init__(self, operand1, operand2):
        self.operand1 = operand1
        self.operand2 = operand2
    def assemble(self):
        frag1 = self.operand1.assemble()
        frag2 = self.operand2.assemble()
        frag = merge_fragment(frag1, frag2)

        a = new_state()
        frag.connect(a, "", frag1.start)
        frag.connect(a, "", frag2.start)
        frag.start = a

        return frag


class Concat(object):
    def __init__(self, operand1, operand2):
        self.operand1 = operand1
        self.operand2 = operand2

    def assemble(self):
        frag1 = self.operand1.assemble()
        frag2 = self.operand2.assemble()
        frag = merge_fragment(frag1, frag2)

        for state in frag1.accepts:
            frag.connect(state, "", frag2.start)
            frag.accepts.remove(state)

        frag.start = frag1.start

        return frag

class Star(object):
    def __init__(self, operand):
        self.operand = operand

    def assemble(self):
        frag = self.operand.assemble()
        for state in frag.accepts:
            frag.connect(state, "", frag.start)

        a = new_state()
        frag.accepts.add(a)
        frag.connect(a, "", frag.start)

        frag.start = a

        return frag

class Character(object):
    def __init__(self, char):
        self.char = char

    def assemble(self):
        frag = new_fragment()
        a = new_state()
        b = new_state()
        frag.connect(a, self.char, b)
        frag.accepts.add(b)
        frag.start = a
        return frag

if __name__ == '__main__':
    b = NFABuilder()
    f = b.new_fragment()
    print f.start
    s1 = f.new_state()
    s2 = f.new_state()
    f.connect(f.start, "", s2)
    f.connect(f.start, "b", s1)
    f.accepts.add(f.start)
    f.accepts.add(s2)
    am = b.build(f)
    print am.start
    print am.accepts
    # print am.states
    print am.transition(1, "")
    print am.transition(3, "")
    print am.transition(1, "b")
