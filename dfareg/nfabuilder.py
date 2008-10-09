# -*- coding: utf-8 -*-
import nfa
from copy import deepcopy

class NFAFragment(object):
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
