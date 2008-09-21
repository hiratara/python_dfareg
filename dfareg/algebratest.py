#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-
import algebra
import unittest

class TestAlgebra(unittest.TestCase):
    def setUp(self):
        pass

    def test_power(self):
        a_set = set([1, 2, 3])
        power_set = algebra.power(a_set)
        # contained
        self.assert_(set([]) in power_set)
        self.assert_(set([1]) in power_set)
        self.assert_(set([2]) in power_set)
        self.assert_(set([3]) in power_set)
        self.assert_(set([1, 2]) in power_set)
        self.assert_(set([2, 3]) in power_set)
        self.assert_(set([3, 1]) in power_set)
        self.assert_(set([1, 2, 3]) in power_set)
        # not contained
        self.assert_(not 1 in power_set)
        self.assert_(not set([3, 4]) in power_set)
        # iteratable
        count = 0
        set_321 = set([3, 2, 1])
        has_set_321 = False
        for elem in power_set:
            count += 1
            if elem == set_321: has_set_321 = True
        self.assert_(count == 8)
        self.assert_(has_set_321)

    def tearDown(self):
        pass

if __name__ == '__main__':
    suite = unittest.makeSuite(TestAlgebra)
    unittest.TextTestRunner(verbosity=2).run(suite)
