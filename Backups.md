# Backups

Within a Clearwater deployment, ellis, homestead and homer all store persistent data.  (Bono and sprout do not.)  To prevent data loss in disaster scenarios, ellis, homestead and homer all have data backup and restore mechanisms.  Specifically, all support

*   manual backup
*   periodic automated local backup
*   manual restore.

This document describes

*   how to list the backups that have been taken
*   how to take a manual backup
*   the periodic automated local backup behavior
*   how to restore from a backup.

## Listing Backups

The process for listing backups varies between ellis, homestead and homer.

### Ellis

To list the backups that have been taken on ellis, run `sudo /usr/share/clearwater/ellis/backup/list_backups.sh`.

    Backups for ellis:
    1372294741  /usr/share/clearwater/ellis/backup/backups/1372294741
    1372294681  /usr/share/clearwater/ellis/backup/backups/1372294681
    1372294621  /usr/share/clearwater/ellis/backup/backups/1372294621
    1372294561  /usr/share/clearwater/ellis/backup/backups/1372294561

### Homestead and Homer

To list the backups that have been taken on homestead or homer, run

*   `sudo /usr/share/clearwater/homestead/backup/list_backups.sh homestead` for homestead
*   `sudo /usr/share/clearwater/homer/backup/list_backups.sh homer` for homer.

This produces output of the following form, listing each of the available backups.

    Backups for keyspace homestead:

    Backups for columnfamily /var/lib/cassandra/data/homestead/public_ids/snapshots:
    1372336442947  /var/lib/cassandra/data/homestead/public_ids/snapshots/1372336442947

    Backups for columnfamily /var/lib/cassandra/data/homestead/filter_criteria/snapshots:
    1372336442947  /var/lib/cassandra/data/homestead/filter_criteria/snapshots/1372336442947

    Backups for columnfamily /var/lib/cassandra/data/homestead/private_ids/snapshots:
    1372336442947  /var/lib/cassandra/data/homestead/private_ids/snapshots/1372336442947

    Backups for columnfamily /var/lib/cassandra/data/homestead/sip_digests/snapshots:
    1372336442947  /var/lib/cassandra/data/homestead/sip_digests/snapshots/1372336442947

## Taking a Manual Backup

The process for taking a manual backup varies between ellis, homestead and homer.  Note that in all cases,

*   the backup is stored locally and should be copied to a secure backup server to ensure resilience
*   this process only backs up a single local node, so the same process must be run on all nodes in a cluster to ensure a complete set of backups
*   these processes cause a small amount of extra load on the disk, so it is recommended not to perform this during periods of high load
*   only 4 backups are stored locally - when a fifth backup is taken, the oldest is deleted.

### Ellis

To take a manual backup on ellis, run `sudo /usr/share/clearwater/ellis/backup/do_backup.sh`.

This produces output of the following form, reporting the successfully-created backup.

    Creating backup in /usr/share/clearwater/ellis/backup/backups/1372336317/db_backup.sql

Make a note of the snapshot directory (`1372336317` in the example above) - this will be referred to as `<snapshot>` below.

This file is only accessible by the root user.  To copy it to the current user's home directory, run

    snapshot=<snapshot>
    sudo bash -c 'cp /usr/share/clearwater/ellis/backup/backups/'$snapshot'/db_backup.sql ~'$USER' &&
                  chown '$USER.$USER' db_backup.sql'

This file can, and should, be copied off the ellis node to a secure backup server.

### Homestead and Homer

To take a manual backup on homestead or homer, run

*   `sudo /usr/share/clearwater/homestead/backup/do_backup.sh homestead` on homestead
*   `sudo /usr/share/clearwater/homer/backup/do_backup.sh homer` on homer.

This produces output of the following form, reporting the successfully-created backup.

    Creating backup for keyspace homestead...
    Requested snapshot for: homestead
    Snapshot directory: 1372333275341

Make a note of the snapshot directory - this will be referred to as `<snapshot>` below.

The backups are only stored locally - the resulting backup is stored in

*   on homestead, `/var/lib/cassandra/data/homestead/sip_digests/snapshots/<snapshot>` and `/var/lib/cassandra/data/homestead/filter_criteria/snapshots/<snapshot>`
*   on homer, `/var/lib/cassandra/data/homer/simservs/snapshots/<snapshot>`.

These directories are only accessible by the cassandra user.  To copy them to the current user's home directory, run

    snapshot=<snapshot>
    sudo bash -c '[ ! -d /var/lib/cassandra/data/homestead ] ||
                  ( cp -R /var/lib/cassandra/data/homestead/sip_digests/snapshots/'$snapshot' ~'$USER/$snapshot'.sip_digests &&
                    chown '$USER.$USER' '$snapshot'.sip_digests )'
    sudo bash -c '[ ! -d /var/lib/cassandra/data/homestead ] ||
                  ( cp -R /var/lib/cassandra/data/homestead/filter_criteria/snapshots/'$snapshot' ~'$USER/$snapshot'.filter_criteria &&
                    chown '$USER.$USER' '$snapshot'.filter_criteria )'
    sudo bash -c '[ ! -d /var/lib/cassandra/data/homer ] ||
                  ( cp -R /var/lib/cassandra/data/homer/simservs/snapshots/'$snapshot' ~'$USER/$snapshot'.simservs &&
                    chown '$USER.$USER' '$snapshot'.simservs )'

These directories (`~/<snapshot>.*`) can, and should, be copied off the homestead or homer node to a secure backup server.

## Periodic Automated Local Backups

Ellis, homestead and homer are all automatically configured to take daily backups, at midnight local time every night.

These backups are stored locally, in the same locations as they would be generated for a manual backup.

## Restoring from a Backup

There are three stages to restoring from a backup.

1.  Copying the backup files to the correct location.
2.  Running the restore backup script.
3.  Synchronizing ellis, homestead and homer's views of the system state.

**This process will impact service and overwrite data in your database.**

### Copying Backup Files

The first step in restoring from a backup is getting the backup files/directories into the correct locations on the ellis, homer or homestead node.

If you are restoring from a backup that was taken on the node on which you are restoring (and haven't moved it), you can just move onto the next step.

If not, copy the files to your home directory and then run one of the following commands.

On ellis, run the following commands, picking an arbitrary snapshot number to use as `<snapshot>`.

    snapshot=<snapshot>
    sudo chown root.root db_backup.sql
    sudo mkdir -p /usr/share/clearwater/ellis/backup/backups/$snapshot
    sudo mv db_backup.sql /usr/share/clearwater/ellis/backup/backups/$snapshot

On homestead, run the following commands, using the snapshot number you're trying to restore as `<snapshot>`.

    snapshot=<snapshot>
    sudo mkdir -p /var/lib/cassandra/data/homestead/sip_digests/snapshots
    sudo mv $snapshot.sip_digests /var/lib/cassandra/data/homestead/sip_digests/snapshots/$snapshot
    sudo mkdir -p /var/lib/cassandra/data/homestead/filter_criteria/snapshots
    sudo mv $snapshot.filter_criteria /var/lib/cassandra/data/homestead/filter_criteria/snapshots/$snapshot
    sudo chown cassandra.cassandra /var/lib/cassandra

On homer, run the following commands, using the snapshot number you're trying to restore as `<snapshot>`.

    snapshot=<snapshot>
    sudo mkdir -p /var/lib/cassandra/data/homer/simservs/snapshots
    sudo mv $snapshot.simservs /var/lib/cassandra/data/homer/simservs/snapshots/$snapshot
    sudo chown cassandra.cassandra /var/lib/cassandra

### Running the Restore Backup Script

To actually restore from the backup file, run

*   `sudo /usr/share/clearwater/ellis/backup/restore_backup.sh <snapshot>` on ellis
*   `sudo /usr/share/clearwater/homestead/backup/restore_backup.sh homestead <snapshot>` on homestead
*   `sudo /usr/share/clearwater/homer/backup/restore_backup.sh homer <snapshot>` on homer.

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

Homestead or homer will produce output of the following form.

    Will attempt to backup from backup 1372336442947
    Found backup directory 1372336442947
    Found backup directory 1372336442947
    Found backup directory 1372336442947
    Found backup directory 1372336442947
    Restoring backup for keyspace homestead...
    xss =  -ea -javaagent:/usr/share/cassandra/lib/jamm-0.2.5.jar -XX:+UseThreadPriorities -XX:ThreadPriorityPolicy=42 -Xms826M -Xmx826M -Xmn100M -XX:+HeapDumpOnOutOfMemoryError -Xss180k
    Clearing commitlog...
    Deleting old .db files...
    Restoring from backup: 1372336442947
    Deleting old .db files...
    Restoring from backup: 1372336442947
    Deleting old .db files...
    Restoring from backup: 1372336442947
    Deleting old .db files...
    Restoring from backup: 1372336442947


At this point, this node has been restored.

### Synchronization

It is possible (and likely) that when backups are taken on different
boxes the data will be out of sync, e.g. ellis will know about a
subscriber, but there will no digest in homestead. To restore the system
to a consistent state we have a syncronization tool within ellis, which
can be run over a deployment to get the databases in sync. To run, log
into an ellis box and execute:

    cd /usr/share/clearwater/ellis
    sudo env/bin/python src/metaswitch/ellis/tools/sync_databases.py

This will:

-   Run through all the lines on ellis that have an owner and verify
    that their digest exists in homestead. If it does not, the line is
    considered lost and is removed from ellis. If the digest exists, it
    will check that there is a valid IFC - if this is missing, it will
    be replaced with the default IFC.
-   Run through all the lines on ellis without an owner and make sure
    there is no orphaned data in homestead and homer, i.e. deleting the
    simservs, IFC and digest for those lines.
