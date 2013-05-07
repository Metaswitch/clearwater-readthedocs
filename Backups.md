Clearwater Backups
==================

All the database backed nodes in Clearwater (currently Ellis, Homer &
Homestead) have an automatic backup facility.

### Backup scripts

Backup scripts for a node are found in
**/usr/share/clearwater/&lt;node\_name\>/backup** - i.e. for an ellis node
**/usr/share/clearwater/ellis/backup**. Available scripts:

-   **sudo ./list\_backups.sh** displays a list of available backups
-   **sudo ./do\_backup.sh** performs a backup right now
-   **sudo ./restore\_backup.sh** restores from a backup - defaulting to
    the latest backup. Optionally pass in a specific backup, e.g.
    **./restore\_backup.sh 1234**

Note for homer and homestead nodes it is necessary to also supply the
node type as the first parameter to the above scripts, e.g.
**./list\_backups.sh homer** or **./restore\_backup.sh homestead 666**

### Synchronizing backups

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

### Restoring from a remote backup

Remote backups are currently not implemented, to backup remotely you
will need to manually copy the backups files to a remote location. The
backup files are located in:

-   **ellis:** /usr/share/clearwater/ellis/backup/backups
-   **homer:** /var/lib/cassandra/data/homer/simservs/snapshots
-   **homestead:**
    /var/lib/cassandra/data/homestead/sip\_digests/snapshots and
    /var/lib/cassandra/data/homestead/filter\_criteria/snapshots

### Periodic backups

Backups are setup by Chef as a daily cron job, which is run at midnight.

### Backup rotation

The backup scripts only keep the last 4 backups. When creating a new
backup **do\_backup** will delete the oldest backup if 4 backups already
exist.

### Cassandra backups

The backup scripts for Homer and Homestead build on the backup
functionality [available in
Cassandra](http://www.datastax.com/docs/1.1/backup_restore). As such,
the daily backups will be put into the same place as those already
created by Cassandra. Cassandra automatically creates a backup before a
TRUNCATE or DROP command is executed. These backups can be restored in
the same way as the daily backups, using the **restore\_backup** script.
