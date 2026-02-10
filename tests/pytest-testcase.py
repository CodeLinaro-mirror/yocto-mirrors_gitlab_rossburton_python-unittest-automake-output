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


def test_skip_function_no_message():
    pytest.skip()


# https://gitlab.com/rossburton/python-unittest-automake-output/-/issues/10
def test_deep_compare():
    d1 = {"foo": 42, "bar": 69}
    d2 = {"foo": 42, "bar": 96}
    assert d1.items() == d2.items()
