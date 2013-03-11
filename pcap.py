#!/usr/bin/env python
from reconWrapping import CallRecon
from swift.common.ring.ring import Ring
from swift.common.ring.ring import RingData
import subprocess
import json, os
#ToDo 
#1. Remove Drives
#2. Rebalance


def get_ring(builder):
	conf = {}
	try:
		swift_dir = conf.get('swift_dir', '/etc/swift')
	except:
		os.system("sudo /bin/chmod 710 /etc/swift/")
		swift_dir = conf.get('swift_dir', '/etc/swift')
	return Ring(swift_dir, ring_name=builder)

def chmod():
	os.system("sudo /bin/chmod 710 /etc/swift/")

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

def rebalance(builder):
	val = subprocess.call(["/usr/bin/swift-ring-builder", "/etc/swift/" + builder + ".builder", "rebalance"], stdout=open(os.devnull, 'wb'))
        if (str(val) == '2'): #If it's a permissions error, chmod
		os.system("sudo /bin/chmod 710 /etc/swift/")
		return subprocess.call(["/usr/bin/swift-ring-builder", "/etc/swift/" + builder + ".builder", "rebalance"])
	return val

#Returns a dict for a particular drive via swift recon.
#Used to get info on mounting and drive sizes
def getDriveSizeDetails(d):
	server_location = "http://%(ip address)s:%(port)s/recon/diskusage" % d
       	try:
        	result = subprocess.check_output(["curl", "-silent", "-i", server_location], shell=False)
	        return json.loads(result.split("\n")[-1])[0]
        except subprocess.CalledProcessError:
        	pass #Something should be done here.
	return []

#Returns a tuple that has (Used space, Max Space)
def totalSpace():
	drives = allUniqueDrives()
	drive_data = []
	for d in drives:
		try:
			drive_data.append(getDriveSizeDetails(d))
		except subprocess.CalledProcessError:
			pass #Something should be done here.
	used_space = float(sum([d["used"] for d in drive_data]))
	total_space = float(sum([d["size"] for d in drive_data]))
	return (used_space, total_space)


def removeDrive(builder, ip, device):
	args = ["/usr/bin/swift-ring-builder", "/etc/swift/" + builder + ".builder", "remove"]
	if device != "":
		args.append(ip + "/" + device)
	else:
		args.append(ip)
	return subprocess.call(args, stdout=open(os.devnull, 'wb'))


#Lists all drives by their their zone. Returns in a similar way to fetchAllDrives
def drivesByZone(builder):
	drives = drivesInBuilder(builder)
	zoned_devs = {}
	for d in drives:
		d_size_info = getDriveSizeDetails(d)
		d['size'] = d_size_info['size']
		d['used'] = d_size_info['used']
		d['avail']= d_size_info['avail']
		if d['zone'] in zoned_devs:
			zoned_devs[d['zone']].append(d)
		else:
			zoned_devs[d['zone']] = [d]
	return zoned_devs



#Gets a list of every drive in Object, Account and Container builder
def allDrives():
	return drivesInBuilder("object") + drivesInBuilder("account") + drivesInBuilder("container")

#Returns all zoned drives where drives are displayed uniquely..
def allZonedDrives():
	object_drives = drivesByZone("object")
	container_drives = drivesByZone("container")
	account_drives = drivesByZone("account")
	drives_dict = {}
	#I hate myself beyond this point:
	for builder in [object_drives, container_drives, account_drives]:
		for zone in builder:
			if zone not in drives_dict:
				drives_dict[zone] = builder[zone]
			else:
				for dev in builder[zone]:
					unique_drives = filter(lambda x: x["ip address"] != dev["ip address"] ,drives_dict[zone])
					if len(unique_drives) != 0:
						drives_dict[zone].append(unique_drives)
	return drives_dict

#Gets all the drives in the 3 builders and cuts it down so each drive only appears once. (based on ip/name)
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


#Returns a list of drives usign the swift-ring-builder
def drivesInBuilder(builder):
	try:
		output = subprocess.check_output(["/usr/bin/swift-ring-builder", "/etc/swift/" + builder + ".builder"])
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
	except:
		chmod()
		return drivesInBuilder(builder)

#Returns a list of drives using the python libraries
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
