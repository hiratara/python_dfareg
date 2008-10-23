# -*- coding: utf-8 -*-
"""
NFA definition
----------------------------------------
Author: hiratara <hira.tara@gmail.com>
"""
class NondeterministicFiniteAutomaton(object):
    def __init__(self, 
                 transition , # a transition function
                 start      , # a start state
                 accepts    , # a set of accept states
                 ):
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

        return frozenset( done )
