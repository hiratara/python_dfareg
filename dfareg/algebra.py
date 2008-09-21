#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-

class AbstractSet(object):
    def issubset(self, set_):
        for elem in self:
            if elem not in set_: return False
        return True


# ベキ集合
class PowerSet(AbstractSet):
    def __init__(self, a_set):
        try:
            hash(a_set)
        except TypeError:
            # use frozenset to be able to get hash
            a_set = frozenset(a_set)
        self.set = a_set

    def __contains__(self, a_set):
        try:
            return self.set.issuperset(a_set)
        except TypeError, te:
            # a_set wasn't a set.
            return False

    def __iter__(self):
        # TODO: yeild使って作った方がいい
        def _power(a_set):
            try:
                iter(a_set).next()
            except StopIteration:
                # no more element. return phai set.
                phai = frozenset()
                return set([ phai ])

            ret = set()
            # car + cdr
            cdr_set = set(a_set)
            car_elem = cdr_set.pop()
            # recursive
            power_sets = _power(cdr_set)
            # make power set
            for set1 in power_sets:
                set2 = set1.union( set([ car_elem ]) )
                ret.add(set1)
                ret.add(set2)
            return ret
        return iter(_power(self.set))

def power(a_set):
    """
    >>> from dfareg import algebra
    >>> ps = algebra.power([1,2,3])
    >>> set([]) in ps
    True
    >>> set([1,2,3,4]) in ps
    False
    >>> set([1,2,3]) in ps
    True
    >>> list(ps)
    [frozenset([2]), frozenset([3]), frozenset([1, 2]), frozenset([]), frozenset([2, 3]), frozenset([1]), frozenset([1, 3]), frozenset([1, 2, 3])]
    """
    return PowerSet(a_set)


class SubsetsIncludingElem(AbstractSet):
    """
    the set of subsets of "super_" including an element of "sub".

    >>> from dfareg import algebra
    >>> s = algebra.subsets_including_elem(set([1,2,3]), set([1,3]))
    >>> for i in s: 
    ...     print i
    ... 
    frozenset([3])
    frozenset([1, 2])
    frozenset([2, 3])
    frozenset([1])
    frozenset([1, 3])
    frozenset([1, 2, 3])
    >>> set([1,2]) in s
    True
    >>> set([2]) in s
    False
    """
    def __init__(self, sub):
        self.sub   = sub
    def __contains__(self, a_set):
        try:
            if a_set & self.sub:
                return True
        except TypeError, te:
            # a_set wasn't a set.
            return False
#     def __iter__(self):
#         return iter(
#             set_
#             for set_ in power(self.super_)
#             if set_ in self
#             )
    def issubset(self, set_):
        if(issubclass(type(set_), PowerSet)):
            # XXX 包含関係を真面目に調べると、元集合が大きい時に処理が戻って来ない
            # 速度稼ぎのための処理。入力がベキ集合であれば、
            # 元の集合同士が包含関係にあればOK
            if(self.super_.issubset(set_.set)): return True
        return super(SubsetsIncludingElem).issubset(set_)


def subsets_including_elem(sub):
    """
    >>> from dfareg import algebra
    >>> sie = algebra.subsets_including_elem(set([1,2,3,4]), set([2,3]))
    >>> set([1,2]) in sie
    True
    >>> set([1,4]) in sie
    False
    >>> set([3]) in sie
    True
    >>> set([5]) in sie
    False
    """
    return SubsetsIncludingElem(sub)


class UnicodeSet(AbstractSet):
    """
    ユニコード文字の集合
    """
    def __contains__(self, val):
        # ordできるものなら文字と見なす
        try:
            ord(val)
            return True
        except:
            return False

unicodeset = UnicodeSet()


def expand_set(set_, func):
    """
    expand set_ with func in super_.
    func: set_ -> power(super_)

    >>> from dfareg import algebra
    >>> algebra.expand_set(set([2]), lambda x: set([x+1]), set([1,2,3]))
    set([2, 3])
    >>> algebra.expand_set(set([2]), lambda x: set([x-1]), set([1,2,3]))
    set([1, 2])
    >>> algebra.expand_set(set([4]), lambda x: set([x-1, x*2]), set([1,2,3,4,5,6,7,8,9,10]))
    set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    >>> algebra.expand_set(set([1]), lambda x: set([x*3, x*2]), set([1,2,3,4,5,6,7,8,9,10]))
    set([1, 2, 3, 4, 6, 8, 9])
    """
    que = set( set_ )
    returns = set()
    while que:
        elem = que.pop()
        if elem in returns:
            continue
        returns.add(elem)
        nexts = func(elem)
        que |= nexts

    return returns
