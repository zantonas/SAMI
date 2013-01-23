#!/usr/bin/env python
from components import Page
from swiftclient import Connection
from swift.common.ring.ring import Ring
from swift.common.ring.ring import RingData

class Pcap(Page):
	name = "Physical Capacity"

	def __init__(self):
		zDrives = self.fetchAllDrives()
		self.addContent(str(zDrives[1]))
		Page.__init__(self)
	
	def addContent(self, text):
		self.content += "\n" + text

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
		self.addContent("<br/>Can")
		#ring_data = RingData.load("/etc/swift/object.ring.gz")
		device_list = self.object_ring.devs
		zoned_devs = dict()
		for iDev in device_list[:]:
			if iDev['zone'] in zoned_devs:
				zoned_devs[iDev['zone']].append(iDev)
			else:
				zoned_devs[iDev['zone']] = [iDev]
		return zoned_devs
					 
	def fetchAllDriveUsage(self):
		pass
page = Pcap()
