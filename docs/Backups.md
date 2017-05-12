# Backups

Within a Clearwater deployment, Ellis and Vellum store persistent data (Bono, Sprout, Homer and Dime do not). To prevent data loss in disaster scenarios, Ellis and Vellum have data backup and restore mechanisms.  Specifically, they support

*   manual backup
*   periodic automated local backup
*   manual restore.

This document describes

*   how to list the backups that have been taken
*   how to take a manual backup
*   the periodic automated local backup behavior
*   how to restore from a backup.

Note that Vellum has 4 databases:
* `homestead_provisioning` and `homestead_cache` for Homestead's data
* `homer` for Homer's data
* `memento` for Memento's data (if using the Memento AS)

Depending on your deployment scenario, you may not need to back up all of the data of Ellis and Vellum:
* If your Clearwater deployment is [integrated with an external HSS](External_HSS_Integration.md), the HSS is the master of Ellis' and some of Vellum's data, so you only need to backup/restore data in the `homer` and `memento` databases on Vellum
* If you are not using a Memento AS, you do not need to backup/restore the `memento` database on Vellum

## Listing Backups

The process for listing backups differs between Ellis and Vellum.

### Ellis

To list the backups that have been taken on Ellis, run `sudo /usr/share/clearwater/ellis/backup/list_backups.sh`.

    Backups for ellis:
    1372294741  /usr/share/clearwater/ellis/backup/backups/1372294741
    1372294681  /usr/share/clearwater/ellis/backup/backups/1372294681
    1372294621  /usr/share/clearwater/ellis/backup/backups/1372294621
    1372294561  /usr/share/clearwater/ellis/backup/backups/1372294561

### Vellum

To list the backups that have been taken on Vellum, run

*   `sudo /usr/share/clearwater/bin/list_backups.sh homestead_provisioning`
*   `sudo /usr/share/clearwater/bin/list_backups.sh homestead_cache`
*   `sudo /usr/share/clearwater/bin/list_backups.sh homer`
*   `sudo /usr/share/clearwater/bin/list_backups.sh memento`

This produces output of the following form, listing each of the available backups.

    No backup directory specified, defaulting to /usr/share/clearwater/homestead/backup/backups
    provisioning1372812963174
    provisioning1372813022822
    provisioning1372813082506
    provisioning1372813143119

You can also specify a directory to search in for backups, e.g. for `homestead_provisioning`:

`sudo /usr/share/clearwater/bin/list_backups.sh homestead_provisioning <backup dir>`

## Taking a Manual Backup

The process for taking a manual backup differs between Ellis and Vellum.  Note that in both cases,

*   the backup is stored locally and should be copied to a secure backup server to ensure resilience
*   this process only backs up a single local node, so the same process must be run on all nodes in a cluster to ensure a complete set of backups
*   these processes cause a small amount of extra load on the disk, so it is recommended not to perform this during periods of high load
*   only 4 backups are stored locally - when a fifth backup is taken, the oldest is deleted.

### Ellis

To take a manual backup on Ellis, run `sudo /usr/share/clearwater/ellis/backup/do_backup.sh`.

This produces output of the following form, reporting the successfully-created backup.

    Creating backup in /usr/share/clearwater/ellis/backup/backups/1372336317/db_backup.sql

Make a note of the snapshot directory (`1372336317` in the example above) - this will be referred to as `<snapshot>` below.

This file is only accessible by the root user.  To copy it to the current user's home directory, run

    snapshot=<snapshot>
    sudo bash -c 'cp /usr/share/clearwater/ellis/backup/backups/'$snapshot'/db_backup.sql ~'$USER' &&
                  chown '$USER.$USER' db_backup.sql'

This file can, and should, be copied off the Ellis node to a secure backup server.

### Vellum

To take a manual backup on Vellum, run

*   `sudo cw-run_in_signaling_namespace /usr/share/clearwater/bin/do_backup.sh homestead_provisioning`
*   `sudo cw-run_in_signaling_namespace /usr/share/clearwater/bin/do_backup.sh homestead_cache`
*   `sudo cw-run_in_signaling_namespace /usr/share/clearwater/bin/do_backup.sh homer`
*   `sudo cw-run_in_signaling_namespace /usr/share/clearwater/bin/do_backup.sh memento`

These each produce output of the following form, reporting the successfully-created backup.

    ...
    Deleting old backup: /usr/share/clearwater/homestead/backup/backups/1372812963174
    Creating backup for keyspace homestead_provisoning...
    Requested snapshot for: homestead_provisioning
    Snapshot directory: 1372850637124
    Backups can be found at: /usr/share/clearwater/homestead/backup/backups/provisioning/

Note that Each of the Vellum databases will produce a different snapshot in a different directory.

The backups are only stored locally - the resulting backup for each command is stored in the listed directory. Make a note of the snapshot directory for each database - these will be referred to as `<snapshot>` below.

These should be copied off the node to a secure backup server.  For example, from a remote location execute `scp -r ubuntu@<homestead node>:/usr/share/clearwater/homestead/backup/backups/provisioning/<snapshot> .`.

## Periodic Automated Local Backups

Ellis and Vellum are automatically configured to take daily backups if you've installed them through chef, at midnight local time every night.

If you want to turn this on, edit your crontab by running `sudo crontab -e` and add the following lines if not already present:

* On Ellis:
    *   `0 0 * * * /usr/share/clearwater/ellis/backup/do_backup.sh`

* On Vellum:
    *   `0 0 * * * /usr/bin/cw-run_in_signaling_namespace /usr/share/clearwater/bin/do_backup.sh homestead_provisioning`
    *   `5 0 * * * /usr/bin/cw-run_in_signaling_namespace /usr/share/clearwater/bin/do_backup.sh homestead_cache`
    *   `10 0 * * * /usr/bin/cw-run_in_signaling_namespace /usr/share/clearwater/bin/do_backup.sh homer`
    *   `15 0 * * * /usr/bin/cw-run_in_signaling_namespace /usr/share/clearwater/bin/do_backup.sh memento`

These backups are stored locally, in the same locations as they would be generated for a manual backup.

## Restoring from a Backup

There are three stages to restoring from a backup.

1.  Copying the backup files to the correct location.
2.  Running the restore backup script.
3.  Synchronizing Ellis' and Vellum's views of the system state.

**This process will impact service and overwrite data in your database.**

### Copying Backup Files

The first step in restoring from a backup is getting the backup files/directories into the correct locations on the Ellis or Vellum node.

If you are restoring from a backup that was taken on the node on which you are restoring (and haven't moved it), you can just move onto the next step.

If not, create a directory on your system that you want to put your backups into (we'll use `~/backup` in this example). Then copy the backups there.  For example, from a remote location that contains your backup directory `<snapshot>` execute `scp -r <snapshot> ubuntu@<vellum node>:backup/<snapshot>`.

On Ellis, run the following commands.

    snapshot=<snapshot>
    sudo chown root.root db_backup.sql
    sudo mkdir -p /usr/share/clearwater/ellis/backup/backups/$snapshot
    sudo mv ~/backup/$snapshot/db_backup.sql /usr/share/clearwater/ellis/backup/backups/$snapshot

On Vellum there is no need to further move the files as the backup script takes a optional backup directory parameter.

If you are restoring a Vellum backup onto a completely clean deployment, you must ensure that the new deployment has at least as many Vellum nodes as the one from which the backup was taken. Each backup should be restored onto only one node, and each node should have only one backup restored onto it. If your new deployment does not have enough Vellum nodes, you should add more nodes and then, once restoring backups is complete, scale down your deployment to the desired size.

### Running the Restore Backup Script

To actually restore from the backup file, run:

* On Ellis:
    *   `sudo /usr/share/clearwater/ellis/backup/restore_backup.sh <snapshot>`

* On Vellum:
    *   `sudo /usr/share/clearwater/bin/restore_backup.sh homestead_provisioning <hs-prov-snapshot> <backup directory>`
    *   `sudo /usr/share/clearwater/bin/restore_backup.sh homestead_cache <hs-cache-snapshot> <backup directory>`
    *   `sudo /usr/share/clearwater/bin/restore_backup.sh homer <homer-snapshot> <backup directory>`
    *   `sudo /usr/share/clearwater/bin/restore_backup.sh memento <memento-snapshot> <backup directory>`

Note that, because the 4 Vellum databases are saved to different backups, the name of the snapshot used to restore each of the databases will be different.

Ellis will produce output of the following form.

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

Vellum will produce output of the following form.

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

For Vellum, after restoring the backups you must also do the following:
- wait until the Cassandra process has restarted by running `sudo monit summary` and verifying that the `cassandra_process` is marked as `Running`
- run `sudo cw-run_in_signaling_namespace nodetool repair`

At this point, this node has been restored.

### Synchronization

It is possible (and likely) that when backups are taken on different
boxes the data will be out of sync, e.g. Ellis will know about a
subscriber, but there will no digest in Vellum. To restore the system
to a consistent state we have a synchronization tool within Ellis, which
can be run over a deployment to get the databases in sync. To run, log
into an Ellis box and execute:

    cd /usr/share/clearwater/ellis
    sudo env/bin/python src/metaswitch/ellis/tools/sync_databases.py

This will:

-   Run through all the lines on Ellis that have an owner and verify
    that there is a private identity associated with the public
    identity stored in Ellis. If successful, it will verify that a
    digest exists in Vellum for that private identity.
    If either of these checks fail, the line is considered lost and
    is removed from Ellis.
    If both checks pass, it will check that there is a valid IFC -
    if this is missing, it will be replaced with the default IFC.
-   Run through all the lines on Ellis without an owner and make sure
    there is no orphaned data in Vellum, i.e. deleting the
    simservs, IFC and digest for those lines.

## Shared Configuration

In addition to the data stored in Ellis and Vellum, a Clearwater deployment also has shared configuration that is [automatically shared between nodes](Automatic_Clustering_Config_Sharing.md). This is stored in a distributed database, and mirrored to files on the disk of each node.

### Backing Up

To backup the shared configuration:

*  If you are in the middle of [modifying shared config](Modifying_Clearwater_settings.md), complete the process to apply the config change to all nodes.
*  Log onto one of the sprout nodes in the deployment.
*  Copy the following files to somewhere else for safe keeping (e.g. another directory on the node, or another node entirely).

    ```
    /etc/clearwater/shared_config
    /etc/clearwater/bgcf.json
    /etc/clearwater/enum.json
    /etc/clearwater/s-cscf.json
    /etc/clearwater/shared_ifcs.xml
    /etc/clearwater/default_ifcs.xml
    ```

### Restoring Configuration

To restore a previous backup, copy the six files listed above to `/etc/clearwater` on one of your sprout nodes. Then run the following commands on that node:

    cw-upload_shared_config
    cw-upload_bgcf_json
    cw-upload_enum_json
    cw-upload_scscf_json
    cw-upload_shared_ifcs
    cw-upload_default_ifcs

See [Modifying Clearwater settings](Modifying_Clearwater_settings.md) for more details on this.
