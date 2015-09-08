# Troubleshooting and Recovery

This document describes how to troubleshoot some common problems, and associated recovery strategies.

## General

*  Clearwater components are monitored by [monit](http://mmonit.com/monit/) and should be restarted by it if the component fails or hangs.  You can check that components are running by issuing `monit status`.  If components are not running as expected, run `monit start <component>` to start a component or `monit stop <component>` to stop it. To restart a component, we recommend using `service <component> stop` to stop the component, and allowing monit to automatically start the component again.

*  The [Clearwater diagnostics monitor](https://github.com/Metaswitch/clearwater-infrastructure/blob/master/clearwater-diags-monitor.md) detects crashes in native clearwater processes (bono, sprout and homestead) and captures a diagnostics bundle containing a core file (among other useful information).  A diagnostics bundle can also be created by running a command line script.

*  By default each component logs to `/var/log/<service>/`, at log level 2 (which only includes errors and very high level events). To see more detailed logs you can enable debug logging; details for how to do this for each component are below. Note that if you want to run stress through your deployment, you should revert the log levels back to the default level.

## Ellis

The most common problem from ellis is it reporting "Failed to update server".  This can happen for several reasons.

*   If ellis reports "Failed to update server" when allocating a new number (either after an explicit request or as part of creating a whole new account), check that ellis has free numbers to allocate.  The [create_numbers.py script](Manual_Install/#ellis) is safe to re-run, to ensure that numbers have been allocated.

*   Check the `/var/log/ellis/ellis-*.log` files.  If these indicate that a timeout occurred communicating with homer or homestead, check that the DNS entries for homer and homestead exist and are configured correctly.  If these are already correct, check homer or homestead to see if they are behaving incorrectly.

*  To turn on debug logging for Ellis, write `LOG_LEVEL = logging.DEBUG` to the `local_settings.py` file (at `/usr/share/clearwater/ellis/src/metaswitch/ellis/local_settings.py`). Then restart clearwater-infrastructure (`sudo service clearwater-infrastructure restart`), and restart Ellis (`sudo service ellis stop` - it will be restarted by monit).

To examine ellis' database, run `mysql` (as root), then type `use ellis;` to set the correct database.  You can then issue standard SQL queries on the users and numbers tables, e.g. `SELECT * FROM users WHERE email = '<email address>'`.

## Homer and Homestead

The most common problem on homer and homestead is failing to read or write to the Cassandra database.

*   Check that Cassandra is running (`sudo monit status`).  If not, check its `/var/log/cassandra/*.log` files.

*   Check that Cassandra is configured correctly.  First access the command-line CQL interface by running `cqlsh`.

    *   If you're on homer, type `use homer;` to set the correct database and then `describe tables;` - this should report `simservs`.  If this is missing, recreate it by running `/usr/share/clearwater/cassandra-schemas/homer.sh`.

   *    If you're on homestead, there are 2 databases.  Type `use homestead_provisioning;` to set the provisioning database and then `describe tables;` - this should report `service_profiles`, `public`, `implicit_registration_sets` and `private`.  Then type `use homestead_cache;` to set the cache database and then `describe tables;` as before - this should report `impi`, `impi_mapping` and `impu`.  If any of these are missing, recreate them by running `/usr/share/clearwater/cassandra-schemas/homestead_cache.sh` and `/usr/share/clearwater/cassandra-schemas/homestead_provisioning.sh`.

*   Check that Cassandra is clustered correctly (if running a multi-node system).  `nodetool status` tells you which nodes are in the cluster, and how the keyspace is distributed among them.

*   If this doesn't help, homer logs to `/var/log/homer/homer-*.log` and homestead logs to `/var/log/homestead/homestead-*.log` and `/var/log/homestead-prov/homestead-*.log`. To turn on debug logging for Homer or Homestead-prov, write `LOG_LEVEL = logging.DEBUG` to the `local_settings.py` file (at `/usr/share/clearwater/<homer|homestead-prov>/src/metaswitch/crest/local_settings.py`). Then restart clearwater-infrastructure (`sudo service clearwater-infrastructure restart`), and restart Homer/Homestead-prov (`sudo service <homer|homestead-prov> stop` - they will be restarted by monit). To turn on debug logging for Homestead write `log_level=5` to `/etc/clearwater/user_settings` (creating it if it doesn't exist already), then restart Homestead (`sudo service homestead stop` - it will be restarted by monit).

To examine homer or homestead's database, run `cqlsh` and then type `use homer;`, `use homestead_provisioning;` or `use homestead_cache` to set the correct database.  You can then issue CQL queries such as `SELECT * FROM impi WHERE private_id = '<private user ID>'`.

## Sprout

The most common problem on sprout is lack of communication with other nodes, causing registration or calls to fail.  Check that homer and homestead are reachable and responding.

Sprout maintains registration state in a memcached cluster.  It's a little clunky to examine this data but you can get some basic information out by running `. /etc/clearwater/config ; telnet $local_ip 11211` to connect to memcached, issuing `stats items`.  This returns a list of entries of the form `STAT items:<slab ID>:...`.  You can then query the keys in each of the slabs with `stats cachedump <slab ID> 0`.

To turn on debug logging for Sprout write `log_level=5` to `/etc/clearwater/user_settings` (creating it if it doesn't exist already), then restart Sprout (`sudo service sprout stop` - it will be restarted by monit).

Memcached logs to `/var/log/memcached.log`. It logs very little by default, but it is possible to make it more verbose by editing `/etc/memcached_11211.conf`, uncommenting the `-vv` line, and then restarting memcached.

Sprout also uses [Chronos](https://github.com/Metaswitch/chronos) to track registration, subscription and authorization timeouts. Chronos logs to `/var/log/chronos/chronos*`. Details of how to edit the Chronos configuration is [here](https://github.com/Metaswitch/chronos/blob/dev/doc/configuration.md).

If you see sprout dying/restarting with no apparent cause in `/var/log/sprout/sprout*.txt`, check `/var/log/monit.log` and `/var/log/syslog` around that time - these can sometimes give clues as to the cause.

## Bono

The most common problem on bono is lack of communication with sprout.  Check that sprout is reachable and responding.

To turn on debug logging for Bono write `log_level=5` to `/etc/clearwater/user_settings` (creating it if it doesn't exist already), then restart Bono (`sudo service bono stop` - it will be restarted by monit).

If you see bono dying/restarting with no apparent cause in `/var/log/bono/bono*.txt`, check `/var/log/monit.log` and `/var/log/syslog` around that time - these can sometimes give clues as to the cause.

## Ralf

To turn on debug logging for Ralf write `log_level=5` to `/etc/clearwater/user_settings` (creating it if it doesn't exist already), then restart Ralf (`sudo service ralf stop` - it will be restarted by monit).

Ralf also uses [Chronos](https://github.com/Metaswitch/chronos) to track call timeouts. Chronos logs to `/var/log/chronos/chronos*`. Details of how to edit the Chronos configuration is [here](https://github.com/Metaswitch/chronos/blob/dev/doc/configuration.md).

If you see Ralf dying/restarting with no apparent cause in `/var/log/ralf/ralf*.txt`, check `/var/log/monit.log` and `/var/log/syslog` around that time - these can sometimes give clues as to the cause.

## Deployment Management

Clearwater comes with a system that [automate clustering and configuration sharing](Automatic_Clustering_Config_Sharing.md). If you cannot scale your deployment up or down, or if configuration changes are not being applied, this system may not be working.

* The management system logs to `/var/log/clearwater-etcd`, `/var/log/clearwater-cluster-manager` and `/var/log/clearwater-config-manager`. To turn on debug logging write `log_level=5` to `etc/clearwater/user_settings` (creating it if it doesn't exist already), then restart the etcd processes (`sudo service <clearwater-config-manager|clearwater-cluster-manager> stop` - they will be restarted by monit)
* `/usr/share/clearwater/clearwater-cluster-manager/scripts/check_cluster_state` will display information about the state of the various data-store clusters used by Clearwater.
* `sudo /usr/share/clearwater/clearwater-config-manager/scripts/check_config_sync` will display whether the node has learned shared configuration.
* The following commands can be useful for inspecting the state of the underlying etcd cluster used by the management system:

        clearwater-etcdctl cluster-health
        clearwater-etcdctl member list


## Getting Help

If none of the above helped, please try the [mailing list](http://lists.projectclearwater.org/listinfo/clearwater).
