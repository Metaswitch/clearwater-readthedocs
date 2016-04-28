C++ Coding Guidelines
=====================

Naming
------

-  Class names are CamelCase, beginning with a capital letter.
-  Constant names are ALL\_CAPITALS with underscores separating words.
-  Method, method parameter and local variable names are lowercase with
   underscores separating words, e.g. ``method_name``.
-  Member variable names are lowercase with underscores separating words
   and also begin with an underscore, e.g. ``_member_variable``.

C++ Feature Use
---------------

-  We assume a C++11-compliant compiler, so C++11 features are allowed
   with some exceptions.
-  No use of ``auto`` type declarations.
-  No use of ``using namespace ...``, if the namespace is particularly
   lengthy, consider using namespace aliasing (e.g.
   ``namespace po = boost::program_options``).
-  Avoid using Boost (or similar) libraries that return special
   library-specific pointers, to minimize "infection" of the code-base.
   Consider using the C++11 equivalents instead.

Formatting
----------

C++ code contributed to Clearwater should be formatted according to the
following conventions:

-  Braces on a separate line from function definitions, ``if``
   statements, etc.
-  Two-space indentation
-  Pointer operators attached to the variable type (i.e. ``int* foo``
   rather than ``int *foo``)
-  ``if`` blocks must be surrounded by braces

For example:

::

    if (x)
           int *foo = do_something();

will be replaced with

::

    if (x) 
    {
     int* foo = do_something();
    }

It's possible to fix up some code automatically using
`astyle <http://astyle.sourceforge.net/>`__, with the options
``astyle --style=ansi -s2 -M80 -O -G -k1 -j -o``. This fixes up a lot of
the most common errors (brace style, indentation, overly long lines),
but isn't perfect - there are some cases where breaking the rules makes
the code clearer, and some edge cases (e.g. around switch statements and
casts on multiple lines) where our style doesn't always match astyle's.

Language Features
-----------------

-  Use of the ``auto`` keyword is forbidden.

Commenting
----------

Where it is necessary to document the interface of classes, this should
be done with Doxygen-style comments - three slashes and appropriate
``@param`` and ``@returns`` tags.

::

    /// Apply first AS (if any) to initial request.
    //
    // See 3GPP TS 23.218, especially s5.2 and s6, for an overview of how
    // this works, and 3GPP TS 24.229 s5.4.3.2 and s5.4.3.3 for
    // step-by-step details.
    //
    // @Returns whether processing should stop, continue, or skip to the end.
    AsChainLink::Disposition
    AsChainLink::on_initial_request(CallServices* call_services,

