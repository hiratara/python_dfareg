# -*- coding: utf-8 -*-
from dfareg.nfa2dfa import nfa2dfa
from dfareg.parser  import Parser
from dfareg.lexer   import Lexer

def _all_items(*args):
    for iter_ in args:
        for item in iter_:
            yield item

def dump_dfa(dfa):
    def stat2str(stat_): return '-'.join(map(str, stat_))
    que  = set([ frozenset(dfa.start) ])
    done = set()
    while que:
        cur_stat = que.pop()
        if cur_stat == dfa.start  : print "[S]",
        if cur_stat in dfa.accepts: print "[A]",
        print stat2str(cur_stat),
        print
        done.add( frozenset(cur_stat) )
        for chr_ in _all_items([''], ( unichr(i) for i in xrange(0, 0x10000) )):
            next_stat = dfa.transition(cur_stat, chr_)
            if not next_stat:
                # 空集合状態に向かう遷移は略記
                continue
            print "\t'%s' -> %s" % (chr_, stat2str(next_stat))

            if next_stat not in done:
                que.add( frozenset(next_stat) )

def dump_nfa(nfa):
    def stat2str(stat_): return stat_
    que  = set([ nfa.start ])
    done = set()
    while que:
        cur_stat = que.pop()
        if cur_stat == nfa.start  : print "[S]",
        if cur_stat in nfa.accepts: print "[A]",
        print stat2str(cur_stat),
        print
        done.add( cur_stat )
        for chr_ in _all_items([''], ( unichr(i) for i in xrange(0, 0x10000) )):
            next_stats = nfa.transition(cur_stat, chr_)
            for next_stat in next_stats:
                print "\t'%s' -> %s" % (chr_, stat2str(next_stat))

                if next_stat not in done:
                    que.add( next_stat )

if __name__ == '__main__':
    #regexp = ur'(おはよう(ございます|)|こん(にち|ばん)(わ|は))*';
    regexp = ur'ab*c';

    lexer_  = Lexer(regexp)
    parser_ = Parser(lexer_)
    nfa     = parser_.expression()
    dump_nfa(nfa)
    dfa     = nfa2dfa(nfa)
    dump_dfa(dfa)

    #if dfa.get_runtime().does_accept(u"こんにちわおはようこんばんは"):
    #    print "match!"
