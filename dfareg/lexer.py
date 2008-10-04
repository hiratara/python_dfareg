#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-



class Talken(object):
    # トークンの種類
    CHARACTER  = 0
    OPE_UNION  = 1
    OPE_STAR   = 2
    LPAREN     = 3
    RPAREN     = 4
    EOF        = 5
    def __init__(self, value, kind):
        # このトークンが持つ値
        self.value = value
        # このトークンの種類
        self.kind  = kind

    def __str__(self):
        return ( u"%s(%d)" % (self.value, self.kind) ).encode("utf-8")


class Lexer(object):
    def __init__(self, string_):
        # 文字をリスト化して保持
        self.string_list = list(string_)

    def scan(self):
        if not self.string_list: 
            # 文字がなくなったらEOFトークンを返す
            return Talken(None, Talken.EOF)

        ch = self.string_list.pop(0)

        if ch == u'\\':
            # エスケープ文字の処理。次の文字を文字トークンとして返す
            return Talken(self.string_list.pop(0), Talken.CHARACTER)
        elif ch == u'|': 
            return Talken(ch, Talken.OPE_UNION)
        elif ch == u'(': 
            return Talken(ch, Talken.LPAREN)
        elif ch == u')': 
            return Talken(ch, Talken.RPAREN)
        elif ch == u'*': 
            return Talken(ch, Talken.OPE_STAR)
        else: 
            # 通常の文字
            return Talken(ch, Talken.CHARACTER)

if __name__ == '__main__':
    lexer = Lexer(u"あ(い\|う|え*(かき|くけこ))*お")
    while True:
        talken = lexer.scan()
        if not talken: break
        print talken
