#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-

VALUE      = 0
OPE_UNION  = 1
OPE_STAR   = 2
LPAREN     = 3
RPAREN     = 4
EOF        = 5

# トークン
class Talken(object):
    def __init__(self, value, kind):
        self.value = value
        self.kind  = kind

    def __str__(self):
        return ( u"%s(%d)" % (self.value, self.kind) ).encode("utf-8")

class Lexer(object):
    def __init__(self, string_):
        self.string_list = list(string_)

    def scan(self):
        if not self.string_list: return Talken(None, EOF)
        ch = self.string_list.pop(0)

        if ch == u'\\':
            return Talken(self.string_list.pop(0), VALUE)
        elif ch == u'|': 
            return Talken(ch, OPE_UNION)
        elif ch == u'(': 
            return Talken(ch, LPAREN)
        elif ch == u')': 
            return Talken(ch, RPAREN)
        elif ch == u'*': 
            return Talken(ch, OPE_STAR)
        else: 
            return Talken(ch, VALUE)

if __name__ == '__main__':
    lexer = Lexer(u"あ(い\|う|え*(かき|くけこ))*お")
    while True:
        talken = lexer.scan()
        if not talken: break
        print talken
