# -*- coding: utf-8 -*-
"""
parse regular expressions
----------------------------------------
Author: hiratara <hira.tara@gmail.com>
"""
from lexer import Token
from nfabuilder import Character, Star, Concat, Union, Context

class Parser(object):
    """
    parse following language
    ----------------------------------------
    expression -> subexpr
    subexpr    -> subexpr '|' seq | seq
    (
        subexpr    -> seq _subexpr
        _subexpr   -> '|' seq _subexpr | ε
    )
    seq        -> subseq | ε
    subseq     -> subseq star | star
    (
        subseq     -> star _subseq
        _subseq    -> star _subseq | ε
    )
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
        self.match(Token.EOF)

        # 構文木を実行し、NFAを作る
        context  = Context()
        fragment = node.assemble(context)
        return fragment.build()

    def subexpr(self):
        # subexpr -> seq _subexpr
        node = self.seq()
        while True:
            if self.look.kind == Token.OPE_UNION:
                # _subexpr -> '|' seq _subexpr | ε
                self.match(Token.OPE_UNION)
                node2 = self.seq()
                node = Union(node, node2)
            else:
                # _subexpr -> ε
                break
        return node

    def seq(self):
        if self.look.kind == Token.LPAREN \
           or self.look.kind == Token.CHARACTER:
            # seq -> subseq
            return self.subseq()
        else:
            # seq -> ''
            return Character("")

    def subseq(self):
        # subseq -> star _subseq
        node = self.star()
        while True:
            if self.look.kind == Token.LPAREN \
               or self.look.kind == Token.CHARACTER:
                # _subseq -> star _subseq
                node2 = self.star()
                node  = Concat(node, node2)
                continue
            else:
                # _subseq -> ε
                break
        return node

    def star(self):
        # star -> factor '*' | factor
        node = self.factor()
        if self.look.kind == Token.OPE_STAR:
            self.match(Token.OPE_STAR)
            node = Star(node)
        return node

    def factor(self):
        if self.look.kind == Token.LPAREN:
            # factor -> '(' subexpr ')'
            self.match(Token.LPAREN)
            node = self.subexpr()
            self.match(Token.RPAREN)
            return node
        else:
            # factor -> CHARACTER
            node = Character(self.look.value)
            self.match(Token.CHARACTER);
            return node
