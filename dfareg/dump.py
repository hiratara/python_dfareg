# -*- coding: utf-8 -*-
"""
dump NFA and DFA.
----------------------------------------
Author: hiratara <hira.tara@gmail.com>
"""
from dfareg.nfa2dfa import nfa2dfa
from dfareg.parser  import Parser
from dfareg.lexer   import Lexer

def _all_items(*args):
    for iter_ in args:
        for item in iter_:
            yield item

class AbstructDumper(object):
    def __init__(self, fa):
        self.fa = fa
        self.que  = set([ fa.start ])
        self.done = set()
        self.cur_stat = None

    def dump(self):
        while self.que:
            self.cur_stat = self.que.pop()
            self.print_stat( self.cur_stat )
            self.done.add( self.cur_stat )
            for chr_ in self.alphabet():
                self.do_transition(chr_)

    def print_stat(self, stat):
        if stat == self.fa.start  : print u"開始",
        if stat in self.fa.accepts: print u"受理",
        print u"状態", self.stat2str(stat),
        print

    def transited(self, chr_, next_stat):
        print u"\t'%s' -> %s" % (chr_, self.stat2str(next_stat))
        if next_stat not in self.done: self.que.add( next_stat )

    def stat2str(self, stat): raise NotImplementedError
    def alphabet(self, stat): raise NotImplementedError
    def do_transition(self, chr_): raise NotImplementedError


class DFADumper(AbstructDumper):
    def stat2str(self, stat):
        return '-'.join(map(str, stat))

    def alphabet(self):
        return ( unichr(i) for i in xrange(0, 0x10000) )

    def do_transition(self, chr_):
        next_stat = self.fa.transition(self.cur_stat, chr_)
        if not next_stat:
            # 空集合状態に向かう遷移は略記
            return
        self.transited(chr_, next_stat)


class NFADumper(AbstructDumper):
    def stat2str(self, stat):
        return stat

    def alphabet(self):
        yield ''
        for i in xrange(0, 0x10000): yield unichr(i) 

    def do_transition(self, chr_):
        nexts = self.fa.transition(self.cur_stat, chr_)
        for next_stat in nexts:
            self.transited(chr_, next_stat)


def dump_dfa(dfa):
    DFADumper(dfa).dump()

def dump_nfa(nfa):
    NFADumper(nfa).dump()
