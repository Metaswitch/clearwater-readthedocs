Dealing with Multiple Failed Nodes
----------------------------------

If your deployment loses half or more of its nodes permanently, it loses
"quorum" which means that the underlying etcd cluster becomes read-only.
While the etcd cluster is in this state, you can’t perform any scaling
operations, or change configuration and have it synced across the
deployment.

If you haven't lost half (or more) of your nodes, then you can use the
process described
`here <http://clearwater.readthedocs.io/en/latest/Handling_Failed_Nodes.html#removing-a-failed-node>`__
for each of your failed nodes.

Procedure
~~~~~~~~~

The procedure creates a new etcd cluster to replace the existing
cluster. The new cluster is populated with the configuration saved in
the configuration files on disk. This allows us to recreate the cluster,
even in cases when the existing cluster is too badly corrupted to read
from.

This procedure won’t impact service. You should follow this process
completely - the behaviour is unspecified if this process is started but
not completed. It is always safe to restart this process from the
beginning (for example, if you encounter an error partway through).

-  If your deployment doesn’t have any Ralf nodes, then you can safely
   ignore any steps relating to Ralf nodes below.
-  If your deployment doesn’t use GR, then you can safely ignore any
   steps relating to the remote site.

Stop the etcd processes
~~~~~~~~~~~~~~~~~~~~~~~

Stop the etcd processes on every node in every site.

-  Run ``sudo monit stop –g etcd``
-  Run ``sudo monit stop –g clearwater_cluster_manager``
-  Run ``sudo monit stop –g clearwater_config_manager``
-  Run ``sudo monit stop –g clearwater_queue_manager``
-  Run ``sudo touch /etc/clearwater/no_cluster_manager``
-  Run ``sudo rm –rf  /var/lib/clearwater-etcd/*``

Select your master nodes
~~~~~~~~~~~~~~~~~~~~~~~~

To follow this process you need to choose some nodes to be the new
founding members of the etcd cluster. You should select:

-  One Sprout node in each of your sites

   -  If there are no live Sprout nodes in any site, there is a complete
      service outage at this point. Continue with this process (missing
      out the Sprout steps) and then add new Sprout nodes once the etcd
      cluster is recovered.
   -  If there are no live Sprout nodes in one site, but a live Sprout
      node in the other site, then that’s fine, just use the live
      Sprout.

-  One Homestead node in any of your sites

   -  If there are no live Homestead nodes, then there is a complete
      service outage at this point. Continue with this process (missing
      out the Homestead steps) and then add new Homestead nodes once the
      etcd cluster is recovered.

-  One Ralf node in each of your sites

   -  If there are no live Ralf nodes in any site, then there is no
      offline billing for any calls at this point. Continue with this
      process (missing out the Ralf steps) and then add new Ralf nodes
      once the etcd cluster is recovered.
   -  If there are no live Ralf nodes in one site, but a live Ralf node
      in the other site, then that’s fine, just use the live Ralf. There
      is no offline billing for any calls made through the site with no
      live Ralfs at this point.

Check the configuration on your master nodes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The next step is to ensure that the configuration files on each node are
correct.

Any of the master nodes – Shared configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The shared configuration is at ``/etc/clearwater/shared_config``. Verify
that this is correct, then copy this file onto every other master node.
Some configuration in ``shared_config`` can be different between sites.
If your deployment has multiple sites, and you have live master nodes in
each site, make sure each node has the correct ``shared_config`` file
for its site. Please see the `configuration options
reference <http://clearwater.readthedocs.io/en/latest/Clearwater_Configuration_Options_Reference.html>`__
for more details.

Sprout – JSON configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check the JSON configuration files (on all Sprouts in your set of master
nodes).

-  Verify that ``/etc/clearwater/enum.json`` file is correct, fixing it
   up if is not.
-  Verify that ``/etc/clearwater/s-cscf.json`` file is correct, fixing
   it up if is not.
-  Verify that ``/etc/clearwater/bgcf.json`` file is correct, fixing it
   up if is not.

Sprout – Chronos
^^^^^^^^^^^^^^^^

The configuration file is at ``/etc/chronos/chronos_cluster.conf``.
Verify that this is present and syntactically correct (on all Sprouts in
your set of master nodes), following the format
`here <https://github.com/Metaswitch/chronos/blob/dev/doc/clustering.md#clustering-chronos>`__.

If the file isn’t present, or is it invalid, then make the configuration
file contain all Sprout nodes in the site as nodes. Otherwise, don’t
change the states of any nodes in the file (even if you know the node
has failed). Note, if there is more than one failed node then there will
be timer failures until this process has been completed. This could
prevent subscribers from receiving notifications when their
registrations/subscriptions expire.

Sprout – Memcached
^^^^^^^^^^^^^^^^^^

You only need to perform these checks on one Sprout node in the
deployment – you don’t need to do this on a Sprout node in each site.

Local site
''''''''''

-  The configuration file is at ``/etc/clearwater/cluster_settings``.
-  Verify that this is present and syntactically correct.

   -  This can have a ``servers`` line and a ``new_servers`` line – each
      line has the format
      ``<servers|new_servers>=<ip address>,<ip address>, …``
   -  If the file isn’t present, or is it invalid, then make the
      configuration file contain all Sprout nodes in the site on the
      ``servers`` lines, and don’t add a ``new_servers`` line.
   -  Otherwise, don’t change the states of any nodes in the file (even
      if you know the node has failed).

-  If there is more than one failed node (and there is no remote site,
   or more than one failed node in the remote site) then there will be
   registration and call failures until this process has been completed.

Remote site
'''''''''''

-  The configuration file is at
   ``/etc/clearwater/remote_cluster_settings``.
-  If this deployment is GR, but there are no live Sprouts in the remote
   site, then delete the configuration file.
-  Otherwise, verify that this is present and syntactically correct.

   -  It has the same format as the ``cluster_settings`` file.
   -  If the file isn’t present, or is it invalid, then make the
      configuration file contain all Sprout nodes in remote site on the
      ``servers`` lines, and don’t add a ``new_servers`` line.
   -  Otherwise, don’t change the states of any nodes in the file (even
      if you know the node has failed).

Ralf – Chronos
^^^^^^^^^^^^^^

The configuration file is at ``/etc/chronos/chronos_cluster.conf``.
Verify that this is present and syntactically correct (on all Ralfs in
your set of master nodes), following the format
`here <https://github.com/Metaswitch/chronos/blob/dev/doc/clustering.md#clustering-chronos>`__.

If the file isn’t present, or it is invalid, then make the configuration
file contain all Ralf nodes in the site as nodes. Otherwise, don’t
change the states of any nodes in the file (even if you know the node
has failed). Note, if there is more than one failed node then there will
be timer failures until this process has been completed. This will cause
some calls to be incorrectly billed (using offline billing).

Ralf – Memcached
^^^^^^^^^^^^^^^^

The configuration file is at ``/etc/clearwater/cluster_settings``.

Verify that this is present and syntactically correct (on all Ralfs in
your set of master nodes). This can have a ``servers`` line and a
``new_servers`` line – each line has the format
``<servers|new_servers>=<ip address>,<ip address>, …``.

If the file isn’t present, or is it invalid, then make the configuration
file contain all Ralf nodes in the site on the ``servers`` lines, and
don’t add a ``new_servers`` line. Otherwise, don’t change the states of
any nodes in the file (even if you know the node has failed).

If there is more than one failed node (and there is no remote site, or
more than one failed node in the remote site) then calls will be
incorrectly billed (using offline billing) until this process has been
completed.

Homestead - Cassandra
^^^^^^^^^^^^^^^^^^^^^

Check that the Cassandra cluster is healthy:

::

    sudo /usr/share/clearwater/bin/run-in-signaling-namespace nodetool status

If the Cassandra cluster isn’t healthy, you must fix this up before
continuing, and remove any failed nodes.

Recreate the etcd cluster
~~~~~~~~~~~~~~~~~~~~~~~~~

-  On your selected master nodes, set ``etcd_cluster`` in
   ``/etc/clearwater/local_config`` to a comma separated list of the
   management IP addresses of your master nodes.
-  Start etcd on the master nodes

   -  Run ``sudo monit monitor –g etcd``
   -  Run ``sudo monit monitor –g clearwater-cluster-manager``
   -  Run ``sudo monit monitor –g clearwater-config-manager``
   -  Run ``sudo monit monitor –g clearwater-queue-manager``

-  This creates the etcd cluster, and synchronises the shared
   configuration. It doesn’t recreate the data store cluster information
   in etcd yet.
-  Verify that the master nodes have formed a new etcd cluster
   successfully:

   -  Running ``sudo monit summary`` on each master node should show
      that the etcd processes are running successfully
   -  Running ``sudo clearwater-etcdctl cluster-health`` (on a single
      master node) should show that the etcd cluster is healthy
   -  Running ``sudo clearwater-etcdctl member list`` should show that
      all the master nodes are members of the etcd cluster.

-  Verify that the configuration has successfully synchronized by
   running
   ``sudo /usr/share/clearwater/clearwater-config-manager/scripts/check_config_sync``

Recreate the data store cluster values in etcd
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sprout
^^^^^^

Run this command on one Sprout node only – you don’t need to run this on
each site

::

    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_memcached_cluster sprout

Run this command on each Sprout node in your set of master nodes

::

    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_chronos_cluster sprout

Homestead
^^^^^^^^^

Run
``/usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_cassandra_cluster homestead``

Ralf
^^^^

Run these commands on each Ralf node in your set of master nodes

::

    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_memcached_cluster ralf
    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_chronos_cluster ralf

Verify the cluster state is correct in etcd by running sudo
``/usr/share/clearwater/clearwater-cluster-manager/scripts/check_cluster_state``

Add the rest of the nodes to the etcd cluster
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run this process on every node (except the master nodes) in your
deployment in turn.

-  Set ``etcd_cluster`` in ``/etc/clearwater/local_config`` to a comma
   separated list of the management IP addresses of your master nodes.
-  Start etcd on the node

   -  Run ``sudo monit monitor –g etcd``
   -  Run ``sudo monit monitor –g clearwater-cluster-manager``
   -  Run ``sudo monit monitor –g clearwater-config-manager``
   -  Run ``sudo monit monitor –g clearwater-queue-manager``

-  Verify that the node has joined the etcd cluster successfully:

   -  Running ``sudo monit summary`` should show that the etcd processes
      are running successfully
   -  Running ``sudo clearwater-etcdctl cluster-health`` should show
      that the etcd cluster is healthy
   -  Running ``sudo clearwater-etcdctl member list`` should show that
      the new node is a member of the etcd cluster.

Start the cluster manager on all nodes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run this process on every node (including the master nodes) in your
deployment in turn.

-  Run ``sudo rm /etc/clearwater/no_cluster_manager``
-  Run ``sudo service clearwater-cluster-manager stop``
-  Verify that the cluster-manager comes back up by running sudo monit
   summary.

Next steps
~~~~~~~~~~

Your deployment now has a working etcd cluster. You now need to:

-  Remove the failed nodes from the data store clusters for Chronos and
   Memcached (following
   http://clearwater.readthedocs.io/en/latest/Handling\_Failed\_Nodes.html#removing-a-node-from-a-data-store).
-  Recover redundancy by adding back the failed nodes.

