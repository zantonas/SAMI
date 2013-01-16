#!/usr/bin/env python
from components import Page
from swiftclient import Connection

class Lcap(Page):
	name = "Logical Capacity"
	
	def __init__(self):
		Page.__init__(self)
	

		user_name="tester"
		account_name="test"
		password="testing"

		creds=account_name + ":" + user_name

		conn = Connection(authurl="http://127.0.0.1:8080/auth/v1.0/", user=creds, key=password)
		headers = conn.head_account()

		total_containers = headers.get('x-account-container-count', 0)
		total_objects = headers.get('x-account-object-count', 0)
		total_bytes = headers.get('x-account-bytes-used', 0)


		print "======================================="
		print "Tenant: " + account_name
		print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		print "Total containers " + total_containers
		print "Total objects " + total_objects
		print "Total bytes " + total_bytes


		body = conn.get_account()

		for x in range(int (total_containers)):
  			cont_inf = body[1][x]
			cont_values = cont_inf.values()
			print "---------------------------------------"
			print "   Container: " + cont_values[2]
			print "---------------------------------------"
			print "   Total objects " + str (cont_values[0])
			print "   Total bytes " + str (cont_values[1])

		print "======================================="
	
page = Lcap()
