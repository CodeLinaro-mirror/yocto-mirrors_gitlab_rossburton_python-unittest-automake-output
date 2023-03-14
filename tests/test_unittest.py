# SPDX-FileCopyrightText: Copyright 2023 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: MIT

import os
import subprocess
import unittest


class TestUnittest(unittest.TestCase):
    def test_all(self):
        test_script = os.path.realpath(
            os.path.join(os.path.dirname(__file__), "unittest-testcase.py")
        )

        expected = f"""
ERROR: unittest-testcase.Tests.test_errors
Traceback (most recent call last):
  File "{test_script}", line 17, in test_errors
    raise Exception("This was deliberate")
Exception: This was deliberate
============================================================================
FAIL: unittest-testcase.Tests.test_fails
Traceback (most recent call last):
  File "{test_script}", line 14, in test_fails
    self.assertTrue(False)
AssertionError: False is not true
============================================================================
PASS: unittest-testcase.Tests.test_passes
SKIP: unittest-testcase.Tests.test_skip_decorator # SKIP Skipped with @unittest.skip
SKIP: unittest-testcase.Tests.test_skip_function # SKIP Skipped with self.skipTest
XFAIL: unittest-testcase.Tests.test_xfail
Traceback (most recent call last):
  File "{test_script}", line 29, in test_xfail
    self.assertTrue(False)
AssertionError: False is not true
XPASS: unittest-testcase.Tests.test_xpass

============================================================================
Testsuite summary
# TOTAL: 7
# PASS: 1
# SKIP: 2
# XFAIL: 1
# FAIL: 1
# XPASS: 1
# ERROR: 1
""".lstrip()

        p = subprocess.run(
            ["python3", "-mputao.unittest", test_script], capture_output=True, text=True
        )
        self.assertEqual(p.stdout, expected)
        self.assertEqual(p.returncode, 1)
