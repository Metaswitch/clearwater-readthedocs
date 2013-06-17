## Valgrind

[Valgrind](http://valgrind.org/) is a very powerful profiling and debugging tool. 

Before you run valgrind, you'll want to tweak pjsip's code slightly.  Valgrind's memory access tracking hooks into malloc and free.  Unfortunately, valgrind uses its own memory management functions, and so mallocs/frees relatively rarely.  To disable this, modify `pjlib/src/pj/pool_caching`'s `pj_caching_pool_init` function to always set cp->max_capacity to 0.  Then rebuild and patch your nodes.

To run bono and sprout under valgrind, just use the normal command-line command prefixed by "valgrind", e.g. `valgrind /usr/share/clearwater/bin/sprout`.

Valgrind will slow down the running of bono and sprout by a factor of 5-10.  It will produce output when it detects invalid/illegal memory access - often these turn out to be benign, but they're rarely spurious.

## GDB 
### Installing
To install gdb, simply type "sudo apt-get install gdb".  gdb is already installed on build machines, but not on live nodes.

If you're debugging on a live node, it's also worth installing the sprout or bono debug packages.  When we build the standard (release) versions, we strip all the symbols out and these are saved off separately in the debug package.  Note that you will still be running the release code - the debug symbols will just be loaded by gdb when you start it up.  To install these packages, type "sudo apt-get install sprout-dbg" or "sudo apt-get install bono-dbg".

### Unpacking crash dumps

We use apport to manage crash dumps.  The dumps temporarily exist in /var/crash before being copied to www/crash on the build machine and user account that built them.  They are copied off the local machine by clearwater_crash_monitor - kill this process is you want them to stay local.

To unpack a crash dump, run "apport-unpack <crash dump name> <directory to unpack into>".  The core file is called CoreDump.