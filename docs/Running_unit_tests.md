# Unit tests 

Project Clearwater has various types of regression testing.

We have [live tests](https://github.com/Metaswitch/clearwater-live-test) which we run regularly over our deployments. We have [FV tests](https://github.com/Metaswitch/clearwater-fv-test) that we run any time the underlying code changes. We also have unit tests; these are specific to a repository, and are run anytime any changes are made to the repository.

This document describes how to run the unit tests for the different Clearwater repositories.

## C++ Unit Tests

For our components written in C++, we use a common makefile [infrastructure](https://github.com/Metaswitch/clearwater-build-infra/blob/master/cpp.mk).

To run the unit tests, change to the `src` subdirectory below the top-level component directory and issue `make test`.

The unit tests use the [Google Test](https://code.google.com/p/googletest/) framework, so the output from the test run looks something like this.

    [==========] Running 92 tests from 20 test cases.
    [----------] Global test environment set-up.
    [----------] 1 test from AuthenticationTest
    [ RUN      ] AuthenticationTest.NoAuthorization
    [       OK ] AuthenticationTest.NoAuthorization (27 ms)
    [----------] 1 test from AuthenticationTest (27 ms total)

    [----------] 6 tests from SimServsTest
    [ RUN      ] SimServsTest.EmptyXml
    [       OK ] SimServsTest.EmptyXml (1 ms)
    ...
    [ RUN      ] SessionCaseTest.Names
    [       OK ] SessionCaseTest.Names (0 ms)
    [----------] 1 test from SessionCaseTest (0 ms total)

    [----------] Global test environment tear-down
    [==========] 92 tests from 20 test cases ran. (27347 ms total)
    [  PASSED  ] 92 tests.

There are various other options for the unit tests as well:

* Passing `JUSTTEST=testname` just runs the specified test case.
* Passing `NOISY=T` prints the logs made during the test run to the screen. You can set what severity of logs are printed by adding a logging level; the logging level matches the severity levels for our logs (defined [here](https://github.com/Metaswitch/cpp-common/blob/master/include/log.h#L53)). For example, `NOISY=T:2` prints all logs up to STATUS severity and `NOISY=T:5` prints all logs up to DEBUG severity.
* `make coverage_check` runs code coverage checks (using [gcov](http://gcc.gnu.org/onlinedocs/gcc/Gcov.html)), and reports if the coverage is less than expected.
* `make coverage_raw` outputs coverage information for each source file.
* `make valgrind` runs memory leak checks (using [Valgrind](http://valgrind.org/)).
* `make full_test` runs the coverage and memory leak checks as well as the tests.

## Python Unit Tests

Our components written in Python don't share a common makefile infrastructure. However, each component typically uses the same `make` commands for running the tests. In the top level component directory, run:

* `make test` to run all of the test cases.
* `make coverage` to view the current unit test coverage.
* `make verify` to run [flake8](http://flake8.pycqa.org/en/latest/) over the code to detect errors.


We do not use tools like pylint by default, as they can be too aggressive and provide a large number of benign errors, often in third party modules. However, it can be difficult to track down import errors using the standard test infrastructure we have in place, and it can be useful under these circumstances to be able to run pylint to draw out any bad imports that might be causing the modules or unit tests to fail.

For example, if we deliberately break an import in the cluster_manager plugin_base.py file (changing `from abc import ...` to `from NOTabc import ...`), running `make test` gives the following output:

```
Traceback (most recent call last):
  File "cluster_mgr_setup.py", line 52, in <module>
    tests_require=["pbr==1.6", "Mock"],
  File "/usr/lib/python2.7/distutils/core.py", line 151, in setup
    dist.run_commands()
  File "/usr/lib/python2.7/distutils/dist.py", line 953, in run_commands
    self.run_command(cmd)
  File "/usr/lib/python2.7/distutils/dist.py", line 972, in run_command
    cmd_obj.run()
  File "build/bdist.linux-x86_64/egg/setuptools/command/test.py", line 170, in run
  File "build/bdist.linux-x86_64/egg/setuptools/command/test.py", line 191, in run_tests
  File "/usr/lib/python2.7/unittest/main.py", line 94, in __init__
    self.parseArgs(argv)
  File "/usr/lib/python2.7/unittest/main.py", line 149, in parseArgs
    self.createTests()
  File "/usr/lib/python2.7/unittest/main.py", line 158, in createTests
    self.module)
  File "/usr/lib/python2.7/unittest/loader.py", line 130, in loadTestsFromNames
    suites = [self.loadTestsFromName(name, module) for name in names]
  File "/usr/lib/python2.7/unittest/loader.py", line 103, in loadTestsFromName
    return self.loadTestsFromModule(obj)
  File "build/bdist.linux-x86_64/egg/setuptools/command/test.py", line 39, in loadTestsFromModule
  File "/usr/lib/python2.7/unittest/loader.py", line 100, in loadTestsFromName
    parent, obj = obj, getattr(obj, part)
AttributeError: 'module' object has no attribute 'contention_detecting_plugin'
```

The error, `AttributeError: 'module' object has no attribute 'xxx'`, is not very helpful in identifying the source of the error. Running pylint (as below) however, will give an error output in the following form:

```
[
    {
        "message": "Unable to import 'NOTabc'",
        "obj": "",
        "column": 0,
        "path": "src/metaswitch/clearwater/cluster_manager/plugin_base.py",
        "line": 33,
        "type": "error",
        "symbol": "import-error",
        "module": "metaswitch.clearwater.cluster_manager.plugin_base"
    }
]
```

The following commands will install and run pylint in your local virtual environment:

```
make clean && make env
_env/bin/easy_install pylint
PYTHONPATH=src:common _env/bin/python -m pylint --disable=all --enable=F,E --output-format json <path_to_modules>
```

Where the `path_to_modules` is the module or package directory of the code you want to check. For our projects, this will usually be under `src/metaswitch/`, e.g. in the clearwater-etcd repo, to test all of clearwater-etcd, use `src/metaswitch/clearwater/` as the path, but to have pylint inspect just the cluster-manager plugin_base file, use `src/metaswitch/clearwater/cluster_manager/plugin_base.py`.
