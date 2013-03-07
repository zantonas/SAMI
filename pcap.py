#!/usr/bin/env python
from components import Page
from reconWrapping import CallRecon
from swiftclient import Connection
from swift.common.ring.ring import Ring
from swift.common.ring.ring import RingData
import json

class PcapTools:

        def __init__(self):
		pass

        def fetchDrives(self, zone):
                iZone = int(zone) #Is this how casting shit works?
                conf = {}
                swift_dir = conf.get('swift_dir', '/etc/swift')
                self.object_ring = Ring(swift_dir, ring_name='object')
                device_list = self.object_ring.devs
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

        def fetchAllDrives(self):
                conf = {}
                swift_dir = conf.get('swift_dir', '/etc/swift')
                self.object_ring = Ring(swift_dir, ring_name='object')
                device_list = self.object_ring.devs
                zoned_devs = dict()
                reconData = {}
                for iDev in device_list[:]:
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

        def fetchDrivesInBuilder(self, builder):
                conf = {}
                swift_dir = conf.get('swift_dir', '/etc/swift')
                self.object_ring = Ring(swift_dir, ring_name=builder)
                device_list = self.object_ring.devs
                zoned_devs = {}
                reconData = {}
		for iDev in device_list[:]:
			if not str(iDev)=='None':
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

