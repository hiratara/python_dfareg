# -*- coding: utf-8 -*-
import nfa2dfa
from parser  import Parser
from lexer   import Lexer

class Regexp(object):
    def __init__(self, regexp, debug=False):
        self.regexp = regexp
        self.dfa    = None
        self._compile(debug)

    def _compile(self, debug=False):
        # コンパイル
        lexer_        = Lexer(self.regexp)
        parser_       = Parser(lexer_)
        nfa           = parser_.expression()
        # 部分集合構成法
        self.dfa      = nfa2dfa.nfa2dfa(nfa)
        if debug:
            from dump import dump_nfa, dump_dfa
            print "[NFA]"
            dump_nfa(nfa)
            print "[DFA]"
            dump_dfa(self.dfa)

    def matches(self, string, debug=False):
        runtime = self.dfa.get_runtime(debug)
        return runtime.does_accept(string)

def compile(regexp, debug=False):
    return Regexp(regexp, debug)
