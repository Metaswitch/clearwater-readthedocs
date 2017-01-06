## Dealing with Complete Site Failure

In a geographically redundant deployment, you may encounter the situation where
an entire site has permanently failed (e.g. because the location of that
geographic site has been physically destroyed). To recover from this situation:

* If the failed site contained half or more of your nodes, you have lost
  quorum in your etcd cluster. You should follow the ["removing multiple failed
  nodes"](Handling_Multiple_Failed_Nodes.md) instructions to
  rebuild the etcd cluster, containing only nodes from the surviving site.
* If the failed site contained fewer than half of your nodes, you have not lost
  quorum in your etcd cluster. You should follow the ["removing failed
  nodes"](Handling_Failed_Nodes.md) instructions to
  remove each failed node from the cluster.

After following the above instructions, you will have removed the nodes in the
failed site from etcd, but not from the Cassandra/Chronos/Memcached datastore
clusters. To do this, follow the ["Removing a Node From a Data
Store"](Handling_Failed_Nodes.md#removing-a-node-from-a-data-store)
instructions above for each failed node, using the `mark_remote_node_failed`
script instead of the `mark_node_failed` script.

You should now have a working single-site cluster, which can continue to run as
a single site, or be safely paired with a new remote site.

