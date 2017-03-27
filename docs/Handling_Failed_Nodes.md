# Dealing with Failed Nodes

Nodes can be easily removed from a Clearwater deployment by following the instructions for [elastic scaling](Clearwater_Elastic_Scaling.md).  However sometimes a node or nodes may fail unexpectedly.   If the nodes cannot be recovered, then you should do the following (in the order specified).
* If one or more nodes have failed that were acting as etcd masters (see [configuration](Clearwater_Configuration_Options_Reference.md)) and as a result you have lost 50% (or more) of your etcd master nodes in any one site then the etcd cluster for that site will have lost "quorum" and have become read-only.  To recover the etcd cluster you will need to follow the process [here](Handling_Multiple_Failed_Nodes.md).
* If one or more nodes have failed that were acting as etcd masters but *more* than half of your etcd cluster remains operational then you must first follow the steps below: “removing a failed node from an etcd cluster”
* If a Vellum node has failed then you should follow the instructions below: “removing a failed Vellum node from the data store clusters”
* You can now spin up a new node to replace the lost capacity.   If you are replacing a node that had been acting as an etcd master then you should typically configure the new node to also be an etcd master in order to retain your original etcd cluster size.

The processes described below do not affect call processing and can be run on a system handling call traffic.

## Removing a failed node from an etcd cluster

If a node fails that was acting as an etcd master then it must be manually removed from the site’s etcd cluster.   Failure to do so may leave the site in a state where future scaling operations do not work, or where in-progress scaling operations fail to complete.

This process assumes that more than half of the site’s etcd cluster is still healthy and so the etcd cluster still has quorum.   If 50% or more of the etcd masters in a given site have failed then you will need to first follow the process [here](Handling_Multiple_Failed_Nodes.md). 

For each failed node, log into a healthy etcd master in the same site as the failed node and run the following steps.
* Run `clearwater-etcdctl cluster-health` and make a note of the ID of the failed node.
* Run `clearwater-etcdctl member list` to check that the failed node reported is the one you were expecting (by looking at its IP address).
* Run `clearwater-etcdctl member remove <ID>`, replacing `<ID>` with the ID learned above.

## Removing a failed Vellum node from the data store clusters

If one or more Vellum nodes fail then they will need to be removed from all of the data store clusters that they were part of.   You will need to know the IP addresses of the failed nodes and if you are using separate signaling and management networks, you must use the signaling IP addresses.

For each site that contains one or more failed Vellum nodes, log onto a healthy Vellum node in the site and run the following commands.  If the site contains multiple failed nodes then you will need to run each command for all failed nodes in the site before moving on to the next command, and each command will block until you have run it for all of the failed nodes in a site so you will need to open a separate shell session for each node that has failed.

* `sudo cw-mark_node_failed "vellum" "memcached" <failed node IP>`
* `sudo cw-mark_node_failed "vellum" "chronos" <failed node IP>`
* `sudo cw-mark_node_failed "vellum" "cassandra" <failed node IP>`

