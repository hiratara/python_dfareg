#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-
#あ(い\|う|え)*お

from nfabuilder import NFABuilder
import algebra

VALUE      = 0
OPE_UNION  = 1
OPE_CONCAT = 2
OPE_STAR   = 3
LPAREN     = 4
RPAREN     = 5

# トークン
class Talken(object):
    def __init__(self, value, kind):
        self.value = value
        self.kind  = kind

    def __repr__(self):
        return ( u"%s(%d)" % (self.value, self.kind) ).encode("utf-8")

# トークンへパースする
def parse(string):
    talken = []

    was_escape = False
    was_factor = False
    for ch in string:
        if ch == u'\\':
            was_escape = True
        elif was_escape:
            if was_factor:
                talken.append(Talken('.', OPE_CONCAT))
            talken.append(Talken(ch, VALUE))
            was_escape = False
            was_factor = True
        elif ch == u'|': 
            talken.append(Talken(ch, OPE_UNION))
            was_factor = False
        elif ch == u'(': 
            if was_factor:
                talken.append(Talken('.', OPE_CONCAT))
            talken.append(Talken(ch, LPAREN))
            was_factor = False
        elif ch == u')': 
            talken.append(Talken(ch, RPAREN))
            was_factor = True
        elif ch == u'*': 
            talken.append(Talken(ch, OPE_STAR))
            was_factor = True
        else: 
            if was_factor:
                talken.append(Talken('.', OPE_CONCAT))
            talken.append(Talken(ch, VALUE))
            was_factor = True

    return talken


class AssembleNFA(object):
    """
    NFAを組み立てる

    E = E union  T | T
    T = T concat S | S
    S = S * | S
    F = ( E ) | 文字
    """

    def __init__(self, talkens):
        self.stack   = list(talkens)
        self.builder = NFABuilder()

    def _assemble_value(self, value):
        frag = self.builder.new_fragment()
        a = frag.new_state()
        b = frag.new_state()
        frag.connect(a, value, b)
        frag.accepts.add(b)
        frag.start = a
        return frag

    def _assemble_union(self, frag1, frag2):
        frag = self.builder.merge_fragment(frag1, frag2)
        a = frag.new_state()
        frag.connect(a, "", frag1.start)
        frag.connect(a, "", frag2.start)
        frag.start = a

        return frag


    def _assemble_concat(self, frag1, frag2):
        frag = self.builder.merge_fragment(frag1, frag2)

        for state in frag1.accepts:
            frag.connect(state, "", frag2.start)
            frag.accepts.remove(state)

        frag.start = frag1.start

        return frag


    def _assemble_star(self, frag):
        for state in frag.accepts:
            frag.connect(state, "", frag.start)

        a = frag.new_state()
        frag.accepts.add(a)
        frag.connect(a, "", frag.start)

        frag.start = a

        return frag


    def _expr(self):
        c = self._term()
        while len(self.stack) > 0 and self.stack[0].kind == OPE_UNION:
            self.stack.pop(0)
            c = self._assemble_union(c, self._term())
        return c

    def _term(self):
        c = self._star()
        while len(self.stack) > 0 and self.stack[0].kind == OPE_CONCAT:
            self.stack.pop(0)
            c = self._assemble_concat(c, self._star())
        return c

    def _star(self):
        c = self._fact()
        while len(self.stack) > 0 and self.stack[0].kind == OPE_STAR:
            self.stack.pop(0)
            c = self._assemble_star(c)
        return c

    def _fact(self):
        t = self.stack.pop(0)
        if t.kind == VALUE:
            return self._assemble_value(t.value)
        if t.kind == LPAREN:
            c = self._expr()
            if not self.stack.pop(0).kind == RPAREN:
                raise "invalid paren"
            return c
        raise "invalid: %s" % t

    def assemble(self):
        root_fragment = self._expr()
        nfa = self.builder.build(root_fragment)

        return nfa

def compile_to_nfa(regexp):
    talkens = parse(regexp)
    assembler = AssembleNFA(talkens)
    return assembler.assemble()


if __name__ == '__main__':
    regexp = u"あ(い\|う|え*(かき|くけこ))*お"
    # 14個
    regexp = u"n*n*n*n*n*n*n*n*n*n*n*n*n*n*n*nnnnnnnnnnnnnnn"
    string = u"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnn"
    nfastate = compile_to_nfa(regexp)
#     for s in nfastate.all_states():
#         print s
    # 動かしてみたい
    automaton = NoneterministicFiniteAutomaton(nfastate)
    print automaton.doesAccept(string)
    print "###################"
    import re
    print re.match(u"^%s$" % regexp, string)



#     # OK
#     print automaton.doesAccept(u"あお")
#     print automaton.doesAccept(u"あい|うお")
#     print automaton.doesAccept(u"あえええくけこお")
#     print automaton.doesAccept(u"あえええええくけこお")
#     # NG
#     print automaton.doesAccept(u"ええええええ")
#     print automaton.doesAccept(u"ああお")
#     print automaton.doesAccept(u"あおお")
#     print automaton.doesAccept(u"あえええ")
