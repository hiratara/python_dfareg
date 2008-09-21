#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-
import dfareg
import unittest

class TestDFA(unittest.TestCase):
    def setUp(self):
        def transition(state, char):
            if state == 0 and char == u"あ": return 1
            if state == 1 and char == u"あ": return 2
            if state == 1 and char == u"う": return 3
            return 4
        self.dfa = dfareg.DeterministicFiniteAutomaton(
            frozenset([0, 1, 2, 3, 4]),
            frozenset(u"あいうえお"),
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

if __name__ == '__main__':
    suite = unittest.makeSuite(TestDFA)
    unittest.TextTestRunner(verbosity=2).run(suite)
