#! /usr/bin/env python3

# SPDX-FileCopyrightText: Copyright 2023 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: MIT

import pytest


def test_passes():
    assert True


def test_fails():
    assert False


@pytest.mark.skip(reason="using pytest.mark.skip")
def test_skip_decorator():
    assert False


def test_skip_function():
    pytest.skip("using pytest.skip()")


@pytest.mark.xfail(reason="using pytest.mark.xfail")
def test_xfail_decorator():
    assert False


def test_xfail_function():
    pytest.xfail("using pytest.xfail()")


@pytest.mark.xfail(reason="using pytest.mark.xfail")
def test_xfail_doesnt():
    assert True


@pytest.fixture
def failing_fixture():
    raise Exception("Raised exception")


def test_error(failing_fixture):
    assert failing_fixture == 2
