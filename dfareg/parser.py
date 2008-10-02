#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-
import lexer

class Parser(object):
    """
    NFAを組み立てる

    E = E union  T | T
    T = T S | S | ε
    S = F star | F
    F = lparen E rparen | value

    ↓

    expr   -> seq '|' expr | seq
    seq    -> star seq | ε
    star   -> factor '*' | factor
    factor -> '(' expr ')' | VALUE
    """

    def __init__(self, lexer, builder):
        self.lexer   = lexer
        self.builder = builder
        self.look    = None
        self.move()

    def match(self, tag):
        if self.look.kind != tag: raise "syntax error"
        self.move()

    def move(self):
        self.look = self.lexer.scan()

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

    def expr(self):
        node = self.seq()
        if self.look.kind == lexer.OPE_UNION:
            self.match(lexer.OPE_UNION)
            node2 = self.expr()
            node = self._assemble_union(node, node2)
        return node

    def seq(self):
        if self.look.kind == lexer.LPAREN or self.look.kind == lexer.VALUE:
            node1 = self.star()
            node2 = self.seq()
            node  = self._assemble_concat(node1, node2)
            return node
        # NOP (ε)
        return self._assemble_value("")

    def star(self):
        node = self.factor()
        if self.look.kind == lexer.OPE_STAR:
            self.match(lexer.OPE_STAR)
            node = self._assemble_star(node)
        return node

    def factor(self):
        if self.look.kind == lexer.LPAREN:
            self.match(lexer.LPAREN)
            node = self.expr()
            self.match(lexer.RPAREN)
            return node
        elif self.look.kind == lexer.VALUE:
            node = self._assemble_value(self.look.value)
            self.match(lexer.VALUE);
            return node
        else:
            raise "syntax error"


if __name__ == '__main__':
    from nfabuilder import NFABuilder
    lexer_ = lexer.Lexer(u"あ(い\|う|え*(かき|くけこ))*お")
    parser = Parser(lexer_, NFABuilder() )
    parser.expr()
