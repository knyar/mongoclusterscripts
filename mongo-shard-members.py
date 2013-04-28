#!/usr/bin/env python
import pymongo

""" Show all shards of your sharded cluster. If shard is a replicaset,
    show its members along with their status and replication lag.
"""

connection = pymongo.Connection('127.0.0.1:27017')
for shard in connection['config']['shards'].find():
    if '/' in shard['host']:
        # woa, it's a replicaset, gotta show some stats
        hosts = shard['host'].split('/')[1]
        s = pymongo.Connection(hosts.split(','))
        rs = s['admin'].command("replSetGetStatus")
        conf = s['local']['system.replset'].find_one()
        print("{}: {} ({})".format(
            shard['_id'],
            shard['host'], 'OK' if int(rs['ok']) else 'NOT OK'))
        members = sorted(rs['members'], key=lambda x: x['state'])
        mastertime = members[0]['optimeDate']
        for member in members:
            priority = 1
            for conf_member in conf['members']:
                if conf_member['host'] == member['name'] and \
                        'priority' in conf_member:
                    priority = conf_member['priority']
            if member['state'] == 1:  # primary
                mastertime = members[0]['optimeDate']
            if member['state'] != 1 and 'optimeDate' in member:
                seconds_behind = mastertime - member['optimeDate']
                status = '{} seconds behind'.format(
                    int(seconds_behind.total_seconds()))
            else:
                status = ''

            print(" - {:10} (prio {:3}) {:40} ({}) {}".format(
                member['stateStr'],
                priority,
                member['name'],
                'OK' if int(member['health']) else 'NOT OK',
                status
            ))
    else:
        print("{}: {}".format(shard['_id'], shard['host']))
