#!/usr/bin/env python
from components import Page
import httplib

import smtplib
from email.mime.text import MIMEText

from swift.common.ring.ring import Ring
from swift.common.ring.ring import RingData


class Alerting(Page):
	name = "Alerting"

	def __init__(self):
	        self.establishConnection()
		Page.__init__(self)	
	def establishConnection(self):
		conn = httplib.HTTPConnection("127.0.0.1:6000")
		conn.request("GET", "/recon/unmounted")
		r1 = conn.getresponse()
		body = r1.read()	

		if body == "[]":
			self.content+="No errors detected. Drives are OK."
		else:
			self.content+="Openstack Swift Alert! Drive errors detected!<br> The following drives have been automatically unmounted to avoid further issues:<br><br>" + body

page = Alerting()
