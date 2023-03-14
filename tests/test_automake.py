# SPDX-FileCopyrightText: Copyright 2023 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: MIT

import subprocess
import unittest


class TestAutomake(unittest.TestCase):
    def test_just_pass(self):
        expected = """
        PASS: tests.py:test_passes
============================================================================
Testsuite summary
# TOTAL: 1
# PASS: 1
# SKIP: 0
# XFAIL: 0
# FAIL: 0
# XPASS: 0
# ERROR: 0
""".lstrip()

        p = subprocess.run(
            ["pytest", "--automake", "tests.py", "-k", "test_passes"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(p.stdout, expected)
        self.assertEqual(p.returncode, 0)

    def test_all(self):
        expected = """
PASS: tests.py:test_passes

def test_fails():
>       assert False
E       assert False

tests.py:14: AssertionError
FAIL: tests.py:test_fails
SKIP: tests.py:test_skip_decorator # SKIP using pytest.mark.skip
SKIP: tests.py:test_skip_function # SKIP using pytest.skip()
XFAIL: tests.py:test_xfail_decorator # XFAIL using pytest.mark.xfail
XFAIL: tests.py:test_xfail_function # XFAIL reason: using pytest.xfail()
XPASS: tests.py:test_xfail_doesnt # XPASS using pytest.mark.xfail

@pytest.fixture
    def failing_fixture():
>       raise Exception("Raised exception")
E       Exception: Raised exception

tests.py:42: Exception
ERROR: tests.py:test_error
============================================================================
Testsuite summary
# TOTAL: 8
# PASS: 1
# SKIP: 2
# XFAIL: 2
# FAIL: 1
# XPASS: 1
# ERROR: 1
""".lstrip()

        p = subprocess.run(
            ["pytest", "--automake", "tests.py"], capture_output=True, text=True
        )
        self.assertEqual(p.stdout, expected)
        self.assertEqual(p.returncode, 1)
