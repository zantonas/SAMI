#!/usr/bin/env python
from components import Page
import httplib

from swift.common.ring.ring import Ring
from swift.common.ring.ring import RingData


class CallRecon():
        def __init__(self, ip, port):
		self.ip = ip
		self.port = port
        
	def establishConnection(self):
		try:
                	conn = httplib.HTTPConnection(str(self.ip) + ":" + str(self.port))
                	conn.request("GET", "/recon/diskusage")
                	r1 = conn.getresponse()
                	return r1.read()
		except Exception, e:
			return ""

