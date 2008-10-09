# -*- coding: utf-8 -*-
from lexer import Talken
from nfabuilder import Character, Star, Concat, Union, Context

class Parser(object):
    """
    構文解析器
    expression -> subexpr
    subexpr    -> seq '|' subexpr | seq
    seq        -> star seq | ε
    star       -> factor '*' | factor
    factor     -> '(' subexpr ')' | CHARACTER
    """

    def __init__(self, lexer):
        self.lexer   = lexer
        self.look    = None
        # 最初の文字を読む
        self.move()

    def match(self, tag):
        if self.look.kind != tag: 
            # 予期せぬトークンが来たら、エラー終了
            raise Exception("syntax error")
        self.move()

    def move(self):
        self.look = self.lexer.scan()

    def expression(self):
        # expression -> subexpr EOF
        node = self.subexpr()
        self.match(Talken.EOF)

        # 構文木を実行し、NFAを作る
        context  = Context()
        fragment = node.assemble(context)
        return fragment.build()

    def subexpr(self):
        # subexpr    -> seq '|' subexpr | seq
        node = self.seq()
        if self.look.kind == Talken.OPE_UNION:
            self.match(Talken.OPE_UNION)
            node2 = self.subexpr()
            node = Union(node, node2)
        return node

    def seq(self):
        if self.look.kind == Talken.LPAREN \
           or self.look.kind == Talken.CHARACTER:
            # seq -> star seq
            node1 = self.star()
            node2 = self.seq()
            node  = Concat(node1, node2)
            return node
        else:
            # seq -> ''
            return Character("")

    def star(self):
        # star -> factor '*' | factor
        node = self.factor()
        if self.look.kind == Talken.OPE_STAR:
            self.match(Talken.OPE_STAR)
            node = Star(node)
        return node

    def factor(self):
        if self.look.kind == Talken.LPAREN:
            # factor -> '(' subexpr ')'
            self.match(Talken.LPAREN)
            node = self.subexpr()
            self.match(Talken.RPAREN)
            return node
        else:
            # factor -> CHARACTER
            node = Character(self.look.value)
            self.match(Talken.CHARACTER);
            return node
