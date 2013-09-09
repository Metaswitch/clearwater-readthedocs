## Naming

*   Class names are CamelCase, beginning with a capital letter.
*   Constant names are ALL_CAPITALS with underscores separating words.
*   Method, method parameter and local variable names are lowercase with underscores separating words, e.g. `method_name`.
*   Member variable names are lowercase with underscores separating words and also begin with an underscore, e.g. `_member_variable`.

## Formatting
C++ code contributed to Clearwater should be formatted consistently using [astyle](http://astyle.sourceforge.net/). The particular options we use for Clearwater code are `astyle --style=ansi -s2 -G -k1 -j`. This enforces the following conventions:
* Braces on a separate line from function definitions, `if` statements, etc.
* Two-space indentation
* Pointer operators attached to the variable type (i.e. `int* foo` rather than `int *foo`)
* `if` blocks must be surrounded by braces

For example:
```
if (x)
       int *foo = do_something();
```
will be replaced with
```
if (x) 
{
 int* foo = do_something();
}
```