#!/usr/bin/env python

from components import Page
from swiftclient import Connection

class Lcap(Page):
	name = "Logical Capacity"
	
	def __init__(self):

		user_name="tester"
		account_name="test"
		password="testing"

		creds=account_name + ":" + user_name

		conn = Connection(authurl="http://127.0.0.1:8080/auth/v1.0/", user=creds, key=password)
		headers = conn.head_account()

		total_containers = headers.get('x-account-container-count', 0)
		total_objects = headers.get('x-account-object-count', 0)
		total_bytes = headers.get('x-account-bytes-used', 0)

		self.content += "<br/> ======================================="
		self.content += "<br/> Tenant: " + account_name
		self.content += "<br/> ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		self.content += "<br/> Total containers " + total_containers
		self.content += "<br/> Total objects " + total_objects
		self.content += "<br/> Total bytes " + total_bytes

		body = conn.get_account()

		self.content += "<table><tbody>"

	        for x in range(int (total_containers)):
                        cont_inf = body[1][x]
                        cont_values = cont_inf.values()
                        self.content += "<tr>"
                        self.content += "<th scope='row'> Container: " + cont_values[2] + " Total objects: " + str (cont_values[0]) + " Total bytes: " + str (cont_values[1]) + "</th>"
                        self.content += "<td>" + str (cont_values[0]) + "</td>"
			self.content += "</tr>"
		self.content += "</tbody></table>"
		
		self.content += "<div id='containers'></div>"

		Page.__init__(self)
page = Lcap()

