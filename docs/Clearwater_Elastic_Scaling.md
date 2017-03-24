# Elastic Scaling

The core Clearwater nodes have the ability to elastically scale; in other words, you can grow and shrink your deployment on demand, without disrupting calls or losing data.

This page explains how to use this elastic scaling function when using a deployment created through the [automated](Automated_Install.md) or [manual](Manual_Install.md) install processes.  Note that, although the instructions differ between the automated and manual processes, the underlying operations that will be performed on your deployment are the same - the automated process simply uses chef to drive this rather than issuing the commands manually.

## Before scaling your deployment

Before scaling up or down, you should decide how many Bono, Sprout, Dime, Vellum and Homer nodes you need (i.e. your target size). This should be based on your call load profile and measurements of current systems, though based on experience we recommend scaling up a tier of a given type (sprout, bono, etc.) when the average CPU utilization within that tier reaches ~60%.

## Performing the resize

### If you did an Automated Install

To resize your automated deployment, run:

    knife deployment resize -E <env> --bono-count <n> --sprout-count <n> --dime-count <n> --vellum-count <n> --homer-count <n>

Where the `<n>` values are how many nodes of each type you need.  Once this command has completed, the resize operation has completed and any nodes that are no longer needed will have been terminated.

More detailed documentation on the available Chef commands is available [here](https://github.com/Metaswitch/chef/blob/master/docs/knife_commands.md).

### If you did a Manual Install

Follow these instructions if you manually installed your deployment and are using Clearwater's [automatic clustering and configuration sharing](Automatic_Clustering_Config_Sharing.md) functionality.

If you're scaling up your deployment, follow the following process:

1.  Spin up new nodes, following the [standard install process](Manual_Install.md), but with the following modifications:

    * Set the `etcd_cluster` so that it only includes nodes that are already in the deployment and that are running as etcd masters (so it does not include any nodes being added).
    * Stop when you get to the "Provide Shared Configuration" step. The nodes will learn their configuration from the existing nodes.

2.  Wait until the new nodes have fully joined the existing deployment. To check if a node has joined the deployment:

    * (on Vellum nodes only) Run `cw-check_cluster_state`. This should report that the local node is in all of its clusters and that the cluster is stable.
    * Run `sudo cw-check_config_sync`. This reports when the node has learned its configuration.

3.  Update DNS to contain the new nodes.

If you're scaling down your deployment, follow the following process:

1.  Update DNS to contain only the nodes that will remain after the scale-down.
2.  On each node that is about to be turned down:

    * Run the appropriate command from the following (based on the node type) to stop processes from automatically restarting.
    
        *   Bono - `monit unmonitor -g bono`
        *   Sprout - `monit unmonitor -g sprout`
        *   Dime - `monit unmonitor -g homestead && monit unmonitor -g homestead-prov && monit unmonitor -g ralf`
        *   Vellum - n/a
        *   Homer - `monit unmonitor -g homer`
        *   Memento - `monit unmonitor -g sprout`        
        *   Ellis - n/a
        
    * Start the main processes quiescing.

        *   Bono - `sudo service bono quiesce`
        *   Sprout - `sudo service sprout quiesce`
        *   Dime - `sudo service homestead stop && sudo service homestead-prov stop && sudo service ralf stop`
        *   Vellum - n/a
        *   Homer - `sudo service homer stop`
        *   Memento - `sudo service sprout quiesce`
        *   Ellis - `sudo service ellis stop`

    * Unmonitor the clearwater management processes:

        *   (on Vellum nodes only) `sudo monit unmonitor -g clearwater_cluster_manager`
        *   `sudo monit unmonitor -g clearwater_config_manager`
        *   `sudo monit unmonitor -g clearwater_queue_manager`
        *   `sudo monit unmonitor -g etcd`

    * If the node you are turning down is a Vellum node, run `sudo service clearwater-etcd decommission`. This will cause the nodes to leave their existing clusters.

4.  Once the above steps have completed, turn down the nodes.

### If you did a Manual Install without Automatic Clustering

Follow these instructions if you manually installed your deployment but are *not* using Clearwater's [automatic clustering and configuration sharing](Automatic_Clustering_Config_Sharing.md) functionality.

If you're scaling up your deployment, follow the following process.

1.  Spin up new nodes, following the [standard install process](Manual_Install.md).
2.  If you are spinning up new Vellum nodes complete the following steps to add the new nodes to the storage clusters.
    * On all Vellum nodes, update `/etc/clearwater/cluster_settings` to contain both a list of the old nodes (`servers=...`) and a (longer) list of the new nodes (`new_servers=...`) and then run `service astaire reload` to re-read this file. 
    * On the new Vellum nodes follow the [instructions on the Cassandra website](http://www.datastax.com/documentation/cassandra/1.2/cassandra/operations/ops_add_node_to_cluster_t.html) to join the new nodes to the existing cluster.
    * On all Vellum nodes, update `/etc/chronos/chronos_cluster.conf` to contain a list of all the nodes (see [here](https://github.com/Metaswitch/chronos/blob/dev/doc/clustering.md) for details of how to do this) and then run `service chronos reload` to re-read this file.
    * On all Vellum nodes, run `service astaire reload` to start resynchronization.
    * On all Vellum nodes, run `service chronos resync` to start resynchronization of Chronos timers.
    * Update DNS to contain the new nodes.
    * On all Vellum nodes, wait until Astaire has resynchronized, either by running `service astaire wait-sync` or by polling over [SNMP](Clearwater_SNMP_Statistics.md).
    * On all Vellum nodes, wait until Chronos has resynchronized, either by running `service chronos wait-sync` or by polling over [SNMP](Clearwater_SNMP_Statistics.md).
    * On all Vellum nodes, update /etc/clearwater/cluster_settings to just contain the new list of nodes (`servers=...`) and then run `service <process> reload` to re-read this file.

If you're scaling down your deployment, follow the following process.

1.  Update DNS to contain the nodes that will remain after the scale-down.
2.  If you are removing Vellum nodes, complete the following steps to remove the nodes from the storage clusters.
    * On all Vellum nodes, update `/etc/clearwater/cluster_settings` to contain both a list of the old nodes (`servers=...`) and a (shorter) list of the new nodes (`new_servers=...`) and then run `service astaire reload` to re-read this file. 
    * On Vellum nodes that you are going to remove follow the [instructions on the Cassandra website](http://www.datastax.com/documentation/cassandra/1.2/cassandra/operations/ops_remove_node_t.html) to remove the leaving nodes from the cluster.
   * On all Vellum nodes, update `/etc/chronos/chronos_cluster.conf` to mark the nodes that are being scaled down as leaving (see [here](https://github.com/Metaswitch/chronos/blob/dev/doc/clustering.md) for details of how to do this) and then run `service chronos reload` to re-read this file.
   * On all Vellum nodes, run `service astaire reload` to start resynchronization.
   * On all Vellum nodes that will remain, run `service chronos resync` to start resynchronization of Chronos timers.
   * On all Vellum nodes, wait until Astaire has resynchronized, either by running `service astaire wait-sync` or by polling over [SNMP](Clearwater_SNMP_Statistics.md).
   * On all Vellum nodes, wait until Chronos has resynchronized, either by running `service chronos wait-sync` or by polling over [SNMP](Clearwater_SNMP_Statistics.md).
   * On all Vellum nodes, update /etc/clearwater/cluster_settings to just contain the new list of nodes (`servers=...`) and then run `service <process> reload` to re-read this file.
   * On all Vellum nodes that will remain, update `/etc/chronos/chronos_cluster.conf` so that it only contains entries for the staying nodes in the cluster and then run `service chronos reload` to re-read this file.
3. On each node that is about to be turned down:

   * Run the appropriate command from the following (based on the node type) to stop processes from automatically restarting.
    
        *   Bono - `monit unmonitor -g bono`
        *   Sprout - `monit unmonitor -g sprout`
        *   Dime - `monit unmonitor -g homestead && monit unmonitor -g homestead-prov && monit unmonitor -g ralf`
        *   Vellum - n/a
        *   Homer - `monit unmonitor -g homer`
        *   Memento - `monit unmonitor -g sprout`        
        *   Ellis - n/a
        
    * Start the main processes quiescing.

        *   Bono - `sudo service bono quiesce`
        *   Sprout - `sudo service sprout quiesce`
        *   Dime - `sudo service homestead stop && sudo service homestead-prov stop && sudo service ralf stop`
        *   Vellum - n/a
        *   Homer - `sudo service homer stop`
        *   Memento - `sudo service sprout quiesce`
        *   Ellis - `sudo service ellis stop`

12.  Turn down each of these nodes once the process has terminated.
