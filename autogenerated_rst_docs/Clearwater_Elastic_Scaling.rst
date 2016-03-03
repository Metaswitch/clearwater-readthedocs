Elastic Scaling
===============

The core Clearwater nodes have the ability to elastically scale; in
other words, you can grow and shrink your deployment on demand, without
disrupting calls or losing data.

This page explains how to use this elastic scaling function when using a
deployment created through the `automated <Automated_Install.md>`__ or
`manual <Manual_Install.md>`__ install processes. Note that, although
the instructions differ between the automated and manual processes, the
underlying operations that will be performed on your deployment are the
same - the automated process simply uses chef to drive this rather than
issuing the commands manually.

Before scaling your deployment
------------------------------

Before scaling up or down, you should decide how many each of Bono,
Sprout, Homestead, Homer and Ralf nodes you need (i.e. your target
size). This should be based on your call load profile and measurements
of current systems, though based on experience we recommend scaling up a
tier of a given type (sprout, bono, etc.) when the average CPU
utilization within that tier reaches ~60%. The `Deployment Sizing
Spreadsheet <http://www.projectclearwater.org/technical/clearwater-performance/>`__
may also provide useful input.

Performing the resize
---------------------

If you did an Automated Install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To resize your automated deployment, run:

::

    knife deployment resize -E <env> --sprout-count <n> --bono-count <n> --homer-count <n> --homestead-count <n> --ralf-count <n>

Where the ``<n>`` values are how many nodes of each type you need. Once
this command has completed, the resize operation has completed and any
nodes that are no longer needed will have been terminated.

More detailed documentation on the available Chef commands is available
`here <https://github.com/Metaswitch/chef/blob/master/docs/knife_commands.mdhttps://github.com/Metaswitch/chef/blob/master/docs/knife_commands.md>`__.

If you did a Manual Install
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Follow these instructions if you manually installed your deployment and
are using Clearwater's `automatic clustering and configuration
sharing <Automatic_Clustering_Config_Sharing>`__ functionality.

If you're scaling up your deployment, follow the following process:

1. Spin up new nodes, following the `standard install
   process <Manual_Install>`__, but with the following modifications:

   -  Set the ``etcd_cluster`` so that it only includes the nodes that
      are already in the deployment (so it does not include the nodes
      being added).
   -  Stop when you get to the "Provide Shared Configuration" step. The
      nodes will learn their configuration from the existing nodes.

2. Wait until the new nodes have fully joined the existing deployment.
   To check if a node has joined the deployment:

   -  Run
      ``/usr/share/clearwater/clearwater-cluster-manager/scripts/check_cluster_state``.
      This should report that the local node is in all of its clusters
      and that the cluster is stable.
   -  Run
      ``sudo /usr/share/clearwater/clearwater-config-manager/scripts/check_config_sync``.
      This reports when the node has learned its configuration.

3. Update DNS to contain the new nodes.

If you're scaling down your deployment, follow the following process:

1. Update DNS to contain the nodes that will remain after the
   scale-down.
2. On each node that is about to be turned down:

   -  Run ``monit unmonitor -g <node-type>``. For example for a sprout
      node: ``monit unmonitor -g sprout``. On a homestead node also run
      ``monit unmonitor -g homestead-prov``.
   -  Start the main process quiescing.

      -  Sprout - ``sudo service sprout quiesce``
      -  Bono - ``sudo service bono quiesce``
      -  Homestead -
         ``sudo service homestead stop && sudo service homestead-prov stop``
      -  Homer - ``sudo service homer stop``
      -  Ralf -``sudo service ralf stop``
      -  Ellis - ``sudo service ellis stop``
      -  Memento - ``sudo service memento stop``

   -  Unmonitor the clearwater management processes:

      -  ``sudo monit unmonitor clearwater_cluster_manager``
      -  ``sudo monit unmonitor clearwater_config_manager``
      -  ``sudo monit unmonitor -g etcd``

   -  Run ``sudo service clearwater-etcd decommission``. This will cause
      the nodes to leave their existing clusters.

3. Once the above steps have completed, turn down the nodes.

If you did a Manual Install without Automatic Clustering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Follow these instructions if you manually installed your deployment but
are *not* using Clearwater's `automatic clustering and configuration
sharing <Automatic_Clustering_Config_Sharing>`__ functionality.

If you're scaling up your deployment, follow the following process.

1.  Spin up new nodes, following the `standard install
    process <Manual_Install.md>`__.
2.  On Sprout and Ralf nodes, update
    ``/etc/clearwater/cluster_settings`` to contain both a list of the
    old nodes (``servers=...``) and a (longer) list of the new nodes
    (``new_servers=...``) and then run ``service <process> reload`` to
    re-read this file. Do the same on Memento nodes, but use
    ``/etc/clearwater/memento_cluster_settings`` as the file.
3.  On new Memento, Homestead and Homer nodes, follow the `instructions
    on the Cassandra
    website <http://www.datastax.com/documentation/cassandra/1.2/cassandra/operations/ops_add_node_to_cluster_t.html>`__
    to join the new nodes to the existing cluster.
4.  On Sprout and Ralf nodes, update
    ``/etc/chronos/chronos_cluster.conf`` to contain a list of all the
    nodes (see
    `here <https://github.com/Metaswitch/chronos/blob/dev/doc/clustering.md>`__
    for details of how to do this) and then run
    ``service chronos reload`` to re-read this file.
5.  On Sprout, Memento and Ralf nodes, run ``service astaire reload`` to
    start resynchronization.
6.  On Sprout and Ralf nodes, run ``service chronos resync`` to start
    resynchronization of Chronos timers.
7.  Update DNS to contain the new nodes.
8.  On Sprout, Memento and Ralf nodes, wait until Astaire has
    resynchronized, either by running ``service astaire wait-sync`` or
    by polling over `SNMP <Clearwater_SNMP_Statistics.md>`__.
9.  On Sprout and Ralf nodes, wait until Chronos has resynchronized,
    either by running ``service chronos wait-sync`` or by polling over
    `SNMP <Clearwater_SNMP_Statistics.md>`__.
10. On all nodes, update /etc/clearwater/cluster\_settings and
    /etc/clearwater/memento\_cluster\_settings to just contain the new
    list of nodes (``servers=...``) and then run
    ``service <process> reload`` to re-read this file.

If you're scaling down your deployment, follow the following process.

1.  Update DNS to contain the nodes that will remain after the
    scale-down.
2.  On Sprout and Ralf nodes, update
    ``/etc/clearwater/cluster_settings`` to contain both a list of the
    old nodes (``servers=...``) and a (shorter) list of the new nodes
    (``new_servers=...``) and then run ``service <process> reload`` to
    re-read this file. Do the same on Memento nodes, but use
    ``/etc/clearwater/memento_clus ter_settings`` as the file.
3.  On leaving Memento, Homestead and Homer nodes, follow the
    `instructions on the Cassandra
    website <http://www.datastax.com/documentation/cassandra/1.2/cassandra/operations/ops_remove_node_t.html>`__
    to remove the leaving nodes from the cluster.
4.  On Sprout and Ralf nodes, update
    ``/etc/chronos/chronos_cluster.conf`` to mark the nodes that are
    being scaled down as leaving (see
    `here <https://github.com/Metaswitch/chronos/blob/dev/doc/clustering.md>`__
    for details of how to do this) and then run
    ``service chronos reload`` to re-read this file.
5.  On Sprout, Memento and Ralf nodes, run ``service astaire reload`` to
    start resynchronization.
6.  On the Sprout and Ralf nodes that are staying in the Chronos
    cluster, run ``service chronos resync`` to start resynchronization
    of Chronos timers.
7.  On Sprout, Memento and Ralf nodes, wait until Astaire has
    resynchronized, either by running ``service astaire wait-sync`` or
    by polling over `SNMP <Clearwater_SNMP_Statistics.md>`__.
8.  On Sprout and Ralf nodes, wait until Chronos has resynchronized,
    either by running ``service chronos wait-sync`` or by polling over
    `SNMP <Clearwater_SNMP_Statistics.md>`__.
9.  On Sprout, Memento and Ralf nodes, update
    /etc/clearwater/cluster\_settings and
    /etc/clearwater/memento\_cluster\_settings to just contain the new
    list of nodes (``servers=...``) and then run
    ``service <process> reload`` to re-read this file.
10. On the Sprout and Ralf nodes that are staying in the cluster, update
    ``/etc/chronos/chronos_cluster.conf`` so that it only contains
    entries for the staying nodes in the cluster and then run
    ``service chronos reload`` to re-read this file.
11. On each node that is about to be turned down:

    -  Run ``monit unmonitor -g <node-type>``. For example for a sprout
       node: ``monit unmonitor -g sprout``. On a homestead node also run
       ``monit unmonitor -g homestead-prov``.
    -  Start the main process quiescing.

       -  Sprout - ``sudo service sprout quiesce``
       -  Bono - ``sudo service bono quiesce``
       -  Homestead - ``sudo service homestead stop``
       -  Homer - ``sudo service homer stop``
       -  Ralf -``sudo service ralf stop``
       -  Ellis - ``sudo service ellis stop``
       -  Memento - ``sudo service memento stop``

12. Turn down each of these nodes once the process has terminated.


