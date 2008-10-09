#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-
import nfa
from copy import deepcopy

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
        self.start   = None  # 整数型
        self.accepts = None  # frozenset型
        self.map     = dict()

    def connect(self, from_, char, to):
        slot = self.map.setdefault( (from_, char), set() )
        slot.add(to)

    def new_skelton(self):
        # コピーして返す
        new_frag = NFAFragment()
        new_frag.map = deepcopy(self.map)
        return new_frag

    def __or__(self, frag):
        new_frag = self.new_skelton()
        for k, v in frag.map.iteritems():
            new_frag.map[k] = v.copy()

        return new_frag

    def build(self):
        map_ = self.map
        def transition(state, char):
            return frozenset(map_.get( (state, char), []))

        return nfa.NondeterministicFiniteAutomaton(
            transition,
            self.start,
            self.accepts
            )


class Context(object):
    def __init__(self):
        self._state_count = 0

    def new_state(self):
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

        a = context.new_state()
        frag.connect(a, "", frag1.start)
        frag.connect(a, "", frag2.start)

        frag.start = a
        frag.accepts = frag1.accepts | frag2.accepts

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

        frag.start   = frag1.start
        frag.accepts = frag2.accepts

        return frag

class Star(object):
    def __init__(self, operand):
        self.operand = operand

    def assemble(self, context):
        frag_orig = self.operand.assemble(context)
        frag = frag_orig.new_skelton()

        for state in frag_orig.accepts:
            frag.connect(state, "", frag_orig.start)

        a = context.new_state()
        frag.connect(a, "", frag_orig.start)

        frag.start = a
        frag.accepts = frag_orig.accepts | frozenset([a])

        return frag

class Character(object):
    def __init__(self, char):
        self.char = char

    def assemble(self, context):
        frag = NFAFragment()
        a = context.new_state()
        b = context.new_state()
        frag.connect(a, self.char, b)

        frag.start = a
        frag.accepts = frozenset([b])

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
