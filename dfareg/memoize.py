# -*- coding: utf-8 -*-
def memoize(func):
    cache = dict()
    def memoized_func(*args):
        if args not in cache:
            res = func(*args)
            cache[args] = res
        return cache[args]

    return memoized_func
