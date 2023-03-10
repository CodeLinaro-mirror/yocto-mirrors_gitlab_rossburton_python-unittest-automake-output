# SPDX-FileCopyrightText: Copyright 2023 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: MIT

import pytest

ENABLED = False
counts = {
    "PASS": 0,
    "SKIP": 0,
    "XFAIL": 0,
    "FAIL": 0,
    "XPASS": 0,
    "ERROR": 0,
}


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
    if config.option.help:
        return

    global ENABLED
    ENABLED = config.option.automake

    if ENABLED:
        reporter = config.pluginmanager.getplugin("terminalreporter")
        if reporter:
            config.pluginmanager.unregister(reporter)


def pytest_runtest_logreport(report):
    if not ENABLED:
        return

    to_display = (
        (report.when == "setup" and report.outcome == "skipped")
        or (report.when == "setup" and report.outcome == "failed")
        or report.when == "call"
    )
    if not to_display:
        return

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
        status = "FAIL"
        print()
        print(report.longreprtext)
        print(f"{status}: {description}")
    elif report.skipped:
        status = "SKIP"
        reason = report.longrepr[2].split(":", 1)[1].strip()
        print(f"{status}: {description} # {status} {reason}")
    else:
        status = "ARGH"
        print(f"{status}: {report=}")

    counts[status] += 1


def pytest_unconfigure(config):
    if not ENABLED:
        return

    print("=" * 76)
    print(f"Testsuite summary for {config.rootdir}")
    print(f"TOTAL: {sum(counts.values())}")
    for k, v in counts.items():
        print(f"{k}: {v}")
