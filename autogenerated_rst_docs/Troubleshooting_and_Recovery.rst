Troubleshooting and Recovery
============================

This document describes how to troubleshoot some common problems, and
associated recovery strategies.

General
-------

-  Clearwater components are monitored by
   `monit <http://mmonit.com/monit/>`__ and should be restarted by it if
   the component fails or hangs. You can check that components are
   running by issuing ``monit status``. If components are not being
   monitored as expected, run ``monit monitor <component>`` to monitor
   it. To restart a component, we recommend using
   ``service <component> stop`` to stop the component, and allowing
   monit to automatically start the component again.

-  The `Clearwater diagnostics
   monitor <https://github.com/Metaswitch/clearwater-infrastructure/blob/master/clearwater-diags-monitor.md>`__
   detects crashes in native clearwater processes (Bono, Sprout and
   Homestead) and captures a diagnostics bundle containing a core file
   (among other useful information). A diagnostics bundle can also be
   created by running a command line script (``sudo cw-gather_diags``).

-  By default each component logs to ``/var/log/<service>/``, at log
   level 2 (which only includes errors and very high level events). To
   see more detailed logs you can enable debug logging; details for how
   to do this for each component are below. Note that if you want to run
   stress through your deployment, you should revert the log levels back
   to the default level.

-  Changes to ``shared_config`` are detected each time
   ``cw-upload_shared_config`` is run (see `Modifying Clearwater
   settings <Modifying_Clearwater_settings.html>`__), and logged to
   ``/var/log/syslog`` on the node from which the configuration was
   changed.

Ellis
-----

The most common problem from Ellis is it reporting "Failed to update
server". This can happen for several reasons.

-  If Ellis reports "Failed to update server" when allocating a new
   number (either after an explicit request or as part of creating a
   whole new account), check that ellis has free numbers to allocate.
   The `create\_numbers.py
   script <https://github.com/Metaswitch/ellis/blob/dev/docs/create-numbers.md>`__
   is safe to re-run, to ensure that numbers have been allocated.

-  Check the ``/var/log/ellis/ellis-*.log`` files. If these indicate
   that a timeout occurred communicating with Homer or Homestead-prov,
   check that the DNS entries for Homer and Homestead-prov exist and are
   configured correctly. If these are already correct, check Homer or
   Homestead-prov to see if they are behaving incorrectly.

-  To turn on debug logging for Ellis write ``log_level=5`` to
   ``/etc/clearwater/user_settings`` (creating it if it doesn't exist
   already), then restart Ellis (``sudo service ellis stop`` - it will
   be restarted by monit).

To examine Ellis' database, run ``mysql`` (as root), then type
``use ellis;`` to set the correct database. You can then issue standard
SQL queries on the users and numbers tables, e.g.
``SELECT * FROM users WHERE email = '<email address>'``.

Vellum
------

Problems on Vellum may include:

-  Failing to read or write to the Cassandra database (only relevant if
   you deployment is using Homestead-Prov, Homer or Memento):

   -  Check that Cassandra is running (``sudo monit status``). If not,
      check its ``/var/log/cassandra/*.log`` files.
   -  Check that Cassandra is configured correctly. First access the
      command-line CQL interface by running ``cqlsh``. There are 3
      databases:

      -  Type ``use homestead_provisioning;`` to set the provisioning
         database and then ``describe tables;`` - this should report
         ``service_profiles``, ``public``,
         ``implicit_registration_sets`` and ``private``.
      -  Type ``use homestead_cache;`` to set the cache database and
         then ``describe tables;`` - this should report ``impi``,
         ``impi_mapping`` and ``impu``.
      -  Type ``use homer;`` to set the homer database and then
         ``describe tables;`` - this should report ``simservs``.
      -  If any of these are missing, recreate them by running

         -  ``/usr/share/clearwater/cassandra-schemas/homestead_cache.sh``
         -  ``/usr/share/clearwater/cassandra-schemas/homestead_provisioning.sh``
         -  ``/usr/share/clearwater/cassandra-schemas/homer.sh``

   -  Check that Cassandra is clustered correctly (if running a
      multi-node system). ``nodetool status`` tells you which nodes are
      in the cluster, and how the keyspace is distributed among them.
   -  To examine Vellum's database, run ``cqlsh`` and then type
      ``use homer;``, ``use homestead_provisioning;`` or
      ``use homestead_cache`` to set the correct database. You can then
      issue CQL queries such as
      ``SELECT * FROM impi WHERE private_id = '<private user ID>'``.

-  Problems with the memcached cluster:

   -  It's a little clunky to examine this data but you can get some
      basic information out by running
      ``. /etc/clearwater/config ; telnet $local_ip 11211`` to connect
      to memcached, issuing ``stats items``. This returns a list of
      entries of the form ``STAT items:<slab ID>:...``. You can then
      query the keys in each of the slabs with
      ``stats cachedump <slab ID> 0``.
   -  Memcached logs to ``/var/log/memcached.log``. It logs very little
      by default, but it is possible to make it more verbose by editing
      ``/etc/memcached_11211.conf``, uncommenting the ``-vv`` line, and
      then restarting memcached

-  Problems with the `Chronos <https://github.com/Metaswitch/chronos>`__
   cluster.

   -  Chronos logs to ``/var/log/chronos/chronos*``.
   -  Details of how to edit the Chronos configuration are
      `here <https://github.com/Metaswitch/chronos/blob/dev/doc/configuration.md>`__.

Sprout
------

The most common problem on Sprout is lack of communication with other
nodes and processes, causing registration or calls to fail. Check that
Vellum and Dime are reachable and responding.

To turn on debug logging for Sprout write ``log_level=5`` to
``/etc/clearwater/user_settings`` (creating it if it doesn't exist
already), then restart Sprout (``sudo service sprout stop`` - it will be
restarted by monit).

If you see Sprout dying/restarting with no apparent cause in
``/var/log/sprout/sprout*.txt``, check ``/var/log/monit.log`` and
``/var/log/syslog`` around that time - these can sometimes give clues as
to the cause.

Bono
----

The most common problem on Bono is lack of communication with Sprout.
Check that Sprout is reachable and responding.

To turn on debug logging for Bono write ``log_level=5`` to
``/etc/clearwater/user_settings`` (creating it if it doesn't exist
already), then restart Bono (``sudo service bono stop`` - it will be
restarted by monit).

If you see Bono dying/restarting with no apparent cause in
``/var/log/bono/bono*.txt``, check ``/var/log/monit.log`` and
``/var/log/syslog`` around that time - these can sometimes give clues as
to the cause.

Dime
----

The most common problems on Dime are:

-  Lack of communication with Vellum. Check that Vellum is reachable and
   responding.
-  (If using Ralf) Lack of communication with a CCF. Check that your CCF
   is reachable and responding (if you don't have a CCF, you don't need
   Ralf).

To turn on debug logging for Ralf, Homestead or Homestead-prov write
``log_level=5`` to ``/etc/clearwater/user_settings`` (creating it if it
doesn't exist already), then restart the service
(``sudo service <ralf|homestead|homestead-prov> stop`` - it will be
restarted by monit).

If you see Ralf, Homestead or Homestead-prov dying/restarting with no
apparent cause in ``/var/log/<service>/<service>*.txt``, check
``/var/log/monit.log`` and ``/var/log/syslog`` around that time - these
can sometimes give clues as to the cause.

Deployment Management
---------------------

Clearwater comes with a system that `automate clustering and
configuration sharing <Automatic_Clustering_Config_Sharing.html>`__. If
you cannot scale your deployment up or down, or if configuration changes
are not being applied, this system may not be working.

-  The management system logs to ``/var/log/clearwater-etcd``,
   ``/var/log/clearwater-cluster-manager``,
   ``/var/log/clearwater-config-manager`` and
   ``/var/log/clearwater-queue-manager``. To turn on debug logging write
   ``log_level=5`` to ``/etc/clearwater/user_settings`` (creating it if
   it doesn't exist already), then restart the etcd processes
   (``sudo service <clearwater-config-manager|clearwater-cluster-manager|clearwater-queue-manager> stop``
   - they will be restarted by monit)
-  ``cw-check_cluster_state`` will display information about the state
   of the various data-store clusters used by Clearwater.
-  ``sudo cw-check_config_sync`` will display whether the node has
   learned shared configuration.
-  ``sudo cw-check_restart_queue_state`` will display whether there is
   new shared configuration that is being synched across the deployment,
   and which nodes are using the new shared configuration.
-  The following commands can be useful for inspecting the state of the
   underlying etcd cluster used by the management system:

   ::

       clearwater-etcdctl cluster-health
       clearwater-etcdctl member list

Getting Help
------------

If none of the above helped, please try the `mailing
list <http://lists.projectclearwater.org/mailman/listinfo/clearwater_lists.projectclearwater.org>`__.
