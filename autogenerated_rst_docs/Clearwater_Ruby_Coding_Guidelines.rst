Ruby Coding Guidelines
======================

Strongly based on https://github.com/chneukirchen/styleguide/ with some
local changes.

Formatting:
-----------

-  Use UTF-8 encoding in your source files.
-  Use 2 space indent, no tabs.
-  Use Unix-style line endings, including on the last line of the file.
-  Use spaces around operators, after commas, colons and semicolons,
   around { and before }.
-  No spaces after (, [ and before ], ).
-  Prefer postfix modifiers (if, unless, rescue) when possible.
-  Indent when as deep as case then indent the contents one step more.
-  Use an empty line before the return value of a method (unless it only
   has one line), and an empty line between defs.
-  Use Yard and its conventions for API documentation. Don't put an
   empty line between the comment block and the definition.
-  Use empty lines to break up a long method into logical paragraphs.
-  Keep lines shorter than 80 characters.
-  Avoid trailing whitespace.

Syntax:
-------

-  Use def with parentheses when there are arguments.
-  Conversely, avoid parentheses when there are none.
-  Never use for, unless you exactly know why. Prefer each or loop.
-  Never use then, a newline is sufficient.
-  Prefer words to symbols.
-  and and or in place of && and \|\|
-  not in place of !
-  Avoid ?:, use if (remember: if returns a value, use it).
-  Avoid if not, use unless.
-  Suppress superfluous parentheses when calling methods, unless the
   method has side-effects.
-  Prefer do...end over {...} for multi-line blocks.
-  Prefer {...} over do...end for single-line blocks.
-  Avoid chaining function calls over multiple lines (implying, use
   {...} for chained functions.
-  Avoid return where not required.
-  Avoid line continuation (\\) where not required.
-  Using the return value of = is okay.
-  if v = array.grep(/foo/)
-  Use \|\|= freely for memoization.
-  When using regexps, freely use =~, -9, :math:`~, ` and $\` when
   needed.
-  Prefer symbols (:name) to strings where applicable.

Naming:
-------

-  Use snake\_case for methods.
-  Use CamelCase for classes and modules. (Keep acronyms like HTTP, RFC
   and XML uppercase.)
-  Use SCREAMING\_CASE for other constants.
-  Use one-letter variables for short block/method parameters, according
   to this scheme:
-  a,b,c: any object
-  d: directory names
-  e: elements of an Enumerable or a rescued Exception
-  f: files and file names
-  i,j: indexes or integers
-  k: the key part of a hash entry
-  m: methods
-  o: any object
-  r: return values of short methods
-  s: strings
-  v: any value
-  v: the value part of a hash entry
-  And in general, the first letter of the class name if all objects are
   of that type (e.g. ``nodes.each { |n| n.name }``)
-  Use \_ for unused variables.
-  When defining binary operators, name the argument other.
-  Use def self.method to define singleton methods.

Comments:
---------

-  Comments longer than a word are capitalized and use punctuation. Use
   two spaces after periods.
-  Avoid superfluous comments. It should be easy to write
   self-documenting code.

Code design
-----------

-  Avoid needless meta-programming.
-  Avoid long methods. Much prefer to go too far the wrong way and have
   multiple one-line methods.
-  Avoid long parameter lists, consider using a hash with documented
   defaults instead.
-  Prefer functional methods over procedural ones (common methods
   below):
-  each - Apply block to each element
-  map - Apply block to each element and remember the returned values.
-  select - Find all matching elements
-  detect - Find first matching element
-  inject - Equivalent to foldl from Haskell
-  Use the mutating version of functional methods (e.g. map!) where
   applicable, rather than using temporary variables.
-  Avoid non-obvious function overloading (e.g. don't use ["0"] \* 8 to
   initialize an array).
-  Prefer objects to vanilla arrays/hashes, this allows you to document
   the structure and interface.
-  Protect the internal data stores from external access. Write API
   functions explicitly.
-  Use attr\_accessor to create getters/setters for simple access.
-  Prefer to add a to\_s function to an object for ease of debugging.
-  Internally, use standard libraries where applicable (See the docs for
   the various APIs).:
-  Hash, Array and Set
-  String
-  Fixnum and Integer
-  Thread and Mutex
-  Fiber
-  Complex
-  Float
-  Dir and File
-  Random
-  Time
-  Prefer string interpolation "blah#{expr}" rather than appending to
   strings.
-  Prefer using the %w{} family of array generators to typing out arrays
   of strings manually.

General:
--------

-  Write ruby -w safe code.
-  Avoid alias, use alias\_method if you absolutely must alias something
   (for Monkey Patching).
-  Use OptionParser for parsing command line options.
-  Target Ruby 2.0 (except where libraries are not compatible, such as
   Chef).
-  Do not mutate arguments unless that is the purpose of the method.
-  Do not mess around in core classes when writing libraries.
-  Do not program defensively.
-  Keep the code simple.
-  Be consistent.
-  Use common sense.

