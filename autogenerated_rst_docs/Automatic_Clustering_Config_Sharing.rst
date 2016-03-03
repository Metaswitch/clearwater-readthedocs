Clearwater Automatic Clustering and Configuration Sharing
=========================================================

Clearwater has a feature that allows nodes in a deployment to
automatically form the correct clusters and share configuration with
each other. This makes deployments much easier to manage. For example:

-  It is easy to add new nodes to an existing deployment. The new nodes
   will automatically join the correct clusters according to their node
   type, without any loss of service. The nodes will also learn the
   majority of their config from the nodes already in the deployment.
-  Similarly, removing nodes from a deployment is straightforward. The
   leaving nodes will leave their clusters without impacting service.
-  It makes it much easier to modify configuration that is shared across
   all nodes in the deployment.

This features uses `etcd <https://github.com/coreos/etcd>`__ as a
decentralized data store, a ``clearwater-cluster-manager`` service to
handle automatic clustering, and a ``clearwater-config-manager`` to
handle configuration sharing.

Is my Deployment Using Automatic Clustering and Configuration Sharing?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To tell if your deployment is using this feature, log onto one of the
nodes in your deployment and run ``dpkg --list | grep clearwater-etcd``.
If this does not give any output the feature is not in use.

Migrating to Automatic Clustering and Configuration Sharing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Deployments that are not using the feature may be migrated so they start
using it. To perform this migration, follow these
`instructions <Migrating_To_etcd>`__.
