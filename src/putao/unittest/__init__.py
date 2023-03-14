# SPDX-FileCopyrightText: Copyright 2023 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: MIT

import unittest


class TestResult(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.successful = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.successful.append(test)
        print(f"PASS: {test.id()}")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        print(f"FAIL: {test.id()}")
        print(self.failures[-1][1].strip())
        print("=" * 76)

    def addError(self, test, err):
        super().addError(test, err)
        print(f"ERROR: {test.id()}")
        print(self.errors[-1][1].strip())
        print("=" * 76)

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        print(f"SKIP: {test.id()} # SKIP {reason}")

    def addExpectedFailure(self, test, err):
        super().addExpectedFailure(test, err)
        print(f"XFAIL: {test.id()}")
        print(self.expectedFailures[-1][1].strip())

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        print(f"XPASS: {test.id()}")


class TestRunner:
    def run(self, test):
        result = TestResult()
        test(result)

        print()
        print("=" * 76)
        print(f"Testsuite summary")
        print(f"# TOTAL: {result.testsRun}")
        print(f"# PASS: {len(result.successful)}")
        print(f"# SKIP: {len(result.skipped)}")
        print(f"# XFAIL: {len(result.expectedFailures)}")
        print(f"# FAIL: {len(result.failures)}")
        print(f"# XPASS: {len(result.unexpectedSuccesses)}")
        print(f"# ERROR: {len(result.errors)}")
        return result
