## Valgrind

[Valgrind](http://valgrind.org/) is a very powerful profiling and debugging tool. 

Before you run valgrind, you'll want to tweak pjsip's code slightly.  Valgrind's memory access tracking hooks into malloc and free.  Unfortunately, pjsip uses its own memory management functions, and so mallocs/frees relatively rarely.  To disable this, modify `pjlib/src/pj/pool_caching`'s `pj_caching_pool_init` function to always set cp->max_capacity to 0.  Then rebuild and patch your nodes.

To run Sprout under valgrind

-  make sure valgrind is installed on your system and you have the Sprout debug packages installed (`sudo apt-get install valgrind` and `sudo apt-get install sprout-dbg`)

-  disable monitoring of sprout (`sudo monit unmonitor poll-sprout; sudo monit unmonitor sprout`)

-  use ps to find the command line you are using to run Sprout (`ps -eaf | grep sprout`)

-  change to the sprout user (`sudo -u sprout bash`)

-  change to the /etc/clearwater directory

-  set up the library path (`export LD_LIBRARY_PATH=/usr/share/clearwater/lib`)

-  run the sprout executable under valgrind, enabling the appropriate valgrind options - for example, to use massif to monitor the heap `valgrind --tools=massif /usr/share/clearwater/bin/sprout <parameters>` (if any of the parameters include a semi-colon, you must prefix this with a backslash otherwise the bash interpreter will interpret this as the end of the command).

Valgrind will slow down the running of bono and sprout by a factor of 5-10.  It will produce output when it detects invalid/illegal memory access - often these turn out to be benign, but they're rarely spurious.

## GDB 
### Installing
To install gdb, simply type `sudo apt-get install gdb`.  gdb is already installed on build machines, but not on live nodes.

If you're debugging on a live node, it's also worth installing the sprout or bono debug packages.  When we build the standard (release) versions, we strip all the symbols out and these are saved off separately in the debug package.  Note that you will still be running the release code - the debug symbols will just be loaded by gdb when you start it up.  To install these packages, type `sudo apt-get install sprout-dbg` or `sudo apt-get install bono-dbg`.

### Unpacking crash dumps

We use apport to manage crash dumps.  The dumps exist temporarily in `/var/crash`. To unpack a crash dump, run `apport-unpack <crash dump name> <directory to unpack into>`.  The core file is called CoreDump.