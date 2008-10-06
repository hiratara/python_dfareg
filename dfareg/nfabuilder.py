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
    def __init__(self, context):
        self.context = context
        self.accepts = set()
        self.map     = dict()
        self.start   = None  # should be set later

    def new_state(self):
        state = self.context.generate_state()
        return state

    def connect(self, from_, char, to):
        slot = self.map.setdefault( (from_, char), set() )
        slot.add(to)

    def __or__(self, frag):
        if frag.context is not self.context:
            raise Exception("can't merge other context fragment")

        new_frag = self.context.new_fragment()
        new_frag.accepts = self.accepts.union(frag.accepts)
        new_frag.map     = dict()
        for k, v in self.map.iteritems():
            new_frag.map[k] = v
        for k, v in frag.map.iteritems():
            new_frag.map[k] = v

        return new_frag

    def build(self):
        def transition(state, char):
            return frozenset(self.map.get( (state, char), []))

        return nfa.NondeterministicFiniteAutomaton(
            transition,
            self.start,
            frozenset(self.accepts)
            )


class Context(object):
    def __init__(self):
        self._state_count = 0

    def new_fragment(self):
        return NFAFragment(self)

    def generate_state(self):
        self._state_count += 1
        return self._state_count


class Union(object):
    def __init__(self, operand1, operand2):
        self.operand1 = operand1
        self.operand2 = operand2

    def assemble(self, context):
        frag1 = self.operand1.assemble(context)
        frag2 = self.operand2.assemble(context)
        frag = frag1 | frag2

        a = frag.new_state()
        frag.connect(a, "", frag1.start)
        frag.connect(a, "", frag2.start)
        frag.start = a

        return frag


class Concat(object):
    def __init__(self, operand1, operand2):
        self.operand1 = operand1
        self.operand2 = operand2

    def assemble(self, context):
        frag1 = self.operand1.assemble(context)
        frag2 = self.operand2.assemble(context)
        frag = frag1 | frag2

        for state in frag1.accepts:
            frag.connect(state, "", frag2.start)
            frag.accepts.remove(state)

        frag.start = frag1.start

        return frag

class Star(object):
    def __init__(self, operand):
        self.operand = operand

    def assemble(self, context):
        frag = self.operand.assemble(context)
        for state in frag.accepts:
            frag.connect(state, "", frag.start)

        a = frag.new_state()
        frag.accepts.add(a)
        frag.connect(a, "", frag.start)

        frag.start = a

        return frag

class Character(object):
    def __init__(self, char):
        self.char = char

    def assemble(self, context):
        frag = context.new_fragment()
        a = frag.new_state()
        b = frag.new_state()
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
