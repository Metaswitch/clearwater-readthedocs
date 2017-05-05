Dealing with Multiple Failed Nodes
----------------------------------

If any site in your deployment loses half or more of its etcd master
nodes permanently, it loses "quorum". This means that the underlying
etcd cluster becomes read-only. While the etcd cluster is in this state,
you can't perform any scaling operations or change configuration and
have it synced across the deployment. You should use this process to
recover the etcd cluster in the failed site.

If you haven't lost half (or more) of your etcd master nodes in a site,
then you can use the process described
`here <http://clearwater.readthedocs.io/en/latest/Handling_Failed_Nodes.html#removing-a-failed-node>`__
for each of your failed nodes.

Procedure
~~~~~~~~~

The procedure creates a new etcd cluster to replace the existing
cluster. The new cluster is populated with the configuration saved in
the configuration files on disk. This allows us to recreate the cluster,
even in cases when the existing cluster is too badly corrupted to read
from.

This procedure won't impact service. You should follow this process
completely - the behaviour is unspecified if this process is started but
not completed. It is always safe to restart this process from the
beginning (for example, if you encounter an error partway through).

If there are no live Vellum nodes in the site, you should continue with
this process, missing out the steps that require running commands on
Vellum. Once the etcd cluster is recovered, you should add the new
replacement nodes.

Stop the etcd processes
~~~~~~~~~~~~~~~~~~~~~~~

Stop the etcd processes on every node in the affected site.

-  Run ``sudo monit stop -g etcd``
-  Run ``sudo monit stop -g clearwater_cluster_manager``
-  Run ``sudo monit stop -g clearwater_config_manager``
-  Run ``sudo monit stop -g clearwater_queue_manager``
-  Run ``sudo touch /etc/clearwater/no_cluster_manager``
-  Run ``sudo rm -rf  /var/lib/clearwater-etcd/*``

Select your master nodes
~~~~~~~~~~~~~~~~~~~~~~~~

To follow this process you need to choose some nodes to be the new
masters of the etcd cluster:

-  If you have 3 or more working Vellum nodes in the site, you should
   use those
-  If not, you should use all the nodes in the site

Check the configuration on your nodes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The next step is to ensure that the configuration files on each node are
correct.

Any of the master nodes - Shared configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The shared configuration is at ``/etc/clearwater/shared_config``. Verify
that this is correct, then copy this file onto every other master node.
Please see the `configuration options
reference <http://clearwater.readthedocs.io/en/latest/Clearwater_Configuration_Options_Reference.html>`__
for more details on how to set the configuration values.

Vellum - Chronos configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  The configuration file is at ``/etc/chronos/chronos_cluster.conf``.
-  Verify that this is present and syntactically correct on all Vellum
   nodes in the affected site.

   -  This should follow the format
      `here <https://github.com/Metaswitch/chronos/blob/dev/doc/clustering.md#clustering-chronos>`__.
   -  If the file isn't present, or is invalid, then make the
      configuration file contain all Vellum nodes in the site as nodes.
   -  Otherwise, don't change the states of any nodes in the file (even
      if you know the node has failed).

-  If there is more than one failed node then there will be timer
   failures until this process has been completed. This could prevent
   subscribers from receiving notifications when their
   registrations/subscriptions expire.

Vellum - Memcached configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  The configuration file is at ``/etc/clearwater/cluster_settings``.
-  Verify that this is present and syntactically correct on all Vellum
   nodes in the affected site.

   -  This can have a ``servers`` line and a ``new_servers`` line - each
      line has the format
      ``<servers|new_servers>=<ip address>,<ip address>, ...``
   -  If the file isn't present, or is invalid, then make the
      configuration file contain all Vellum nodes in the site on the
      ``servers`` lines, and don't add a ``new_servers`` line.
   -  Otherwise, don't change the states of any nodes in the file (even
      if you know the node has failed).

-  If there is more than one failed node (and there is no remote site,
   or more than one failed node in the remote site) then there will be
   registration and call failures, and calls will be incorrectly billed
   (if using Ralf) until this process has been completed.

Vellum - Cassandra configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check that the Cassandra cluster is healthy by running the following on
a Vellum node:

::

    sudo /usr/share/clearwater/bin/run-in-signaling-namespace nodetool status

If the Cassandra cluster isn't healthy, you must fix this up before
continuing, and remove any failed nodes.

Sprout - JSON configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check the JSON configuration files on all Sprout nodes in the affected
site:

-  Verify that ``/etc/clearwater/enum.json`` file is correct, fixing it
   up if is not.
-  Verify that ``/etc/clearwater/s-cscf.json`` file is correct, fixing
   it up if is not.
-  Verify that ``/etc/clearwater/bgcf.json`` file is correct, fixing it
   up if is not.

Recreate the etcd cluster
~~~~~~~~~~~~~~~~~~~~~~~~~

-  On your selected master nodes, set ``etcd_cluster`` in
   ``/etc/clearwater/local_config`` to a comma separated list of the
   management IP addresses of your master nodes.
-  Start etcd on the master nodes

   -  Run ``sudo monit monitor -g etcd``
   -  Run ``sudo monit monitor -g clearwater_config_manager``
   -  Run ``sudo monit monitor -g clearwater_queue_manager``

-  This creates the etcd cluster, and synchronises the shared
   configuration. It doesn't recreate the data store cluster information
   in etcd yet.
-  Verify that the master nodes have formed a new etcd cluster
   successfully:

   -  Running ``sudo monit summary`` on each master node should show
      that the etcd processes are running successfully, except the
      ``clearwater_cluster_manager_process``
   -  Running ``sudo clearwater-etcdctl cluster-health`` (on a single
      master node) should show that the etcd cluster is healthy
   -  Running ``sudo clearwater-etcdctl member list`` should show that
      all the master nodes are members of the etcd cluster.

-  Verify that the configuration has successfully synchronized by
   running
   ``sudo /usr/share/clearwater/clearwater-config-manager/scripts/check_config_sync``

Add the rest of the nodes to the etcd cluster
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run this process on every node which is not one of the master nodes in
the affected site in turn. If all nodes in the site are master nodes,
you can skip this step.

-  Set ``etcd_proxy`` in ``/etc/clearwater/local_config`` to a comma
   separated list of the management IP addresses of your master nodes.
-  Start etcd on the node

   -  Run ``sudo monit monitor -g etcd``
   -  Run ``sudo monit monitor -g clearwater_config_manager``
   -  Run ``sudo monit monitor -g clearwater_queue_manager``

-  Verify that the node has contacted the etcd cluster successfully:

   -  Running ``sudo monit summary`` should show that the etcd processes
      are running successfully, except the
      ``clearwater_cluster_manager_process``

Recreate the data store cluster values in etcd
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run these commands on one Vellum node in the affected site:

::

    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_chronos_cluster vellum
    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_memcached_cluster vellum
    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_cassandra_cluster vellum

Verify the cluster state is correct in etcd by running sudo
``/usr/share/clearwater/clearwater-cluster-manager/scripts/check_cluster_state``

Start the cluster manager on all nodes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run this process on every node (including the master nodes) in the
affected site in turn.

-  Run ``sudo rm /etc/clearwater/no_cluster_manager``
-  Run ``sudo monit monitor -g clearwater_cluster_manager``
-  Verify that the cluster-manager comes back up by running
   ``sudo monit summary``.

Next steps
~~~~~~~~~~

Your deployment now has a working etcd cluster. You now need to:

-  Remove the failed nodes from the data store clusters for Chronos and
   Memcached (following
   http://clearwater.readthedocs.io/en/latest/Handling\_Failed\_Nodes.html#removing-a-node-from-a-data-store).
-  Recover redundancy by replacing the failed nodes.

