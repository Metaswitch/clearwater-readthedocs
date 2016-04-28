Debugging Clearwater with GDB and Valgrind
==========================================

Valgrind
--------

`Valgrind <http://valgrind.org/>`__ is a very powerful profiling and
debugging tool.

Before you run Bono or Sprout under valgrind, you may want to tweak
pjsip's code slightly as indicated below, then rebuild and patch your
nodes.

-  Valgrind's memory access tracking hooks into malloc and free.
   Unfortunately, pjsip uses its own memory management functions, and so
   mallocs/frees relatively rarely. To disable this, modify
   ``pjlib/src/pj/pool_caching.c``'s ``pj_caching_pool_init`` function
   to always set cp->max\_capacity to 0.

-  Valgrind's thread safety tool (helgrind) tracks the order in which
   locks are taken, and reports on any lock cycles (which can in theory
   cause deadlocks). One of these locks generates a lot of benign
   results. To prevent these edit ``pjsip\include\pjsip\sip_config.h``
   and set the value of ``PJSIP_SAFE_MODULE`` to 0.

-  Valgrind's thread safety tool also spots variables that are accessed
   on mutliple threads without locking the locking necessary to prevent
   race conditions. Pjsip's memory pools maintain some statistics that
   are not used by Clearwater, but that trip valgrind's race condition
   detection. To suppress this edit ``pjlib/src/pj/pool_caching.c`` and
   remove the bodies of the ``cpool_on_block_alloc`` and
   ``cpool_on_block_free`` (keeping only the bodies).

To run Bono, Sprout or Homestead under valgrind (the example commands
assume you are running sprout), the easiest way is to:

-  Find the command line you are using to run Sprout
   (``ps -eaf | grep sprout``)
-  Make sure valgrind is installed on your system and you have the
   appropriate debug packages installed
   (``sudo apt-get install valgrind`` and
   ``sudo apt-get install sprout-dbg``)
-  Disable monitoring of sprout (``sudo monit unmonitor -g sprout``)
-  Stop sprout (``sudo service sprout stop``)
-  Allow child processes to use more file descriptors, and become the
   sprout user
   (``sudo -i; ulimit -Hn 1000000; ulimit -Sn 1000000; (sudo -u sprout bash);``)
-  Change to the ``/etc/clearwater`` directory
-  Set up the library path
   (``export LD_LIBRARY_PATH=/usr/share/clearwater/sprout/lib:$LD_LIBRARY_PATH``)
-  Run the executable under valgrind, enabling the appropriate valgrind
   options - for example, to use massif to monitor the Sprout heap
   ``valgrind --tools=massif --massif-out-file=/var/log/sprout/massif.out.%p /usr/share/clearwater/bin/sprout <parameters>``
   (the --massif-out-file option is required to ensure the output is
   written to a directory where the sprout user has write permission).
   If any of Sprout parameters include a semi-colon, you must prefix
   this with a backslash otherwise the bash interpreter will interpret
   this as the end of the command.

Valgrind will slow down the running of Bono, Sprout and Homestead by a
factor of 5-10. It will produce output when it detects invalid/illegal
memory access - often these turn out to be benign, but they're rarely
spurious.

GDB
---

Installing
~~~~~~~~~~

To install gdb, simply type ``sudo apt-get install gdb``. gdb is already
installed on build machines, but not on live nodes.

If you're debugging on a live node, it's also worth installing the
sprout or bono debug packages. When we build the standard (release)
versions, we strip all the symbols out and these are saved off
separately in the debug package. Note that you will still be running the
release code - the debug symbols will just be loaded by gdb when you
start it up. To install these packages, type
``sudo apt-get install sprout-dbg`` or
``sudo apt-get install bono-dbg``.
