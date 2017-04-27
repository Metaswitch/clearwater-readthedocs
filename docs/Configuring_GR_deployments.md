# Configuring Geographic redundancy

This article describes

* How to install a geographically redundant deployment
* How to add a site to your deployment
* How to remove a site from your deployment

More information about Clearwater's geographic redundancy support is available [here](http://clearwater.readthedocs.io/en/latest/docs/Geographic_redundancy.html), and how to recover a deployment after site failure is described [here](http://clearwater.readthedocs.io/en/latest/Handling_Site_Failure.html).

## Installing a geographically redundant deployment

The process for setting up a geographically-redundant deployment is as follows.

1. Create your first site, following the instructions [here](http://clearwater.readthedocs.io/en/latest/Manual_Install.html#create-the-per-node-configuration) - make sure you add the extra configuration options/Chronos configuration for GR and set up your DNS records following the extra GR instructions. At this point, you have a working non-GR deployment.
2. Then add your second site, again following the instructions [here](http://clearwater.readthedocs.io/en/latest/Manual_Install.html#create-the-per-node-configuration), and again making sure you add the extra configuration options/Chronos configuration/DNS records for GR.
3. And that's it! Your two sites are ready to handle calls and can replicate data between themselves.

You can also use Chef to try GR function, by setting `"gr" => true` in the environment, as described in [the automated install docs](Automated_Install.md).

## Adding a site to a non-GR deployment

Adding a site to a non-GR deployment follows the same basic process as described [above](). The first step is to convert your existing site to one that supports GR.

1. Update the DNS records
2. Update shared config
3. Update Chronos
4. Update cassandra

Now you can add a new site, following the instructions (from step 2) [above](). 

To revert this process, simply remove the new site, following the instructions [below]()

## Removing a site from a GR deployment

The process for removing a site is as follows.

1. Change DNS to no longer send any traffic to the removed site, and wait for the DNS TTL.
2. On your remaining site, change its configuration to no longer use the remote site (chronos, shared config, dns config).
3. Change Cassandra? TODO!!
4. Quiesce the main processes on each node
    * Bono - `monit unmonitor -g bono && sudo service bono quiesce` (note, this will take as long as your reregistration period)
    * Sprout or Memento- `monit unmonitor -g sprout && sudo service sprout quiesce`
    * Dime - `monit stop -g homestead && monit stop -g homestead-prov && monit stop -g ralf`
    * Homer - `monit stop -g homer`
    * Ellis - `monit stop -g ellis`
    * Vellum - `sudo monit unmonitor -g clearwater_cluster_manager && sudo service clearwater-cluster-manager decommission`
5. Permanently delete the nodes.

To revert this process, simply add the site back, following the instructions [above]()
