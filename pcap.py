#!/usr/bin/env python
from reconWrapping import CallRecon
from swift.common.ring.ring import Ring
from swift.common.ring.ring import RingData
import subprocess
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
def test():
	drivesInBuilder("")

def removeDrive(builder, ip, device):
	output = subprocess.check_output(["swift-ring-builder", "/etc/swift/object.builder"])

def drivesByZone():
	drives = allDrives()
	zoned_devs = {}
	for d in drives:
		if d['zone'] in zoned_devs:
			zoned_devs[d['zone']].append(d)
		else:
			zoned_devs[d['zone']] = [d]
	return zoned_devs
def allDrives():
	return drivesInBuilder("object") + drivesInBuilder("account") + drivesInBuilder("container")

def allUniqueDrives():
	all_drives =  allDrives()
	unique_drives = []
	ip_names = set([])
	for d in all_drives:
		ip_name = (d["ip address"], d["name"])
		if ip_name not in ip_names:
			unique_drives.append(d)
		ip_names.add(ip_name)
	return unique_drives

def drivesInBuilder(builder):
	output = subprocess.check_output(["swift-ring-builder", "/etc/swift/" + builder + ".builder"])
	output_list = output.split('\n') #Break the output into a list seperated by new lines

	#Header related stuff#
	headers_dirty = output_list[3].split()[1:] #Make a list of the headers
	headers = map(lambda x: x.replace(":", ""), headers_dirty) #Clean up the headers (remove things like colons)
	headers = filter(lambda x: x!= "address", headers) #Removed the "address element"
	headers = map(lambda x: x if x != "ip" else "ip address", headers) #Changed "ip" to "ip address"

	#Drive list related stuff#
	filtered_list = filter(lambda x: x != "" , output_list)[4:] #Remove empty spaces
	clean_list = map(lambda x: x.split(), filtered_list) #Remove the whitespace

	return map(lambda x : dict(zip(headers, x)),clean_list)

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
