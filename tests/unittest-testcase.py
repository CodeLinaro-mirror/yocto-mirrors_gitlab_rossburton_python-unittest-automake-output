#! /usr/bin/env python3

# SPDX-FileCopyrightText: Copyright 2023 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: MIT

import unittest


class Tests(unittest.TestCase):
    def test_passes(self):
        self.assertTrue(True)

    def test_fails(self):
        self.assertTrue(False)

    def test_errors(self):
        raise Exception("This was deliberate")

    @unittest.skip("Skipped with @unittest.skip")
    def test_skip_decorator(self):
        raise Exception("Should not reach this")

    def test_skip_function(self):
        self.skipTest("Skipped with self.skipTest")
        raise Exception("Should not reach this")

    @unittest.expectedFailure
    def test_xfail(self):
        self.assertTrue(False)

    @unittest.expectedFailure
    def test_xpass(self):
        self.assertTrue(True)
