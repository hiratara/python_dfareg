# -*- coding: utf-8 -*-
"""
NFA definition
----------------------------------------
Author: hiratara <hira.tara@gmail.com>
"""
class NFARuntime(object):
    def __init__(self, NFA):
        self.NFA = NFA
        self.cur_states = self.NFA.epsilon_expand( 
            frozenset([ self.NFA.start ]) 
            )

    def do_transition(self, char):
        next_states = set()
        for state in self.cur_states:
            next_states |= self.NFA.transition(state, char)
        next_states = self.NFA.epsilon_expand(next_states)

        self.cur_states = next_states

    def is_accept_state(self):
        for state in self.cur_states:
            if state in self.NFA.accepts: return True
        return False

    def does_accept(self, input):
        for alphabet in input:
            self.do_transition(alphabet)
        return self.is_accept_state()


class NFABacktrackRuntime(object):
    def __init__(self, NFA):
        self.NFA = NFA
        self.cur_state = self.NFA.start
        self.left     = None
        self.branches = set()
        self.done     = set()

    def do_transition(self):
        # 文字列を読み終わったので、Falseを返す
        if self.left is None: 
            return False

        # とりうる遷移
        branches = set()

        # εを読む
        for state in self.NFA.transition(self.cur_state, u""):
            branches.add( (state, self.left) )

        if self.left:
            # まだ読める字があるので、次の1文字を読む
            char, self.left = self.left[0], self.left[1:]
            for state in self.NFA.transition(self.cur_state, char):
                branches.add( (state, self.left) )
        else:
            # 読める字がないので、読まずに終わる
            branches.add( (self.cur_state, None) );

        # すでに辿った道を除く
        branches = set( filter(lambda x: x not in self.done, branches) )

        if branches:
            # どの選択肢をとるか選ぶ
            self.cur_state, self.left = self._select(branches)
            # 残りはバックトラックできるように溜める
            self.branches |= branches
        else:
            # 遷移がもうない。状態をNoneにしておく
            self.cur_state, self.left = None, None

        return True

    def _select(self, branches):
        selected = branches.pop()
        self.done.add(selected)
        return selected

    def backtrack(self):
        if self.branches:
            self.cur_state, self.left = self._select(self.branches)
            return True
        else:
            return False

    def is_accept_state(self):
        return self.cur_state in self.NFA.accepts

    def does_accept(self, input):
        self.left = input
        while True:
            # 適当な経路でNFAを辿る
            while self.do_transition(): 
                pass
            if self.is_accept_state(): 
                # 受理状態についたので、受理。
                return True
            elif self.backtrack(): 
                # ダメだったのでバックトラックして別の経路へ
                continue
            else:
                # バックトラックできない。受理しない。
                return False


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
        # return NFABacktrackRuntime(self)

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
