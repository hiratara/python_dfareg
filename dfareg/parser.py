#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-
import lexer, inter

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

    def __init__(self, lexer):
        self.lexer   = lexer
        self.look    = None
        self.move()

    def match(self, tag):
        if self.look.kind != tag: raise "syntax error"
        self.move()

    def move(self):
        self.look = self.lexer.scan()

    def expr(self):
        node = self.seq()
        if self.look.kind == lexer.OPE_UNION:
            self.match(lexer.OPE_UNION)
            node2 = self.expr()
            node = inter.Union(node, node2)
        return node

    def seq(self):
        if self.look.kind == lexer.LPAREN or self.look.kind == lexer.VALUE:
            node1 = self.star()
            node2 = self.seq()
            node  = inter.Concat(node1, node2)
            return node
        # NOP (ε)
        return inter.Character("")

    def star(self):
        node = self.factor()
        if self.look.kind == lexer.OPE_STAR:
            self.match(lexer.OPE_STAR)
            node = inter.Star(node)
        return node

    def factor(self):
        if self.look.kind == lexer.LPAREN:
            self.match(lexer.LPAREN)
            node = self.expr()
            self.match(lexer.RPAREN)
            return node
        elif self.look.kind == lexer.VALUE:
            node = inter.Character(self.look.value)
            self.match(lexer.VALUE);
            return node
        else:
            raise "syntax error"


if __name__ == '__main__':
    from nfabuilder import NFABuilder
    lexer_ = lexer.Lexer(u"あ(い\|う|え*(かき|くけこ))*お")
    parser = Parser(lexer_, NFABuilder() )
    parser.expr()
