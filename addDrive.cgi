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
				["weight", "zone", "ip", "port", "device", "meta"]<br/>
				""")

	def argsOK(self, args):
		testAgainst = ["weight", "zone", "ip", "port", "device", "meta"] #List of vars we want
		return set(testAgainst).issubset(args)

	def addDrive(self, dev):
		if dev["objserver"] == "true":
			cmd = "swift-ring-builder /etc/swift/object.builder add " + str(self.formatDev(dev)) + " 100"
			procobj = os.popen(cmd)
			processedobj = procobj.read()
			procobj.close()
			self.addContent(processedobj + "<br/>" + cmd + "<br/>" )

		if dev["accserver"] == "true":
                        cmdacc = "swift-ring-builder /etc/swift/account.builder add " + str(self.formatDev(dev)) + " 100"
                        procacc = os.popen(cmdacc)
                        processedacc = procacc.read()
                        procacc.close()
                        self.addContent(processedacc + "<br/>" + cmdacc + "<br/>" )

		if dev["contserver"] == "true":
                        cmdcont = "swift-ring-builder /etc/swift/container.builder add " + str(self.formatDev(dev)) + " 100"
                        proccont = os.popen(cmdcont)
                        processedcont = proccont.read()
                        proccont.close()
                        self.addContent(processedcont + "<br/>" + cmdcont + "<br/>" )

	def formatDev(self, dev):
		return 'z%(zone)s-%(ip)s:%(port)s/%(device)s_"%(meta)s"' % dev

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
