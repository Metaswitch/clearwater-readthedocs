# Configuring Geographic redundancy

This article describes

* How to install a geographically redundant deployment
* How to add a site to your deployment
* How to remove a site from your deployment

More information about Clearwater's geographic redundancy support is available [here](http://clearwater.readthedocs.io/en/latest/docs/Geographic_redundancy.html), and how to recover a deployment after site failure is described [here](http://clearwater.readthedocs.io/en/latest/Handling_Site_Failure.html).

## Installing a geographically redundant deployment

The process for setting up a geographically-redundant deployment is as follows.

1. Create your first site, following the instructions [here](http://clearwater.readthedocs.io/en/latest/Manual_Install.html) - make sure you add the extra configuration options/Chronos configuration for GR and set up your DNS records following the extra GR instructions. At this point, you have a working non-GR deployment.
2. Then add your second site, again following the instructions [here](http://clearwater.readthedocs.io/en/latest/Manual_Install.html), and again making sure you add the extra configuration options/Chronos configuration/DNS records for GR.
3. And that's it! Your two sites are ready to handle calls and can replicate data between themselves.

You can also use Chef to try GR function, by setting `"gr" => true` in the environment, as described in [the automated install docs](Automated_Install.md).

## Adding a site to a non-GR deployment

Adding a site to a non-GR deployment follows the same basic process as described [above](http://clearwater.readthedocs.io/en/latest/Configuring_GR_Deployments.html#installing-a-geographically-redundant-deployment). The first step is to convert your existing site to one that supports GR. At various points in the steps below the instructions as for the site name; this is either the value of `local_site_name` in `/etc/clearwater/local_config` if it was set when the site was first created, or it's `site1`.

1. Add the per-site DNS records needed for GR deployments - instructions [here](Clearwater_DNS_Usage.md) and [here](http://clearwater.readthedocs.io/en/latest/Manual_Install.html#dns-records). Wait for the TTL of your DNS records to pass.
2. Update the shared configuration to use the GR options - follow the GR parts of setting up shared config [here](http://clearwater.readthedocs.io/en/latest/Manual_Install.html#provide-shared-configuration). Wait for the maximum registration time of your subscribers to pass.
3. Update the Chronos configuration on your Vellum nodes to add the GR configuration file - instructions [here]((http://clearwater.readthedocs.io/en/latest/Manual_Install.html#chronos-configuration).
4. Update Cassandra's strategy by running `cw-update_cassandra_strategy`.

Now you can add a new site, following the instructions (from step 2) [above](http://clearwater.readthedocs.io/en/latest/Configuring_GR_Deployments.html#installing-a-geographically-redundant-deployment).

To revert this process, simply remove the new site, following the instructions [below](http://clearwater.readthedocs.io/en/latest/Configuring_GR_Deployments.html#removing-a-site-from-a-gr-deployment).

## Removing a site from a GR deployment

The process for removing a site is as follows.

1. Change DNS so that no external nodes (e.g. the HSS, the P-CSCF) send any traffic to the site to remove, and wait for the DNS TTL to pass.
3. On your remaining site, update the shared configuration to remove the GR options - revert the GR parts of setting up shared config [here](http://clearwater.readthedocs.io/en/latest/Manual_Install.html#provide-shared-configuration). Wait for the maximum registration time of your subscribers to pass. There's no need to remove the `site_name` value from shared configuration options though, and no need to change the DNS records.
3. Update the Chronos configuration on your Vellum nodes on the remaining site to remove the GR configuration file - instructions [here]((http://clearwater.readthedocs.io/en/latest/Manual_Install.html#chronos-configuration).
4. Remove the Vellum nodes from the Cassandra cluster by running `cw-remove_site_from_cassandra <site_name>`, where the `site_name` is the `local_site_name` of the removed site. Update Cassandra's strategy by running `cw-update_cassandra_strategy`.
5. Quiesce the main processes on each node
    * Bono - `monit unmonitor -g bono && sudo service bono quiesce` (note, this will take as long as your reregistration period)
    * Sprout or Memento- `monit unmonitor -g sprout && sudo service sprout quiesce`
    * Dime - `monit stop -g homestead && monit stop -g homestead-prov && monit stop -g ralf`
    * Homer - `monit stop -g homer`
    * Ellis - `monit stop -g ellis`
    * Vellum - `sudo monit unmonitor -g clearwater_cluster_manager && sudo service clearwater-cluster-manager decommission`
6. Permanently delete the nodes.

To revert this process, simply add the site back, following the instructions [above](http://clearwater.readthedocs.io/en/latest/Configuring_GR_Deployments.html#adding-a-site-to-a-non-gr-deployment)
