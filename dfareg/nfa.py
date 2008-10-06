#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-

class NondeterministicFiniteAutomaton(object):
    """
    An nondeterministic finite automaton implementation.
    It's just for fun. So, you shouldn't use this in your products.
    """
    def __init__(self, 
                 transition , # a transition function
                 start      , # a start state
                 accepts    , # a set of accept states
                 ):
        """
        Instanciate new deterministic finite automaton 
        from 5-tuple.
        """
        self.transition = transition
        self.start      = start
        self.accepts    = accepts

    def get_runtime(self):
        return NFARuntime(self)

    def epsilon_expand(self, set_):
        # 空文字を辿るべき状態を集めたキュー
        que = set( set_ )
        # 辿り終わった状態
        done = set()
        while que:
            # キューから取り出す
            stat = que.pop()
            # 空文字によって辿れる遷移を辿る
            nexts = self.transition(stat, "")
            # この状態は辿り終わったので、保存
            done.add(stat)
            # 辿って出て来た状態を、さらに空文字で辿るのに、キューに居れる
            for next_stat in nexts:
                # 辿り終わってない要素だけ
                if not next_stat in done: que.add(next_stat)

        return done
