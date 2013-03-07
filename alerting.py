#!/usr/bin/env python
from components import Page
import httplib
import json
import ast
from swift.common.ring.ring import Ring
from swift.common.ring.ring import RingData

#FORMAT: [key=ip][port]
diskips = dict()

conf = {}
swift_dir = conf.get('swift_dir', '/etc/swift')

account_ring = Ring(swift_dir, ring_name='account')
account_device_list = account_ring.devs
account_zoned_devs = dict()
for iDev in account_device_list[:]:
	if iDev != None:
                if iDev['zone'] in account_zoned_devs:
                                account_zoned_devs[iDev['zone']].append(iDev)
                else:
                                account_zoned_devs[iDev['zone']] = [iDev]
for zone in account_zoned_devs:
                for device in account_zoned_devs[zone]:
                                obj = {'port':device['port']}
                                ref = device['ip']
                                if ref in diskips:
                                                diskips[ref].append(obj)
                                else:
                                                diskips[ref] = [obj]



container_ring = Ring(swift_dir, ring_name='container')
container_device_list = container_ring.devs
container_zoned_devs = dict()
for iDev in container_device_list[:]:
	if iDev != None:
                if iDev['zone'] in container_zoned_devs:
                                container_zoned_devs[iDev['zone']].append(iDev)
                else:
                                container_zoned_devs[iDev['zone']] = [iDev]
for zone in container_zoned_devs:
                for device in container_zoned_devs[zone]:
                                obj = {'port':device['port']}
                                ref = device['ip']
                                if ref in diskips:
                                                diskips[ref].append(obj)
                                else:
                                                diskips[ref] = [obj]


object_ring = Ring(swift_dir, ring_name='object')
object_device_list = object_ring.devs
object_zoned_devs = dict()
for iDev in object_device_list[:]:
	if iDev != None:
                if iDev['zone'] in object_zoned_devs:
                                object_zoned_devs[iDev['zone']].append(iDev)
                else:
                                object_zoned_devs[iDev['zone']] = [iDev]
for zone in object_zoned_devs:               
		 for device in object_zoned_devs[zone]:
                                obj = {'port':device['port']}
                                ref = device['ip']
                                if ref in diskips:
                                                diskips[ref].append(obj)
                                else:
                                                diskips[ref] = [obj]


unmounted_drives = dict()

nodes_unpingable = []
for storagenode in diskips:
                conn = httplib.HTTPConnection(storagenode + ':' + str(diskips[storagenode][0]['port']))
                try:
                                conn.request("GET", "/recon/unmounted")
                                response = conn.getresponse()
                                body = json.loads(response.read())
                                for device in range(len(body)):
                                                obj = {'port':diskips[storagenode][0]['port'], 'device':body[device]['device']}
                                                ref = storagenode
                                                if ref in unmounted_drives:
                                                                unmounted_drives[ref].append(obj)
                                                else:
                                                                unmounted_drives[ref] = [obj]
                except:
                                nodes_unpingable.append(storagenode)

f = open('alerting.dat', 'w+')
f.seek(0)
f.write(','.join(nodes_unpingable) + '\n')
drives = ast.literal_eval(json.dumps(unmounted_drives))
f.write(str(drives))
f.close()

