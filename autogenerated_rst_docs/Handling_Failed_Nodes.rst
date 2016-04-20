Dealing with Failed Nodes
=========================

Nodes can be easily removed from a Clearwater deployment by following
the instructions for `elastic
scaling <Clearwater_Elastic_Scaling.md>`__. When scaling down the
remaining nodes are informed that a node is leaving and take appropriate
action. However sometimes a node may fail unexpectedly. If this happens
and the node cannot be recovered (for example the virtual machine has
been deleted) the remaining nodes must be manually informed of the
failure. This article explains how to do this.

The processes described in the document do not affect call processing
and can be run on a system handling call traffic.

Removing a Failed Node
----------------------

If a node permanently fails scaling the deployment up and down may stop
working, or if a scaling operation is in progress it may get stuck
(because other nodes in the tier will wait forever for the failed node
to react). To recover from this situation the failed node should be
removed from the deployment using the following steps:

-  Remove the node from the underlying etcd cluster. To do this:

   -  Run ``clearwater-etcdctl cluster-health`` and make a note of the
      ID of the failed node.
   -  Run ``clearwater-etcdctl member list`` to check that the failed
      node reported is the one you were expecting (by looking at its IP
      address).
   -  Run ``clearwater-etcdctl member remove <ID>``, replacing ``<ID>``
      with the ID learned above.

-  Remove the failed node from any back-end data store clusters it was a
   part of (see Removing a Node From a Data Store).

Multiple Failed Nodes
---------------------

If your deployment loses half or more of its nodes permanently, it loses
"quorum" which means that the underlying etcd cluster becomes read-only.
This means that scaling up and down is not possible and changes to
shared config cannot be made. It also means that the steps for removing
a single failed node won't work. This section describes how to recover
from this state.

In this example, your initial cluster consists of servers A, B, C, D, E
and F. D, E and F die permanently, and A, B and C enter a read-only
state (because they lack quorum). Recent changes may have been
permanently lost at this point (if they were not replicated to the
surviving nodes).

You should follow this process completely - the behaviour is unspecified
if this process is started but not completed. It is always safe to
restart this process from the beginning (for example, if you encounter
an error partway through).

To recover from this state:

-  stop etcd on A, B and C by running ``sudo monit stop -g etcd``
-  create a new cluster, only on A, by:

   -  editing ``etcd_cluster`` in ``/etc/clearwater/local_config`` to
      just contain A's IP (e.g. ``etcd_cluster=10.0.0.1``)
   -  running ``sudo service clearwater-etcd force-new-cluster``. This
      will warn that this is dangerous and should only be run during
      this process; choose to proceed.
   -  running ``clearwater-etcdctl member list`` to check that the
      cluster only has A in
   -  running ``clearwater-etcdctl cluster-health`` to check that the
      cluster is healthy
   -  running ``clearwater-etcdctl get configuration/shared_config`` to
      check that the data is safe.
   -  running ``sudo monit monitor -g etcd`` to put etcd back under
      monit control

-  get B to join that cluster by:

   -  editing ``etcd_cluster`` in ``/etc/clearwater/local_config`` to
      just contain A's IP (e.g. ``etcd_cluster=10.0.0.1``)
   -  running ``sudo service clearwater-etcd force-decommission``. This
      will warn that this is dangerous and offer the chance to cancel;
      do not cancel.
   -  running ``sudo monit monitor -g etcd``.

-  get C to join that cluster by following the same steps as for B:

   -  editing ``etcd_cluster`` in ``/etc/clearwater/local_config`` to
      just contain A's IP (e.g. ``etcd_cluster=10.0.0.1``)
   -  running ``sudo service clearwater-etcd force-decommission``. This
      will warn that this is dangerous and should only be run during
      this process; choose to proceed.
   -  running ``sudo monit monitor -g etcd``.

-  check that the cluster is now OK by doing the following on A:

   -  running ``clearwater-etcdctl member list`` to check that the
      cluster now has A, B and C in
   -  running ``clearwater-etcdctl cluster-health`` to check that the
      cluster is healthy
   -  running
      ``clearwater-etcdctl get clearwater/<site_name>/configuration/shared_config``
      to check that the data is safe. The ``site_name`` is set in
      ```local_config`` <http://clearwater.readthedocs.org/en/stable/Manual_Install/index.html#create-the-per-node-configuration>`__
      if the deployment is `geographically
      redundant <http://clearwater.readthedocs.org/en/stable/Geographic_redundancy/index.html>`__,
      and defaults to ``site1`` if unset.

-  log on to A. For each of D, E and F follow the instructions in
   Removing a Node From a Data Store.

Removing a Node From a Data Store
---------------------------------

The ``mark_node_failed`` script can be used to remove a failed node from
a back-end data store. You will need to know the type of the failed node
(e.g. "sprout") and its IP address. To remove the failed node log onto a
working node in the same site and run the following commands (depending
on the failed node's type). If you are removing multiple nodes
simultaneously, ensure that you run the ``mark_node_failed`` scripts for
each store type simultaneously (e.g. for multiple sprout removal, mark
all failed nodes for memcached simultaneously first, and then mark all
failed nodes for chronos).

If you cannot log into a working node in the same site (e.g. because an
entire geographically redundant site has been lost), you can use a
working node in the other site, but in this case you must run
``/usr/share/clearwater/clearwater-cluster-manager/scripts/mark_remote_node_failed``
instead of
``/usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed``.

If you are using separate signaling and management networks, you must
use the signaling IP address of the failed node as the failed node IP in
the commands below.

Sprout
~~~~~~

::

    sudo /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed "sprout" "memcached" <failed node IP>
    sudo /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed "sprout" "chronos" <failed node IP>

Homestead
~~~~~~~~~

::

    sudo /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed "homestead" "cassandra" <failed node IP>

Homer
~~~~~

::

    sudo /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed "homer" "cassandra" <failed node IP>

Ralf
~~~~

::

    sudo /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed "ralf" "chronos" <failed node IP>
    sudo /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed "ralf" "memcached" <failed node IP>

Memento
~~~~~~~

::

    sudo /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed "memento" "cassandra" <failed node IP>
    sudo /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed "memento" "memcached" <failed node IP>

Complete Site Failure
---------------------

In a geographically redundant deployment, you may encounter the
situation where an entire site has permanently failed (e.g. because the
location of that geographic site has been physically destroyed). To
recover from this situation:

-  If the failed site contained half or more of your nodes, you have
   lost quorum in your etcd cluster. You should follow the `"Multiple
   Failed Nodes" <Handling_Failed_Nodes.md#multiple-failed-nodes>`__
   instructions above to rebuild the etcd cluster, containing only nodes
   from the surviving site.
-  If the failed site contained fewer than half of your nodes, you have
   not lost quorum in your etcd cluster. You should follow the
   `"Removing a Failed
   Node" <Handling_Failed_Nodes.md#removing-a-failed-node>`__
   instructions above to remove each failed node from the cluster.

After following the above instructions, you will have removed the nodes
in the failed site from etcd, but not from the
Cassandra/Chronos/Memcached datastore clusters. To do this, follow the
`"Removing a Node From a Data
Store" <Handling_Failed_Nodes.md#removing-a-node-from-a-data-store>`__
instructions above for each failed node, using the
``mark_remote_node_failed`` script instead of the ``mark_node_failed``
script.

You should now have a working single-site cluster, which can continue to
run as a single site, or be safely paired with a new remote site.
