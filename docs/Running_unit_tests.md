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
* Passing `NOISY=T` enables verbose logging during the tests; you can add a logging level (e.g., `NOISY=T:99`) to control which logs you see.
* `make coverage_check` runs code coverage checks (using [gcov](http://gcc.gnu.org/onlinedocs/gcc/Gcov.html)), and reports if the coverage is less than expected.
* `make coverage_raw` outputs coverage information for each source file.
* `make valgrind` runs memory leak checks (using [Valgrind](http://valgrind.org/)).
* `make full_test` runs the coverage and memory leak checks as well as the tests.

## Python Unit Tests

Our components written in Python don't share a common makefile infrastructure. However, each component typically uses the same `make` commands for running the tests. In the top level component directory, run:

* `make test` to run all of the test cases.
* `make coverage` to view the current unit test coverage.
* `make verify` to run [flake8](http://flake8.pycqa.org/en/latest/) over the code to detect errors.
