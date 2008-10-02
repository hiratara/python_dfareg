#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-
from dfa import *
from nfa2dfa import nfa2dfa
from parser     import Parser
from nfabuilder import NFABuilder
from lexer      import Lexer

def strict_match_nfa(regexp, string):
    nfa = lexer.compile_to_nfa(regexp)
    return nfa.get_runtime().does_accept(string)

def strict_match_dfa(regexp, string):
    nfa = lexer.compile_to_nfa(regexp)
    dfa = nfa2dfa(nfa)
    return dfa.get_runtime().does_accept(string)

strict_match = strict_match_dfa

def print_nfa(regexp):
    nfa = lexer.compile_to_nfa(regexp)
    print "[START]"
    print nfa.start
    print "[STATES]"
    for s in nfa.states:
        print s
    print "[ACCEPTS]"
    for s in nfa.accepts:
        print s
    print "[TRANSITION]"
    print "not printable"


class Regexp(object):
    def __init__(self, regexp):
        self.regexp = regexp
        self.fa     = None
        self._compile()

    def _compile(self):
        lexer_        = Lexer(self.regexp)
        parser_       = Parser(lexer_)
        root_node     = parser_.expr()
        root_fragment = root_node.assemble()
        # XXX ↓NFABuilder() を直す必要あり。inter.pyと同化？
        nfa           = NFABuilder().build(root_fragment)
        self.fa       = nfa2dfa(nfa)

    def matches(self, string):
        return self.fa.get_runtime().does_accept(string)

def compile(regexp):
    return Regexp(regexp)


#     for k, v in nfafrag.map.iteritems():
#         print k, v

# cd /Users/tarara/Documents/技術関係/開発合宿/20080524/python

# >>> import dfareg
# >>> dfareg.strict_match("(p(erl|ython|hp)|ruby)", "python")
# True

# >>> dfareg.print_nfa("A*B")

# >>> import re
# >>> re.match("^x*x*x*x*x*x*x*x*x*x*x*x*x*x*xxxxxxxxxxxxxx$", "xxxxxxxxxxxxxx")
# <_sre.SRE_Match object at 0x2581a8>
# >>> dfareg.strict_match("x*x*x*x*x*x*x*x*x*x*x*x*x*x*xxxxxxxxxxxxxx", "xxxxxxxxxxxxxx")
# True
