# Clearwater Automatic Clustering and Configuration Sharing

Clearwater has a feature that allows nodes in a deployment to automatically form the correct clusters and share configuration with each other. This makes deployments much easier to manage. For example:

* It is easy to add new nodes to an existing deployment. The new nodes will automatically join the correct clusters according to their node type, without any loss of service. The nodes will also learn the majority of their config from the nodes already in the deployment.
* Similarly, removing nodes from a deployment is straightforward. The leaving nodes will leave their clusters without impacting service.
* It makes it much easier to modify configuration that is shared across all nodes in the deployment.

This features uses [etcd](https://github.com/coreos/etcd) as a decentralized data store, a `clearwater-cluster-manager` service to handle automatic clustering, and a `clearwater-config-manager` to handle configuration sharing.

### Etcd masters and proxies
Clearwater nodes can run either as an etcd master or an etcd proxy. When depoying a node, you can chose whether it acts as a master or proxy by filling in either the `etcd_cluster` or `etcd_proxy` config option in `/etc/clearwater/local_config` (see the [configuration options reference](Clearwater_Configuration_Options_Reference.md) for more details).

There are some restrictions on which nodes can be masters or proxies:
* There must always be at least 3 etcd masters in the cluster
* The first node to be deployed in a site must be an etcd master

The [automated](Automated_Install.md) and [manual](Manual_Install.md) install instructions will both create a deployment with all nodes running as etcd masters.
