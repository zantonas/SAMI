#!/usr/bin/env python
from reconWrapping import CallRecon
from swift.common.ring.ring import Ring
import json, os

def get_ring(builder):
	conf = {}
	try:
		swift_dir = conf.get('swift_dir', '/etc/swift')
	except:
		os.system("sudo /bin/chmod 710 /etc/swift/")
		swift_dir = conf.get('swift_dir', '/etc/swift')
	return Ring(swift_dir, ring_name=builder)


def fetchDrives(zone):
	iZone = int(zone)
	conf = {}
	object_ring = get_ring("object")
	device_list = object_ring.devs
	zoned_devs = dict()
	for iDev in device_list[:]:
		if iDev['zone'] in zoned_devs:
				zoned_devs[iDev['zone']].append(iDev)
		else:
				zoned_devs[iDev['zone']] = [iDev]
	if iZone in zoned_devs:
		return zoned_devs[iZone]
	else:
		return '[{}]'


def fetchDrivesInBuilder(builder):
	conf = {}
	object_ring = get_ring(builder)
	device_list = object_ring.devs
	zoned_devs = {}
	reconData = {}
	for iDev in device_list[:]:
		if iDev != None:
			if iDev['zone'] in zoned_devs:
				zoned_devs[iDev['zone']].append(iDev)
			else:
				zoned_devs[iDev['zone']] = [iDev]
				if iDev['ip'] not in reconData:
					reconData[iDev['ip']] = json.loads(CallRecon(iDev['ip'], iDev['port']).establishConnection())
				for reconDevice in reconData:
					for dev in reconData[reconDevice]:
						if dev['device'] == iDev['device']:
							iDev['used'] = dev['used']
							iDev['size'] = dev['size']
	return zoned_devs