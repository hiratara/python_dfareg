#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-
import nfabuilder

_builder = nfabuilder.NFABuilder()

class Union(object):
    def __init__(self, operand1, operand2):
        self.operand1 = operand1
        self.operand2 = operand2
    def assemble(self):
        frag1 = self.operand1.assemble()
        frag2 = self.operand2.assemble()
        frag = _builder.merge_fragment(frag1, frag2)

        a = frag.new_state()
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
        frag = _builder.merge_fragment(frag1, frag2)

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

        a = frag.new_state()
        frag.accepts.add(a)
        frag.connect(a, "", frag.start)

        frag.start = a

        return frag

class Character(object):
    def __init__(self, char):
        self.char = char

    def assemble(self):
        frag = _builder.new_fragment()
        a = frag.new_state()
        b = frag.new_state()
        frag.connect(a, self.char, b)
        frag.accepts.add(b)
        frag.start = a
        return frag
