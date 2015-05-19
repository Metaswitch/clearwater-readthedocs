# Dealing with Failed Nodes

Nodes can be easily removed from a Clearwater deployment by following the instructions for [elastic scaling](Clearwater_Elastic_Scaling.md). When scaling down the remaining nodes are informed that a node is leaving and take appropriate action. However sometimes a node may fail unexpectedly. If this happens and the node cannot be recovered (for example the virtual machine has been deleted) the remaining nodes must be manually informed of the failure. This article explains how to do this.

## Removing a Failed Node

If a node permanently fails scaling the deployment up and down may stop working, or if a scaling operation is in progress it may get stuck (because other nodes in the tier will wait forever for the failed node to react). To recover from this situation the failed node should be removed from the deployment using the following steps:

* Remove the node from the underlying etcd cluster. To do this:
    * Run `clearwater-etcdctl cluster-health` and make a note of the ID of the failed node.
    * Run `clearwater-etcdctl member list` to check that the failed node reported is the one you were expecting (by looking at its IP address).
    * Run `clearwater-etcdctl member remove <ID>`, replacing `<ID>` with the ID learned above.
* Remove the failed node from any back-end data store clusters it was a part of (see Removing a Node From a Data Store).

## Multiple Failed Nodes

If your deployment loses half or more of its nodes permanently, it loses "quorum" which means that the underlying etcd cluster becomes read-only. This means that scaling up and down is not possible and changes to shared config cannot be made. It also means that the steps for removing a single failed node won't work. This section describes how to recover from this state.

In this example, your initial cluster consists of servers A, B, C, D, E and F. D, E and F die permanently, and A, B and C enter a read-only state (because they lack quorum). Recent changes may have been permanently lost at this point (if they were not replicated to the surviving nodes).

You should follow this process completely - the behaviour is unspecified if this process is started but not completed. It is always safe to restart this process from the beginning (for example, if you encounter an error partway through).

To recover from this state:

* stop etcd on A, B and C by running `sudo service clearwater-etcd stop`
* create a new cluster, only on A, by:
    * editing `etcd_cluster` in `/etc/clearwater/local_config` to just contain A's IP (e.g. `etcd_cluster=10.0.0.1`)
    * running `sudo service clearwater-etcd force-new-cluster`. This will warn that this is dangerous and should only be run during this process; choose to proceed.
    * running `clearwater-etcdctl member list` to check that the cluster only has A in
    * running `clearwater-etcdctl cluster-health` to check that the cluster is healthy
    * running `clearwater-etcdctl get ims_domain` to check that the data is safe
* get B to join that cluster by:
    * editing `etcd_cluster` in `/etc/clearwater/local_config` to just contain A's IP (e.g. `etcd_cluster=10.0.0.1`)
    * running `service clearwater-etcd force-decommission`. This will warn that this is dangerous and offer the chance to cancel; do not cancel.
    * running `service clearwater-etcd start`.
* get C to join that cluster by following the same steps as for B:
    * editing `etcd_cluster` in `/etc/clearwater/local_config` to just contain A's IP (e.g. `etcd_cluster=10.0.0.1`)
    * running `service clearwater-etcd force-decommission`. This will warn that this is dangerous and should only be run during this process; choose to proceed.
    * running `service clearwater-etcd start`.
* check that the cluster is now OK by doing the following on A:
    * running `clearwater-etcdctl member list` to check that the cluster now has A, B and C in
    * running `clearwater-etcdctl cluster-health` to check that the cluster is healthy
    * running `clearwater-etcdctl get ims_domain` to check that the data is safe
* log on to A. For each of D, E and F follow the instructions in Removing a Node From a Data Store.

## Removing a Node From a Data Store

The `mark_node_failed` script can be used to remove a failed node from a back-end data store. You will need to know the type of the failed node (e.g. "sprout") and its IP address. To remove the failed node log onto a working node in the deployment and run the following commands depending on the failed node's type.

### Sprout

    /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed "sprout" "memcached" <failed node IP>
    /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed "sprout" "chronos" <failed node IP>

### Homestead

    /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed "homestead" "cassandra" <failed node IP>

### Homer

    /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed "homer" "cassandra" <failed node IP>

### Ralf

    /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed "ralf" "chronos" <failed node IP>
    /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed "ralf" "memcached" <failed node IP>

### Memento

    /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed "ralf" "cassandra" <failed node IP>
    /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed "ralf" "memcached" <failed node IP>
