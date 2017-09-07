Configuring Geographic redundancy
=================================

This article describes

-  How to install a geographically redundant deployment
-  How to add a site to your deployment
-  How to remove a site from your deployment

More information about Clearwater's geographic redundancy support is
available
`here <http://clearwater.readthedocs.io/en/latest/docs/Geographic_redundancy.html>`__,
and how to recover a deployment after site failure is described
`here <http://clearwater.readthedocs.io/en/latest/Handling_Site_Failure.html>`__.

Installing a geographically redundant deployment
------------------------------------------------

The process for setting up a geographically-redundant deployment is as
follows.

1. Create your first site, following the instructions
   `here <http://clearwater.readthedocs.io/en/latest/Manual_Install.html>`__
   - make sure you add the extra configuration options/Chronos
   configuration for GR and set up your DNS records following the extra
   GR instructions. At this point, you have a working non-GR deployment.
2. Then add your second site, again following the instructions
   `here <http://clearwater.readthedocs.io/en/latest/Manual_Install.html>`__,
   and again making sure you add the extra configuration options/Chronos
   configuration/DNS records for GR.
3. And that's it! Your two sites are ready to handle calls and can
   replicate data between themselves.

You can also use Chef to try GR function, by setting
``"num_gr_sites" => 2`` in the environment, as described in `the
automated install docs <Automated_Install.html>`__.

Adding a site to a non-GR deployment
------------------------------------

Adding a site to a non-GR deployment follows the same basic process as
described
`above <http://clearwater.readthedocs.io/en/latest/Configuring_GR_Deployments.html#installing-a-geographically-redundant-deployment>`__.
At various points in the steps below the instructions as for the site
name; this is either the value of ``local_site_name`` in
``/etc/clearwater/local_config`` if it was set when the site was first
created, or it's ``site1``.

1. Add your second site, following the instructions
   `here <http://clearwater.readthedocs.io/en/latest/Manual_Install.html>`__
   - make sure you add the extra configuration options/Chronos
   configuration for GR and set up your DNS records following the extra
   GR instructions. At this point, your second site is clustered with
   your first site, but no traffic is being sent to it.
2. Now you need to update the shared configuration on your first site so
   that it will communicate with your second site

   -  Update the shared configuration on your first site to use the GR
      options - follow the GR parts of setting up shared config
      `here <http://clearwater.readthedocs.io/en/latest/Manual_Install.html#provide-shared-configuration>`__.
   -  Update the Chronos configuration on your Vellum nodes on your
      first site to add the GR configuration file - instructions
      `here <http://clearwater.readthedocs.io/en/latest/Manual_Install.html#chronos-configuration>`__.
   -  If you are using any of Homestead-Prov, Homer or Memento:

      -  Update Cassandra's strategy by running
         ``cw-update_cassandra_strategy`` on any Vellum node in your
         entire deployment.

   -  At this point, your first and second sites are replicating data
      between themselves, but no external traffic is going to your
      second site.

3. Change DNS so that your external nodes (e.g. the HSS, the P-CSCF)
   will send traffic to your new site. Now you have a GR deployment.

To revert this process, simply remove the new site, following the
instructions
`below <http://clearwater.readthedocs.io/en/latest/Configuring_GR_Deployments.html#removing-a-site-from-a-gr-deployment>`__.

Removing a site from a GR deployment
------------------------------------

The process for removing a site is as follows.

1. Change DNS so that no external nodes (e.g. the HSS, the P-CSCF) send
   any traffic to the site you're removing, and wait for the DNS TTL to
   pass. At this point your two sites are still replicating data between
   themselves, but the site you're removing isn't getting any external
   traffic.
2. Now you need to update the shared configuration on the site you're
   keeping so that it no longer replicates data to the site you're
   removing.

   -  Update the Chronos configuration on your Vellum nodes on the
      remaining site to remove the GR configuration file - instructions
      `here <http://clearwater.readthedocs.io/en/latest/Manual_Install.html#chronos-configuration>`__.
   -  Update the shared configuration on your remaining site to remove
      the GR options - e.g. revert the GR parts of setting up shared
      config
      `here <http://clearwater.readthedocs.io/en/latest/Manual_Install.html#provide-shared-configuration>`__.
   -  At this point, your remaining site is handling all the external
      traffic, and isn't replicating any data to the site you're
      removing.

3. Now you can remove the site. Firstly, quiesce the main processes on
   each node in the site you're removing.

   -  Bono - ``monit unmonitor -g bono && sudo service bono quiesce``
      (note, this will take as long as your reregistration period)
   -  Sprout or Memento-
      ``monit unmonitor -g sprout && sudo service sprout quiesce``
   -  Dime -
      ``monit stop -g homestead && monit stop -g homestead-prov && monit stop -g ralf``
   -  Homer - ``monit stop -g homer``
   -  Ellis - ``monit stop -g ellis``
   -  Vellum -
      ``sudo monit unmonitor -g clearwater_cluster_manager && sudo service clearwater-cluster-manager decommission``

4. Once this is complete, you can permanently delete the nodes.

To revert this process, simply add the site back, following the
instructions
`above <http://clearwater.readthedocs.io/en/latest/Configuring_GR_Deployments.html#adding-a-site-to-a-non-gr-deployment>`__
