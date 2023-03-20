# Python Unittest Automake Output

Also known as _putao_, is a package designed to make Python unit test output look like `automake`, for the purpose of integrating into systems which expect `automake`-style output (such as `ptest` in OpenEmbedded).

`putao` is MIT-licensed (see [`LICENSE`](LICENSE)) and copyright 2023 Arm Limited.

## Python `unittest`

The module `putao.unittest` uses the `unittest.main()` entrypoint with custom `TestResult` and `TestRunner` classes for the desired output.

```
~/Code/picobuild/tests $ python3 -mputao.unittest
PASS: test_build.BuildAPITests.test_flit_core_sdist
PASS: test_build.BuildAPITests.test_flit_core_wheel
PASS: test_build.BuildAPITests.test_legacy
[ ... ]
Testsuite summary
# TOTAL: 9
# PASS: 9
# SKIP: 0
# XFAIL: 0
# FAIL: 0
# XPASS: 0
# ERROR: 0
```

## `pytest`

A `pytest` plugin is installed which adds an `--automake` option to the `pytest` command:

```
~/Code/pyproject-hooks $ pytest --automake
PASS: tests/test_call_hooks.py:test_missing_backend_gives_exception
PASS: tests/test_call_hooks.py:test_get_requires_for_build_wheel
PASS: tests/test_call_hooks.py:test_get_requires_for_build_editable
PASS: tests/test_call_hooks.py:test_get_requires_for_build_sdist
PASS: tests/test_call_hooks.py:test_prepare_metadata_for_build_wheel
[ ... ]
Testsuite summary
# TOTAL: 34
# PASS: 34
# SKIP: 0
# XFAIL: 0
# FAIL: 0
# XPASS: 0
# ERROR: 0
```
