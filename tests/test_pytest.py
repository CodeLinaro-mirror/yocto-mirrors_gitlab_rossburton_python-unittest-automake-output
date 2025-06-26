# SPDX-FileCopyrightText: Copyright 2023 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: MIT

import subprocess
import unittest


class TestPytest(unittest.TestCase):
    def pytest(self, expected_output, expected_status, *args):
        self.maxDiff = 5000

        p = subprocess.run(
            ["pytest", "--automake"] + list(args),
            capture_output=True,
            text=True,
        )
        self.assertEqual(p.stdout, expected_output)
        self.assertEqual(p.returncode, expected_status)

    def test_just_pass(self):
        expected = """
        PASS: tests/pytest-testcase.py:test_passes
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
        self.pytest(expected, 0, "pytest-testcase.py", "-k", "test_passes")

    def test_all(self):
        expected = """
PASS: tests/pytest-testcase.py:test_passes

def test_fails():
>       assert False
E       assert False

pytest-testcase.py:14: AssertionError
FAIL: tests/pytest-testcase.py:test_fails
SKIP: tests/pytest-testcase.py:test_skip_decorator # SKIP using pytest.mark.skip
SKIP: tests/pytest-testcase.py:test_skip_function # SKIP using pytest.skip()
XFAIL: tests/pytest-testcase.py:test_xfail_decorator # XFAIL using pytest.mark.xfail
XFAIL: tests/pytest-testcase.py:test_xfail_function # XFAIL using pytest.xfail()
XPASS: tests/pytest-testcase.py:test_xfail_doesnt # XPASS using pytest.mark.xfail

@pytest.fixture
    def failing_fixture():
>       raise Exception("Raised exception")
E       Exception: Raised exception

pytest-testcase.py:42: Exception
ERROR: tests/pytest-testcase.py:test_error
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
        self.pytest(expected, 1, "pytest-testcase.py")

    def test_collect_fail(self):
        expected = """
pytest-fail-collect.py:8: in <module>
    raise Exception("This test failed to collect")
E   Exception: This test failed to collect
ERROR: tests/pytest-fail-collect.py:tests/pytest-fail-collect.py
============================================================================
Testsuite summary
# TOTAL: 1
# PASS: 0
# SKIP: 0
# XFAIL: 0
# FAIL: 0
# XPASS: 0
# ERROR: 1
"""
        self.pytest(expected, 2, "pytest-fail-collect.py")
