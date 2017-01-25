Dealing with Failed Nodes
=========================

Nodes can be easily removed from a Clearwater deployment by following
the instructions for `elastic
scaling <Clearwater_Elastic_Scaling.html>`__. When scaling down the
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
   part of (see `Removing a Node From a Data
   Store <http://clearwater.readthedocs.io/en/latest/Handling_Failed_Nodes.html#removing-a-node-from-a-data-store>`__
   below).

Removing a Node From a Data Store
---------------------------------

The ``cw-mark_node_failed`` script can be used to remove a failed node
from a back-end data store. If there are multiple failed nodes, ensure
that you run the ``cw-mark_node_failed`` scripts for each store type
simultaneously (e.g. for multiple sprout removal, mark all failed nodes
for memcached simultaneously first, and then mark all failed nodes for
chronos). The ``cw-mark_node_failed`` script will only terminate once
all of the failed nodes for that datastore have been marked as such, so
you can do this by running ``cw-mark_node_failed`` for each of that
datastore's failed nodes in a separate shell session.

You will need to know the type of the failed node (e.g. "sprout") and
its IP address. If you are using separate signaling and management
networks, you must use the signaling IP address of the failed node. To
remove the failed node log onto a working node in the same site and run
the following commands (depending on the failed node's type):

Sprout
~~~~~~

::

    sudo cw-mark_node_failed "sprout" "memcached" <failed node IP>
    sudo cw-mark_node_failed "sprout" "chronos" <failed node IP>

Homestead
~~~~~~~~~

::

    sudo cw-mark_node_failed "homestead" "cassandra" <failed node IP>

Homer
~~~~~

::

    sudo cw-mark_node_failed "homer" "cassandra" <failed node IP>

Ralf
~~~~

::

    sudo cw-mark_node_failed "ralf" "chronos" <failed node IP>
    sudo cw-mark_node_failed "ralf" "memcached" <failed node IP>

Memento
~~~~~~~

::

    sudo cw-mark_node_failed "memento" "cassandra" <failed node IP>
    sudo cw-mark_node_failed "memento" "memcached" <failed node IP>

If you cannot log into a working node in the same site (e.g. because an
entire geographically redundant site has been lost), you can use a
working node in the other site, but in this case you must run
``/usr/share/clearwater/clearwater-cluster-manager/scripts/mark_remote_node_failed``
instead of ``cw-mark_node_failed``.

Multiple Failed Nodes
---------------------

If your deployment loses half or more of its nodes permanently, it loses
"quorum" which means that the underlying etcd cluster becomes read-only.
Please follow the process described
`here <http://clearwater.readthedocs.io/en/latest/Handling_Multiple_Failed_Nodes.html>`__
for details of how to recover.

If you haven't lost half (or more) of your nodes, then you can use the
same process described
`above <http://clearwater.readthedocs.io/en/latest/Handling_Failed_Nodes.html#removing-a-failed-node>`__
for each of your failed nodes (remembering that you may need to run the
``cw-mark_node_failed`` script for each failed node simultaneously).
