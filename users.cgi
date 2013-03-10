#!/usr/bin/env python

from components import Page
from swiftclient import Connection

import cgi

import json
from keystoneclient.v2_0 import client

class Users(Page):
	name = 'User Management'
	
	def __init__(self):
		self.generate_header()
		self.generate_tables()
		Page.__init__(self)

	def generate_header(self):
	    self.headerresources += '''
            <script src="js/jquery-1.9.0.min.js"></script>
            <script src="js/jquery.dataTables.min.js"></script>
            <link rel="stylesheet" href="css/jquery.dataTables.css" media="screen">
	    <script type="text/javascript">
		$(function () {	
	    $('#usertable').dataTable({"sPaginationType": "full_numbers", "aaSorting": []});});</script>'''
	
	def generate_tables(self):

		f = open("settings.conf", "r")
        	settings = []
        	for line in f:
                	settings.append(line.split('\n')[0])

		keystone = client.Client(token=settings[3], endpoint=settings[4])
		
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
		
		enable = form.getvalue("enable")
		if enable != None:
			keystone.users.update_enabled(user=enable, enabled=True)
		disable = form.getvalue("disable")
		if disable != None:
			keystone.users.update_enabled(user=disable, enabled=False)	

		userlist =  keystone.users.list() # List users

		self.addContent('<table id="usertable"><thead><tr><th>Name</th><th>Email</th><th>Enabled</th><th>Action</th></tr></thead><tbody>')

		for i in range(len(userlist)):
			self.addContent('<tr>')
		        self.addContent('<td>' + userlist[i].name + '</td>')
		        #self.addContent('<td>' + userlist[i].id + '</td>')
			self.addContent('<td>' + str(userlist[i].email) + '</td>')
			if userlist[i].enabled == True:
				self.addContent('<td> True </td>')
				self.addContent('<td><form action="users.cgi" method="post"> <button type="disable" name="disable" value="' + userlist[i].id + '">Disable</button>')
			else:
				self.addContent('<td> False </td>')
				self.addContent('<td><form action="users.cgi" method="post"> <button type="enable" name="enable" value="' + userlist[i].id + '">Enable</button>')
			self.addContent('<button type="submit" name="id" value="' + userlist[i].id + '">Delete</button></form>  </td>')
			self.addContent('</tr>')		
		self.addContent('</tbody></table>')				



		self.addContent('<div class="tablesection"><h3>Add User:</h3>')
		self.addContent('''<form action="users.cgi" method="post">
				<b>Name: </b><input type="text" name="name" />
				<b>Password: </b><input type="text" name="password" />
				<b>Email: </b><input type="text" name="email" />
				<b>Enabled: </b><input type="checkbox" name="enabled" value="true">
				<input type="submit" name="bsubmit" value="Add User"/>
				</form></div>''');


Page = Users()
