#!/usr/bin/env python

from components import Page
from swiftclient import Connection

import cgi

import json
from keystoneclient.v2_0 import client

class Users(Page):
	name = 'User Management'
	
	def __init__(self):
		self.generate_tables()
		Page.__init__(self)
		
	def generate_tables(self):

		token = 'ADMIN'
		endpoint = 'http://10.29.125.11:35357/v2.0/'

		keystone = client.Client(token=token, endpoint=endpoint)
		
		###DEAL WITH POST FIRST
		#############################
		form = cgi.FieldStorage()
                user_name = form.getvalue("name")

                if user_name != None:
                        password = form.getvalue("password")
                        enable = form.getvalue("enabled")
                        email = form.getvalue("email")
                        if enable == 'true':
                                keystone.users.create(name=user_name, password=password, email=email)
                        else:
                                keystone.users.create(name=user_name, password=password, email=email, enabled=enable)

                user_id = form.getvalue("id")
                if user_id != None:
                        keystone.users.delete(user_id)
		#############################

		userlist =  keystone.users.list() # List users

		self.addContent('<table border="1"><tr><th>Name</th><th>ID</th><th>Email</th><th>Enabled</th><th>Delete</th></tr>')

		for i in range(len(userlist)):
			self.addContent('<tr>')
		        self.addContent('<td>' + userlist[i].name + '</td>')
		        self.addContent('<td>' + userlist[i].id + '</td>')
			self.addContent('<td>' + str(userlist[i].email) + '</td>')
			if userlist[i].enabled == True:
				self.addContent('<td> True  </td>')
			else:
				self.addContent('<td> False </td>')
			self.addContent('<td> <form action="users.cgi" method="post"> <button type="submit" name="id" value="' + userlist[i].id + '">Delete</button></form>  </td>')
			self.addContent('</tr>')		
		self.addContent('</table>')				



		self.addContent('<br><b>Add User:</b><br>')
		self.addContent('''<form action="users.cgi" method="post">
				<b>Name: </b><input type="text" name="name" />
				<b>Password: </b><input type="text" name="password" />
				<b>Email: </b><input type="text" name="email" />
				<b>Enabled: </b><input type="checkbox" name="enabled" value="true">
				<input type="submit" name="bsubmit" />
				</form>''');

		#self.addContent('<b>Delete User:</b><br>')
		#self.addContent('''<form action="users.cgi" method="post">
                #                <b>User ID: </b><input type="text" name="id" />
                #                <input type="submit" name="bsubmit" />
                #                </form>''');



Page = Users()
