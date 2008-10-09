# -*- coding: utf-8 -*-
from nfa2dfa import nfa2dfa
from parser  import Parser
from lexer   import Lexer

class Regexp(object):
    def __init__(self, regexp):
        self.regexp = regexp
        self.fa     = None
        self._compile()

    def _compile(self):
        lexer_        = Lexer(self.regexp)
        parser_       = Parser(lexer_)
        nfa           = parser_.expression()
        self.fa       = nfa2dfa(nfa)

    def matches(self, string):
        return self.fa.get_runtime().does_accept(string)

def compile(regexp):
    return Regexp(regexp)
