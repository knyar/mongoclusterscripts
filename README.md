mongoclusterscripts
===================

Various scripts for your MongoDB sharded cluster.

All scripts are in Python and obviously need the `pymongo` module to work.

I use all these scripts in production, but I highly recommend you to read them
and understand how they work before relying on them.

mongo-backup
------------

This directory contains the `mongoclusterbackup` python module that can be used
to create consistent backups of your mongodb cluster.

It basically follows [mongodb shard backup procedure described in mongodb
documentation](http://docs.mongodb.org/manual/tutorial/backup-sharded-cluster-with-filesystem-snapshots/):
- stops cluster balancer;
- stops one of configuration servers to prevent metadata changes;
- backs up configuration database;
- locks all shards. If your shards are replicasets, only one of the secondary
  servers will be locked;
- creates LVM snapshots on the servers;
- unlocks the shards;
- starts the configuration server and enables the balancer.

This ensures that consistent cluster data is present on the servers. You
will still have to copy that data to the backup medium of your choice and
remove LVM snapshots.

Check `run.py` for a sample launching script.

mongo-shard-members
-------------------

Shows all shards of your sharded cluster. If a shard is a replicaset, shows its
members along with their status and replication lag.

splitter
--------

Chunk splitter that tries to balance the number of objects per chunk rather
than their size.

MongoDB balancer splits chunks based on the total size of each chunk.
Sometimes this is not what you need and you would rather balance your chunks
depending on the number of objects they contain, not their bytesize.

This script goes through each shard of your cluster, counts the number
of items in each chunk (which is quite expensive operation when you
have a large number of chunks) and splits each chunk. It repeats this
until all your chunks have less than a given number of objects in them.

Credits
=======

Copyright (c) 2013, Anton Tolchanov

The scripts are licensed under MIT license.
