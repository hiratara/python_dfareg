#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-
import lexer, nfabuilder

class Parser(object):
    """
    NFAを組み立てる
    expression -> subexpr
    subexpr    -> seq '|' subexpr | seq
    seq        -> star seq | ε
    star       -> factor '*' | factor
    factor     -> '(' subexpr ')' | VALUE
    """

    def __init__(self, lexer):
        self.lexer   = lexer
        self.look    = None
        self.move()

    def match(self, tag):
        if self.look.kind != tag: raise "syntax error"
        self.move()

    def move(self):
        self.look = self.lexer.scan()

    def expression(self):
        node     = self.subexpr()
        context  = nfabuilder.Context()
        fragment = node.assemble(context)
        return fragment.build()

    def subexpr(self):
        node = self.seq()
        if self.look.kind == lexer.OPE_UNION:
            self.match(lexer.OPE_UNION)
            node2 = self.subexpr()
            node = nfabuilder.Union(node, node2)
        return node

    def seq(self):
        if self.look.kind == lexer.LPAREN or self.look.kind == lexer.VALUE:
            node1 = self.star()
            node2 = self.seq()
            node  = nfabuilder.Concat(node1, node2)
            return node
        # NOP (ε)
        return nfabuilder.Character("")

    def star(self):
        node = self.factor()
        if self.look.kind == lexer.OPE_STAR:
            self.match(lexer.OPE_STAR)
            node = nfabuilder.Star(node)
        return node

    def factor(self):
        if self.look.kind == lexer.LPAREN:
            self.match(lexer.LPAREN)
            node = self.subexpr()
            self.match(lexer.RPAREN)
            return node
        elif self.look.kind == lexer.VALUE:
            node = nfabuilder.Character(self.look.value)
            self.match(lexer.VALUE);
            return node
        else:
            raise "syntax error"


if __name__ == '__main__':
    from nfabuilder import NFABuilder
    lexer_ = lexer.Lexer(u"あ(い\|う|え*(かき|くけこ))*お")
    parser = Parser(lexer_, NFABuilder() )
    parser.expression()
