#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-

import nfa

class NFAStateGenerator(object):
    def __init__(self):
        self.counter = 0

    def new_state(self):
        self.counter += 1
        return self.counter

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
    def __init__(self, parent):
        self.parent  = parent
        self.accepts = set()
        self.states  = set()
        self.map     = dict()
        self.start   = None  # should be set later

    def new_state(self):
        state = self.parent.generate_state()
        self.states.add(state)
        return state

    def connect(self, from_, char, to):
        slot = self.map.setdefault( (from_, char), set() )
        slot.add(to)


class NFABuilder(object):
    def __init__(self, alphabet, generator = None):
        if generator is None:
            self.generator = NFAStateGenerator()
        else:
            self.generator = generator
        self.alphabet = alphabet

    def generate_state(self):
        return self.generator.new_state()

    def new_fragment(self):
        return NFAFragment(self)

    def merge_fragment(self, frag1, frag2):
        new_frag = self.new_fragment()

        new_frag.accepts = frag1.accepts.union(frag2.accepts)
        new_frag.states  = frag1.states.union(frag2.states)
        new_frag.map     = dict()
        for k, v in frag1.map.iteritems():
            new_frag.map[k] = v
        for k, v in frag2.map.iteritems():
            new_frag.map[k] = v

        return new_frag


    def build(self, fragment):
        def transition(state, char):
            return frozenset(fragment.map.get( (state, char), []))

        return nfa.NondeterministicFiniteAutomaton(
            frozenset(fragment.states),
            self.alphabet,
            transition,
            fragment.start,
            frozenset(fragment.accepts)
            )







if __name__ == '__main__':
    b = NFABuilder("abcde")
    f = b.new_fragment()
    print f.start
    s1 = f.new_state()
    s2 = f.new_state()
    f.connect(f.start, None, s2)
    f.connect(f.start, "b", s1)
    f.accepts.add(f.start)
    f.accepts.add(s2)
    am = b.build(f)
    print am.start
    print am.accepts
    print am.states
    print am.transition(1, None)
    print am.transition(3, None)
    print am.transition(1, "b")

