#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-
import dfareg
from dfareg.dfa import DeterministicFiniteAutomaton
import unittest

class TestDFA(unittest.TestCase):
    def setUp(self):
        def transition(state, char):
            if state == 0 and char == u"あ": return 1
            if state == 1 and char == u"あ": return 2
            if state == 1 and char == u"う": return 3
            return 4
        self.dfa = DeterministicFiniteAutomaton(
            transition,
            0,
            frozenset([3])
            )

    def testok(self):
        self.assert_(self.dfa.get_runtime().does_accept(u"あう"))

    def testng(self):
        self.assert_(not self.dfa.get_runtime().does_accept(u"ああ"))

    def testng2(self):
        self.assert_(not self.dfa.get_runtime().does_accept(u"あうあ"))

    def testng3(self):
        self.assert_(not self.dfa.get_runtime().does_accept(u"おあう"))

    def tearDown(self):
        pass

class TestRegexp(unittest.TestCase):
    def setUp(self): pass
    def tearDown(self): pass
    def test_normal(self):
        reg = dfareg.compile(r"(p(erl|ython|hp)|ruby)")
        self.assert_(reg.matches("python"))
        self.assert_(reg.matches("ruby"))
        self.assert_(not reg.matches("VB"))
    def test_japanese1(self):
        reg = dfareg.compile(ur"山田(太|一|次|三)郎")
        self.assert_(reg.matches(u"山田太郎"))
        self.assert_(reg.matches(u"山田三郎"))
        self.assert_(not reg.matches("山田郎"))
    def test_japanese2(self):
        reg = dfareg.compile(ur"ｗｗ*|\(笑\)")
        self.assert_(reg.matches(u"(笑)"))
        self.assert_(reg.matches(u"ｗｗｗ"))
        self.assert_(not reg.matches(u"笑"))
    def test_escape(self):
        reg = dfareg.compile(r"a\c")
        self.assert_(reg.matches(r"ac"))
        self.assert_(not reg.matches(r"a\c"))
        reg = dfareg.compile(r"a\\c")
        self.assert_(reg.matches(r"a\c"))
        self.assert_(not reg.matches(r"ac"))
    def test_empty_select(self):
        reg = dfareg.compile(r"a(b|)")
        self.assert_(reg.matches(r"ab"))
        self.assert_(reg.matches(r"a"))
        self.assert_(not reg.matches(r"abb"))
    def test_syntax_error(self):
        import sys
        for regexp in ['ab(cd', 'e(*)f', ')h', 'i|*', '*']:
            err = None
            try:
                reg = dfareg.compile(regexp)
            except Exception, e:
                err = e
            self.assert_(str(err) == 'syntax error')

if __name__ == '__main__':
    suite = unittest.makeSuite(TestDFA)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.makeSuite(TestRegexp)
    unittest.TextTestRunner(verbosity=2).run(suite)
