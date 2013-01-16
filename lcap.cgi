#!/usr/bin/env python
from components import Page
import swiftclient.client


class Lcap(Page):
	name = "Logical Capacity"
	
	def __init__(self):
		Page.__init__(self)
		#print "hey"
		#swiftclient.client.head_account("http://127.0.0.1:8080/v1/AUTH_test", "test:tester", "AUTH_tkb0cec83203184895a641a2cda75bacfc")
		
		

page = Lcap()