Backups
=======

Within a Clearwater deployment, ellis, homestead, homer and memento all
store persistent data. (Bono and sprout do not.) To prevent data loss in
disaster scenarios, ellis, homestead, homer and memento all have data
backup and restore mechanisms. Specifically, all support

-  manual backup
-  periodic automated local backup
-  manual restore.

This document describes

-  how to list the backups that have been taken
-  how to take a manual backup
-  the periodic automated local backup behavior
-  how to restore from a backup.

Note that if your Clearwater deployment is `integrated with an external
HSS <External_HSS_Integration.md>`__, the HSS is the master of ellis and
homestead's data, and those nodes do not need to be backed up. However,
homer's data still needs to be backed up.

Listing Backups
---------------

The process for listing backups varies between ellis and homestead,
homer and memento.

Ellis
~~~~~

To list the backups that have been taken on ellis, run
``sudo /usr/share/clearwater/ellis/backup/list_backups.sh``.

::

    Backups for ellis:
    1372294741  /usr/share/clearwater/ellis/backup/backups/1372294741
    1372294681  /usr/share/clearwater/ellis/backup/backups/1372294681
    1372294621  /usr/share/clearwater/ellis/backup/backups/1372294621
    1372294561  /usr/share/clearwater/ellis/backup/backups/1372294561

Homestead, Homer and Memento
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Homestead actually contains two databases (``homestead_provisioning``
and ``homestead_cache``) and these must be backed up together. This is
why there are two commands for each homestead operation. Homer and
memento only contain one database and so there is only one command for
each operation.

To list the backups that have been taken on homestead, homer or memento,
run

-  ``sudo /usr/share/clearwater/bin/run-in-signaling-namespace /usr/share/clearwater/bin/list_backups.sh homestead_provisioning``
   and
   ``sudo /usr/share/clearwater/bin/run-in-signaling-namespace /usr/share/clearwater/bin/list_backups.sh homestead_cache``
   for homestead
-  ``sudo /usr/share/clearwater/bin/run-in-signaling-namespace /usr/share/clearwater/bin/list_backups.sh homer``
   for homer
-  ``sudo /usr/share/clearwater/bin/run-in-signaling-namespace /usr/share/clearwater/bin/list_backups.sh memento``
   for memento.

This produces output of the following form, listing each of the
available backups.

::

    No backup directory specified, defaulting to /usr/share/clearwater/homestead/backup/backups
    provisioning1372812963174
    provisioning1372813022822
    provisioning1372813082506
    provisioning1372813143119

You can also specify a directory to search in for backups, e.g. for
homestead:

``sudo /usr/share/clearwater/bin/run-in-signaling-namespace /usr/share/clearwater/bin/list_backups.sh homestead_provisioning <backup dir>``

Taking a Manual Backup
----------------------

The process for taking a manual backup varies between ellis and
homestead, homer and memento. Note that in all cases,

-  the backup is stored locally and should be copied to a secure backup
   server to ensure resilience
-  this process only backs up a single local node, so the same process
   must be run on all nodes in a cluster to ensure a complete set of
   backups
-  these processes cause a small amount of extra load on the disk, so it
   is recommended not to perform this during periods of high load
-  only 4 backups are stored locally - when a fifth backup is taken, the
   oldest is deleted.

Ellis
~~~~~

To take a manual backup on ellis, run
``sudo /usr/share/clearwater/ellis/backup/do_backup.sh``.

This produces output of the following form, reporting the
successfully-created backup.

::

    Creating backup in /usr/share/clearwater/ellis/backup/backups/1372336317/db_backup.sql

Make a note of the snapshot directory (``1372336317`` in the example
above) - this will be referred to as ``<snapshot>`` below.

This file is only accessible by the root user. To copy it to the current
user's home directory, run

::

    snapshot=<snapshot>
    sudo bash -c 'cp /usr/share/clearwater/ellis/backup/backups/'$snapshot'/db_backup.sql ~'$USER' &&
                  chown '$USER.$USER' db_backup.sql'

This file can, and should, be copied off the ellis node to a secure
backup server.

Homestead, Homer and Memento
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To take a manual backup on homestead, homer or memento, run

-  ``sudo /usr/share/clearwater/bin/run-in-signaling-namespace /usr/share/clearwater/bin/do_backup.sh homestead_provisioning``
   and
   ``sudo /usr/share/clearwater/bin/run-in-signaling-namespace /usr/share/clearwater/bin/do_backup.sh homestead_cache``
   on homestead
-  ``sudo /usr/share/clearwater/bin/run-in-signaling-namespace /usr/share/clearwater/bin/do_backup.sh homer``
   on homer
-  ``sudo /usr/share/clearwater/bin/run-in-signaling-namespace /usr/share/clearwater/bin/do_backup.sh memento``
   on memento.

This produces output of the following form, reporting the
successfully-created backup.

::

    ...
    Deleting old backup: /usr/share/clearwater/homestead/backup/backups/1372812963174
    Creating backup for keyspace homestead_provisoning...
    Requested snapshot for: homestead_provisioning
    Snapshot directory: 1372850637124
    Backups can be found at: /usr/share/clearwater/homestead/backup/backups/provisioning/

Make a note of the snapshot directory - this will be referred to as
``<snapshot>`` below.

The backups are only stored locally - the resulting backup is stored in
``/usr/share/clearwater/homestead/backup/backups/provisioning/<snapshot>``

These should be copied off the node to a secure backup server. For
example, from a remote location execute
``scp -r ubuntu@<homestead node>:/usr/share/clearwater/homestead/backup/backups/provisioning/<snapshot> .``.

Periodic Automated Local Backups
--------------------------------

Ellis, homestead, homer and memento are all automatically configured to
take daily backups if you've installed them through chef, at midnight
local time every night.

If you want to turn this on, edit your crontab by running
``sudo crontab -e`` and add the following lines if not already present:

-  ``0 0 * * * /usr/share/clearwater/ellis/backup/do_backup.sh`` on
   ellis
-  ``0 0 * * * /usr/share/clearwater/bin/run-in-signaling-namespace /usr/share/clearwater/bin/do_backup.sh homestead_provisioning``
   and
   ``5 0 * * * /usr/share/clearwater/bin/run-in-signaling-namespace /usr/share/clearwater/bin/do_backup.sh homestead_cache``
   on homestead
-  ``0 0 * * * /usr/share/clearwater/bin/run-in-signaling-namespace /usr/share/clearwater/bin/do_backup.sh homer``
   on homer
-  ``0 0 * * * /usr/share/clearwater/bin/run-in-signaling-namespace /usr/share/clearwater/bin/do_backup.sh memento``
   on memento.

These backups are stored locally, in the same locations as they would be
generated for a manual backup.

Restoring from a Backup
-----------------------

There are three stages to restoring from a backup.

1. Copying the backup files to the correct location.
2. Running the restore backup script.
3. Synchronizing ellis, homestead, homer and memento's views of the
   system state.

**This process will impact service and overwrite data in your
database.**

Copying Backup Files
~~~~~~~~~~~~~~~~~~~~

The first step in restoring from a backup is getting the backup
files/directories into the correct locations on the ellis, homer,
homestead or memento node.

If you are restoring from a backup that was taken on the node on which
you are restoring (and haven't moved it), you can just move onto the
next step.

If not, create a directory on your system that you want to put your
backups into (we'll use ``~/backup`` in this example). Then copy the
backups there. For example, from a remote location that contains your
backup directory ``<snapshot>`` execute
``scp -r <snapshot> ubuntu@<homestead node>:backup/<snapshot>``.

On ellis, run the following commands.

::

    snapshot=<snapshot>
    sudo chown root.root db_backup.sql
    sudo mkdir -p /usr/share/clearwater/ellis/backup/backups/$snapshot
    sudo mv ~/backup/$snapshot/db_backup.sql /usr/share/clearwater/ellis/backup/backups/$snapshot

On homestead/homer/memento there is no need to further move the files as
the backup script takes a optional backup directory parameter.

Running the Restore Backup Script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To actually restore from the backup file, run

-  ``sudo /usr/share/clearwater/ellis/backup/restore_backup.sh <snapshot>``
   on ellis
-  ``sudo /usr/share/clearwater/bin/run-in-signaling-namespace /usr/share/clearwater/bin/restore_backup.sh homestead_provisioning <snapshot> <backup directory>``
   and
   ``sudo /usr/share/clearwater/bin/run-in-signaling-namespace /usr/share/clearwater/bin/restore_backup.sh homestead_cache <snapshot> <backup directory>``
   on homestead
-  ``sudo /usr/share/clearwater/bin/run-in-signaling-namespace /usr/share/clearwater/bin/restore_backup.sh homer <snapshot> <backup directory>``
   on homer
-  ``sudo /usr/share/clearwater/bin/run-in-signaling-namespace /usr/share/clearwater/bin/restore_backup.sh memento <snapshot> <backup directory>``
   on memento.

Ellis will produce output of the following form.

::

    Will attempt to backup from backup 1372336317
    Found backup directory 1372336317
    Restoring backup for ellis...
    --------------
    /*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */
    --------------

    ...

    --------------
    /*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */
    --------------

Homestead, homer or memento will produce output of the following form.

::

    Will attempt to backup from backup 1372336442947
    Will attempt to backup from directory /home/ubuntu/bkp_test/
    Found backup directory /home/ubuntu/bkp_test//1372336442947
    Restoring backup for keyspace homestead_provisioning...
    xss =  -ea -javaagent:/usr/share/cassandra/lib/jamm-0.2.5.jar -XX:+UseThreadPriorities -XX:ThreadPriorityPolicy=42 -Xm
    s826M -Xmx826M -Xmn100M -XX:+HeapDumpOnOutOfMemoryError -Xss180k
    Clearing commitlog...
    filter_criteria: Deleting old .db files...
    filter_criteria: Restoring from backup: 1372336442947
    private_ids: Deleting old .db files...
    private_ids: Restoring from backup: 1372336442947
    public_ids: Deleting old .db files...
    public_ids: Restoring from backup: 1372336442947
    sip_digests: Deleting old .db files...
    sip_digests: Restoring from backup: 1372336442947

At this point, this node has been restored.

Synchronization
~~~~~~~~~~~~~~~

It is possible (and likely) that when backups are taken on different
boxes the data will be out of sync, e.g. ellis will know about a
subscriber, but there will no digest in homestead. To restore the system
to a consistent state we have a synchronization tool within ellis, which
can be run over a deployment to get the databases in sync. To run, log
into an ellis box and execute:

::

    cd /usr/share/clearwater/ellis
    sudo env/bin/python src/metaswitch/ellis/tools/sync_databases.py

This will:

-  Run through all the lines on ellis that have an owner and verify that
   there is a private identity associated with the public identity
   stored in ellis. If successful, it will verify that a digest exists
   in homestead for that private identity. If either of these checks
   fail, the line is considered lost and is removed from ellis. If both
   checks pass, it will check that there is a valid IFC - if this is
   missing, it will be replaced with the default IFC.
-  Run through all the lines on ellis without an owner and make sure
   there is no orphaned data in homestead and homer, i.e. deleting the
   simservs, IFC and digest for those lines.

Shared Configuration
--------------------

In addition to the data stored in ellis, homer, homestead and memento, a
Clearwater deployment also has shared configuration that is
`automatically shared between
nodes <Automatic_Clustering_Config_Sharing.md>`__. This is stored in a
distributed database, and mirrored to files on the disk of each node.

Backing Up
~~~~~~~~~~

To backup the shared configuration:

-  If you are in the middle of `modifying shared
   config <Modifying_Clearwater_settings.md>`__, complete the process to
   apply the config change to all nodes.
-  Log onto one of the sprout nodes in the deployment.
-  Copy the following files to somewhere else for safe keeping (e.g.
   another directory on the node, or another node entirely).

   /etc/clearwater/shared\_config /etc/clearwater/bgcf.json
   /etc/clearwater/enum.json /etc/clearwater/s-cscf.json

Restoring Configuration
~~~~~~~~~~~~~~~~~~~~~~~

To restore a previous backup, copy the four files listed above to
``/etc/clearwater`` on one of your sprout nodes. Then run the following
commands on that node:

::

    /usr/share/clearwater/clearwater-config-manager/scripts/upload_shared_config
    /usr/share/clearwater/clearwater-config-manager/scripts/upload_bgcf_json
    /usr/share/clearwater/clearwater-config-manager/scripts/upload_enum_json
    /usr/share/clearwater/clearwater-config-manager/scripts/upload_scscf_json

