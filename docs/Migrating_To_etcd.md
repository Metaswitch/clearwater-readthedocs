# Migrating to Automatic Clustering and Configuration Sharing

Clearwater now supports a feature where new nodes can automatically join an existing deployment and learn their configuration from the existing nodes. This makes the deployment much easier to manage. However deployments created before the **TODO** release do not have this feature. This article explains how to migrate a deployment to take advantage of the new feature.

## Upgrade the Deployment

[Upgrade](Upgrading_a_Clearwater_deployment) to the latest stable Clearwater release.

## Prepare Configuration Files

Do the following on each node in turn:

1.  Run `TODO: AMC`. This examines the existing `/etc/clearwater/config` file and produces three new files:

    * `/etc/clearwater/local_config` which contains the settings only relevant to this node
    * `/etc/clearwater/shared_config` which contains the settings applicable to the deployment as a whole
    * A new `/etc/clearwater/config` that just references the two previous files

    Check each of these files by hand to make sure they look sensible.

2.  Edit `/etc/clearwater/local_config` to add a line `etcd_cluster="<NodeIPs>"` where `NodeIPs` is a comma separated list of the private IP addresses of nodes in the deployment. For example if your deployment contained nodes with IP addresses of 10.0.0.1 to 10.0.0.6, `NodeIPs` would be `10.0.0.1,10.0.0.2,10.0.0.3,10.0.0.4,10.0.0.5,10.0.0.6`

3.  Run `sudo touch /etc/clearwater/no_cluster_manager`. This temporarily disables the cluster manager so that you can program it with the current deployment topology.

## Install Clustering and Configuration Management Services

On each node run `sudo apt-get install clearwater-cluster-manager clearwater-config-manager`.

## Upload the Current Cluster Settings

Now you need to tell the cluster manager about the current topology of the various database clusters that exist in a Clearwater deployment. For each of the nodes types listed below, log onto *one* of the nodes of that type and run the specified commands.

### Sprout

    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_memcached_cluster sprout
    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_chronos_cluster sprout

### Ralf

    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_memcached_cluster ralf
    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_chronos_cluster ralf

### Homestead

    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_cassandra_cluster homestead

### Homer

    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_cassandra_cluster homer

### Memento

    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_memcached_cluster memento
    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_cassandra_cluster memento


## Upload the Shared Configuration

Run the following commands on *one* of your sprout nodes. This will upload the configuration that is shared across the deployment to etcd. If you add any new nodes to the deployment they will automatically learn this configuration from etcd.

* `/usr/share/clearwater/bin/upload_shared_config`
* `/usr/share/clearwater/bin/upload_s-cscf_config`
* `/usr/share/clearwater/bin/upload_bgcf_config`
* `/usr/share/clearwater/bin/upload_enum_config`

## Tidy Up

The final step is to re-enable the cluster manager by running the following commands:

    sudo rm /etc/clearwater/no_cluster_manager
    sudo service clearwater-cluster-manager restart
