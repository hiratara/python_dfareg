# -*- coding: utf-8 -*-
from nfa2dfa import nfa2dfa
from parser  import Parser
from lexer   import Lexer

class Regexp(object):
    def __init__(self, regexp, debug=False):
        self.regexp = regexp
        self.fa     = None
        self.debug  = debug
        self._compile()

    def _compile(self):
        lexer_        = Lexer(self.regexp)
        parser_       = Parser(lexer_)
        nfa           = parser_.expression()
        self.dfa       = nfa2dfa(nfa)
        if self.debug:
            from dump import dump_nfa, dump_dfa
            print "[NFA]"
            dump_nfa(nfa)
            print "[DFA]"
            dump_dfa(self.dfa)

    def matches(self, string):
        runtime = self.dfa.get_runtime(debug=self.debug)
        return runtime.does_accept(string)

def compile(regexp, debug=False):
    return Regexp(regexp, debug)
