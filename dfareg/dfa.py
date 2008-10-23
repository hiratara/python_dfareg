# -*- coding: utf-8 -*-
"""
DFA definitions.
----------------------------------------
Author: hiratara <hira.tara@gmail.com>
"""
class DFARuntime(object):
    def __init__(self, DFA, debug=False):
        self.DFA   = DFA
        self.cur_state = self.DFA.start
        self.debug = debug

    def do_transition(self, char):
        self.cur_state = self.DFA.transition(self.cur_state, char)

    def is_accept_state(self):
        return self.cur_state in self.DFA.accepts

    def does_accept(self, input):
        if self.debug: print self.cur_state
        for alphabet in input:
            self.do_transition(alphabet)
            if self.debug: print "'%s' -> %s" % (alphabet, self.cur_state)
        return self.is_accept_state()


class DeterministicFiniteAutomaton(object):
    def __init__(self, 
                 transition , # 遷移関数
                 start      , # 開始状態
                 accepts    , # 受理状態の集合
                 ):
        self.transition = transition
        self.start      = start
        self.accepts    = accepts

    def get_runtime(self, debug=False):
        return DFARuntime(self, debug)
