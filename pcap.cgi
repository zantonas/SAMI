#!/usr/bin/env python
from components import Page
from swiftclient import Connection
from swift.common.ring.ring import Ring
from swift.common.ring.ring import RingData
class Pcap(Page):
	name = "Physical Capacity"

	def __init__(self):
		self.whiteLightning()
		Page.__init__(self)
		
		#print "hey"
		#swiftclient.client.head_account("http://127.0.0.1:8080/v1/AUTH_test", "test:tester", "AUTH_tkb0cec83203184895a641a2cda75bacfc")
	def addContent(self, text):
		self.content += "\n" + text	

	def whiteLightning(self):
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
		self.addContent("<br/>" + str(zoned_devs[1]) );
					 
	def establishConnection(self):
		user_name="tester"
		account_name="test"
		password="testing"

		creds=account_name + ":" + user_name

		conn = Connection(authurl="http://127.0.0.1:8080/auth/v1.0/", user=creds, key=password)
		headers = conn.head_account()

		total_containers = headers.get('x-account-container-count', 0)
		total_objects = headers.get('x-account-object-count', 0)
		total_bytes = headers.get('x-account-bytes-used', 0)


		self.content += "\n<br/>======================================="
		self.content +=  "\n<br/>Tenant: " + account_name
		self.content +=  "\n<br/>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		self.content +=  "\n<br/>Total containers " + total_containers
		self.content +=  "\n<br/>Total objects " + total_objects
		self.content +=  "\n<br/>Total bytes " + total_bytes

page = Pcap()
