Migrating to Automatic Clustering and Configuration Sharing
===========================================================

Clearwater now supports an `automatic clustering and configuration
sharing <Automatic_Clustering_Config_Sharing>`__ feature. This makes
Clearwater deployments much easier to manage. However deployments
created before the 'For Whom The Bell Tolls' release do not use this
feature. This article explains how to migrate a deployment to take
advantage of the new feature.

Upgrade the Deployment
----------------------

`Upgrade <Upgrading_a_Clearwater_deployment>`__ to the latest stable
Clearwater release. You will also need to update your firewall settings
to support the new clearwater management packages; open port 2380 and
4000 between every node (see
`here <http://clearwater.readthedocs.org/en/stable/Clearwater_IP_Port_Usage/index.html>`__
for the complete list).

Verify Configuration Files
--------------------------

Do the following on each node in turn:

1. Run
   ``/usr/share/clearwater/infrastructure/migration-utils/configlint.py``.
   This examines the existing ``/etc/clearwater/config`` file and checks
   that the migration scripts can handle all the settings defined in it.

2. If ``configlint.py`` produces a warning about a config option, this
   can mean one of two things:

   -  The config option is invalid (for example, because there is a
      typo, or this option has been retired). Check the `configuration
      options
      reference <Clearwater_Configuration_Options_Reference.md>`__ for a
      list of valid options.
   -  The config option is valid, but the migration script doesn't
      recognise the option and won't automatically migrate it. In this
      case, you will need to make a note of this config option now, and
      add it back in after the rest of the migration has run. (A later
      step in this process covers that.)

Once you have checked your configuration file and taken a note of any
unrecognised settings, continue with the next step.

Prepare Local Configuration Files
---------------------------------

Do the following on each node in turn:

1. Run
   ``sudo /usr/share/clearwater/infrastructure/migration-utils/migrate_local_config /etc/clearwater/config``.
   This examines the existing ``/etc/clearwater/config`` file and
   produces a new ``/etc/clearwater/local_config`` which contains the
   settings only relevant to this node. Check that this file looks
   sensible.

2. Edit ``/etc/clearwater/local_config`` to add a line
   ``etcd_cluster="<NodeIPs>"`` where ``NodeIPs`` is a comma separated
   list of the private IP addresses of nodes in the deployment. For
   example if your deployment contained nodes with IP addresses of
   10.0.0.1 to 10.0.0.6, ``NodeIPs`` would be
   ``10.0.0.1,10.0.0.2,10.0.0.3,10.0.0.4,10.0.0.5,10.0.0.6``. If your
   deployment was GR, this should include the IP addresses of nodes in
   both sites.

3. If your deployment was geographically redundant, you should choose
   arbitrary names for each site (e.g. 'site1' and 'site2'), and set the
   ``local_site_name`` and ``remote_site_name`` settings in
   ``/etc/clearwater/local_config`` accordingly. For example, if the
   node is in 'site1', you should have ``local_site_name=site1`` and
   ``remote_site_name=site2``.

4. If the node is a Sprout or Ralf node, run
   ``sudo /usr/share/clearwater/bin/chronos_configuration_split.py``.
   This examines the existing ``/etc/chronos/chronos.conf`` file and
   extracts the clustering settings into a new file called
   ``/etc/chronos/chronos_cluster.conf``. Check each of these files by
   hand to make sure they look sensible. If the ``chronos_cluster.conf``
   file already exists, then the script will exit with a warning. In
   this case, please check the configuration files by hand, and either
   delete the ``chronos_cluster.conf`` file and re-run the script, or
   manually split the configuration yourself. Details of the expected
   configuration are
   `here <https://github.com/Metaswitch/chronos/blob/dev/doc/configuration.md>`__.

5. Run ``sudo touch /etc/clearwater/no_cluster_manager`` on all nodes.
   This temporarily disables the cluster manager (which is installed in
   the next step) so that you can program it with the current deployment
   topology.

Prepare Shared Configuration Files
----------------------------------

This step merges the config from all the nodes in your deployment into a
single config file that will be managed by etcd.

1. Log onto to one of the nodes in the deployment and create a temporary
   directory (e.g. ``~/config-migration``). Copy the
   ``/etc/clearwater/config`` file from each node in the deployment to
   this directory. Give each of these a name of the form
   ``<node>_orig_config``, e.g. ``sprout-1_orig_config``.

2. Run
   ``sudo /usr/share/clearwater/infrastructure/migration-utils/migrate_shared_config``,
   passing it all the config files in the temporary directory

   -  ``sudo /usr/share/clearwater/infrastructure/migration-utils/migrate_shared_config *_orig_config``

3. This will produce the file ``/etc/clearwater/shared_config``. Check
   the contents of this file looks sensible. If running
   ``configlint.py`` indicated that any configuration would not be
   automatically migrated, add that configuration to
   ``/etc/clearwater/shared_config`` now.

4. Copy this file to ``/etc/clearwater/shared_config`` on each node in
   the deployment.

5. On each node in turn:

   -  Run
      ``sudo /usr/share/clearwater/infrastructure/migration-utils/switch_to_migrated_config``
   -  Run ``sudo service clearwater-infrastructure restart`` to
      regenerate any dependant configuration files
   -  Restart the Clearwater services on the node.

Install Clustering and Configuration Management Services
--------------------------------------------------------

On each node run ``sudo apt-get install clearwater-management``.

Upload the Current Cluster Settings
-----------------------------------

Now you need to tell the cluster manager about the current topology of
the various database clusters that exist in a Clearwater deployment. For
each of the nodes types listed below, log onto *one* of the nodes of
that type and run the specified commands.

Sprout
~~~~~~

::

    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_memcached_cluster sprout
    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_chronos_cluster sprout

Ralf
~~~~

::

    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_memcached_cluster ralf
    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_chronos_cluster ralf

Homestead
~~~~~~~~~

::

    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_cassandra_cluster homestead

Homer
~~~~~

::

    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_cassandra_cluster homer

Memento
~~~~~~~

::

    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_memcached_cluster memento
    /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_cassandra_cluster memento

Upload the Shared Configuration
-------------------------------

Run the following commands on *one* of your Sprout nodes. This will
upload the configuration that is shared across the deployment to etcd.
If you add any new nodes to the deployment they will automatically learn
this configuration from etcd.

-  ``sudo /usr/share/clearwater/clearwater-config-manager/scripts/upload_shared_config``
-  ``sudo /usr/share/clearwater/clearwater-config-manager/scripts/upload_scscf_json``
-  ``sudo /usr/share/clearwater/clearwater-config-manager/scripts/upload_bgcf_json``
-  ``sudo /usr/share/clearwater/clearwater-config-manager/scripts/upload_enum_json``

Tidy Up
-------

The final step is to re-enable the cluster manager by running the
following commands:

::

    sudo rm /etc/clearwater/no_cluster_manager

