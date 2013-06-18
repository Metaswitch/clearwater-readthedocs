# Troubleshooting and Recovery

This document describes how to troubleshoot some common problems, and associated recovery strategies.

## General

*   Clearwater components are monitored by [monit](http://mmonit.com/monit/) and should be restarted by it if the component fails or hangs.  You can check that components are running by issuing `monit status`.  If components are not running as expected, run `monit start <component>` to start a component or `monit stop <component>` to stop it.

## Ellis

The most common problem from ellis is it reporting "Failed to update server".  This can happen for several reasons.

*   If ellis reports "Failed to update server" when allocating a new number (either after an explicit request or as part of creating a whole new account), check that ellis has free numbers to allocate.  The [create_numbers.py script](https://github.com/Metaswitch/clearwater-docs/wiki/Manual%20Install#ellis) is safe to re-run, to ensure that numbers have been allocated.

*   Check the `/var/log/ellis/ellis-*.log` files.  If these indicate that a timeout occurred communicating with homer or homestead, check that the DNS entries for homer and homestead exist and are configured correctly.  If these are already correct, check homer or homestead to see if they are behaving incorrectly.

To examine ellis' database, run `mysql` (as root), then type `use ellis;` to set the correct database.  You can then issue standard SQL queries on the users and numbers tables, e.g. `SELECT * FROM users WHERE email = '<email address>'`.

## Homer and Homestead

The most common problem on homer and homestead is failing to read or write to the Cassandra database.

*   Check that Cassandra is running.  If not, check its `/var/log/cassandra/*.log` files.

*   Check that Cassandra is configured correctly.  First access the command-line CQL interface by running `cqlsh -3`.  Then type `use homer;` or `use homestead;` to set the correct database.  Finally, issue `describe tables;` - this should report `simservs` on homer and `filter_criteria` and `sip_digests` on homestead.  If these are missing, recreate them by running the section of the [homer](https://github.com/Metaswitch/crest/blob/dev/debian/homer.postinst) or [homestead](https://github.com/Metaswitch/crest/blob/dev/debian/homestead.postinst) post-install scripts, starting at the `echo Connecting to Cassandra on localhost...` line and ending just before the `# Start monit monitoring ourselves` line.

*   Check that Cassandra is clustered correctly (if running a multi-node system).  `nodetool ring` tells you which nodes are in the cluster, and how the keyspace is distributed among them.

If this doesn't help, homer logs to `/var/log/homer/homer-*.log` and homestead logs to `/var/log/homestead/homestead-*.log`.

To examine homer or homestead's database, run `cqlsh -3` and then type `use homer;` or `use homestead;` to set the correct database.  You can then issue CQL queries such as `SELECT * FROM sip_digests WHERE private_id = '<private user ID>'`.

## Sprout

The most common problem on sprout is lack of communication with other nodes, causing registration or calls to fail.  Check that homer and homestead are reachable and responding.

If this doesn't help, sprout logs to `/var/log/sprout/sprout*.txt`.  By default, it is set to log level 2, which only includes errors and very high-level events.  To enable more detailed trace, change the log level to 5 by writing `log_level=5` to `/etc/clearwater/user_settings` (creating it if it doesn't exist already), and then restarting sprout.

Sprout maintains registration state in a memcached cluster.  It's a little clunky to examine this data but you can get some basic information out by running `. /etc/clearwater/config ; telnet $local_ip 11211` to connect to memcached, issuing `stats items`.  This returns a list of entries of the form `STAT items:<slab ID>:...`.  You can then query the keys in each of the slabs with `stats cachedump <slab ID> 0`.

## Bono

The most common problem on bono is lack of communication with sprout.  Check that sprout is reachable and responding.

If this doesn't help, bono logs to `/var/log/bono/sprout*.txt`.  By default, it is set to log level 2, which only includes errors and very high-level events.  To enable more detailed trace, change the log level to 5 by writing `log_level=5` to `/etc/clearwater/user_settings` (creating it if it doesn't exist already), and then restarting bono.

## Chef

*   After stopping/restarting the Chef server, you might see logs as follows.

        merb : chef-server (api) : worker (port 4000) ~ Connection failed - user: chef - (Bunny::ProtocolError)

    This can be worked around by recreating the chef account, as follows, including the `<rabbitMQPass>` you supplied when you [installed the Chef server](Installing a Chef server).

        rabbitmqctl add_vhost /chef
        rabbitmqctl add_user chef <rabbitMQPass>
        rabbitmqctl set_permissions -p /chef chef ".*" ".*" ".*"

## Getting Help

If none of the above helped, please try the [mailing list](http://lists.projectclearwater.org/listinfo/clearwater).