#!/usr/bin/env python
from components import Page
import cgi
import json
import os
import pcap
class AddDrive(Page):
        name = "Add Drive"

        def __init__(self):
		self.input()
                Page.__init__(self)
	
	def input(self):
		args = cgi.FieldStorage()
		if self.argsOK(args):
			newDrive = Drive(args)
			self.addDrive(newDrive.toDict())
		else:
			self.addContent("""
				args missing<br/>
				Please be sure to have included the following:<br/>
				["weight", "zone", "ip", "port", "device"]<br/>
				""")

	def argsOK(self, args):
		testAgainst = ["weight", "zone", "ip", "port", "device"] #List of vars we want
		return set(testAgainst).issubset(args)

	def addDrive(self, dev):
		try:
			if dev["objserver"] == "true":
				cmd = "sudo swift-ring-builder /etc/swift/object.builder add " + str(self.formatDev(dev)) + " " + dev["weight"]
				procobj = os.popen(cmd)
				processedobj = procobj.read()
				procobj.close()
				self.addContent(processedobj + cmd )

			if dev["accserver"] == "true":
        	                cmdacc = "sudo swift-ring-builder /etc/swift/account.builder add " + str(self.formatDev(dev)) + " " + dev["weight"]
        	                procacc = os.popen(cmdacc)
                        	processedacc = procacc.read()
                        	procacc.close()
	                        self.addContent(processedacc)

			if dev["contserver"] == "true":
                        	cmdcont = "sudo swift-ring-builder /etc/swift/container.builder add " + str(self.formatDev(dev)) + " " + dev["weight"]
                        	proccont = os.popen(cmdcont)
                        	processedcont = proccont.read()
                        	proccont.close()
                        	self.addContent(processedcont)
		except:
			pcap.chmod()
			self.addDrive(dev)
			
	def formatDev(self, dev):
		if dev["meta"] != None:
			return 'z%(zone)s-%(ip)s:%(port)s/%(device)s_"%(meta)s"' % dev
		else:
			return 'z%(zone)s-%(ip)s:%(port)s/%(device)s' % dev

class Drive:
	def __init__(self, data):
		if "contserver" in data:
			if data.getvalue("contserver") == "on":
				self.cont = "true"
			else:
	                        self.cont = "false"

		else:
			self.cont = "false"

		if "accserver" in data:
                        if data.getvalue("accserver") == "on":
                                self.acc = "true"
			else:
	                        self.acc = "false"
		else:
                        self.acc = "false"

		if "objserver" in data:
                        if data.getvalue("objserver") == "on":
                                self.obj = "true"
			else:
				self.obj = "false"
		else:
                        self.obj = "false"

		
		self.weight = data.getvalue("weight")
		self.zone = data.getvalue("zone")
		self.ip = data.getvalue("ip")
		self.port = data.getvalue("port")
		self.device = data.getvalue("device")
		self.meta = data.getvalue("meta")
	
	def toDict(self):
		return {'zone':self.zone, 'ip':self.ip, 'port':self.port, 'device':self.device, 'weight':self.weight, 'meta':self.meta, 'contserver': self.cont, 'accserver': self.acc, 'objserver': self.obj}

Page = AddDrive()
