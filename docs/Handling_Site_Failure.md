## Dealing with Complete Site Failure

In a geographically redundant deployment, you may encounter the situation where
an entire site has permanently failed (e.g. because the location of that
geographic site has been physically destroyed). To recover from this situation:

* If the failed site contained half or more of your nodes, you have lost
  quorum in your etcd cluster. You should follow the instructions [here](http://clearwater.readthedocs.io/en/latest/Handling_Multiple_Failed_Nodes.html) to rebuild the etcd cluster, containing only nodes from the surviving site.
* If the failed site contained fewer than half of your nodes, you have not lost
  quorum in your etcd cluster. You should follow the instructions [here](http://clearwater.readthedocs.io/en/latest/Handling_Failed_Nodes.html) to remove each failed node from the cluster.

You should now have a working single-site cluster, which can continue to run as
a single site, or be safely paired with a new remote site.
