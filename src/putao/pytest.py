# SPDX-FileCopyrightText: Copyright 2023 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: MIT

import pytest

from _pytest.terminal import TerminalReporter

ENABLED = False

def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting", "reporting", after="general")
    group.addoption(
        "--automake",
        default=False,
        action="store_true",
        help="Write automake-style output",
    )


@pytest.mark.trylast
def pytest_configure(config):
    """Set all the options before the test run."""
    # The help printing uses the terminalreporter,
    # which is unregistered by the streaming mode.
    global ENABLED

    if config.option.help:
        return

    ENABLED = config.option.automake

    if ENABLED:
        standard_reporter = config.pluginmanager.getplugin("terminalreporter")
        new_reporter = PutaoTerminalReporter(standard_reporter.config)
        config.pluginmanager.unregister(standard_reporter)
        config.pluginmanager.register(new_reporter, "terminalreporter")


class PutaoTerminalReporter(TerminalReporter):

    def __init__(self, config, file=None) -> None:
        TerminalReporter.__init__(self, config, file)
        self.counts = {
            "PASS": 0,
            "SKIP": 0,
            "XFAIL": 0,
            "FAIL": 0,
            "XPASS": 0,
            "ERROR": 0,
        }

    def handle_report(self, report):
        description = str(report.location[0]) + ":" + str(report.location[2])

        if hasattr(report, "wasxfail"):
            # Test was expected to fail and did
            if report.skipped:
                status = "XFAIL"
            # Test was expected to fail but passed
            elif report.passed:
                status = "XPASS"
            else:
                status = "ARGH"
            print(f"{status}: {description} # {status} {report.wasxfail}")
        elif report.passed:
            status = "PASS"
            print(f"{status}: {description}")
        elif report.failed:
            if report.when in ("collect", "setup"):
                status = "ERROR"
            else:
                status = "FAIL"
            print()
            print(report.longreprtext)
            print(f"{status}: {description}")
        elif report.skipped:
            status = "SKIP"
            # there may not be a custom skipping message
            if ":" in report.longrepr[2]:
                reason = report.longrepr[2].split(":", 1)[1].strip()
            else:
                reason = report.longrepr[2].strip()
            print(f"{status}: {description} # {status} {reason}")
        else:
            status = "ARGH"
            print(f"{status}: {report=}")

        self.counts[status] += 1


    def pytest_collectreport(self, report):
        TerminalReporter.pytest_collectreport(self, report)

        if not report.passed:
            self.handle_report(report)


    def pytest_runtest_logreport(self, report):
        if not ENABLED:
            return

        to_display = (
            (report.when == "setup" and report.outcome == "skipped")
            or (report.when == "setup" and report.outcome == "failed")
            or report.when == "call"
        )
        if not to_display:
            return

        self.handle_report(report)

    def pytest_sessionstart(self, session) -> None:
        self._session = session

    def pytest_runtest_logstart(self, nodeid, location) -> None:
        pass

    def pytest_runtest_logfinish(self, nodeid: str) -> None:
        pass

    def summary_failures(self) -> None:
        pass

    def summary_errors(self) -> None:
        pass

    def short_test_summary(self) -> None:
        pass

    def summary_stats(self) -> None:
        print("=" * 76)
        print("Testsuite summary")
        print(f"# TOTAL: {sum(self.counts.values())}")
        for k, v in self.counts.items():
            print(f"# {k}: {v}")
