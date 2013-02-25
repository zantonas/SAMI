#!/usr/bin/env python

from components import Page
from swiftclient import Connection

import cgi

import json
from keystoneclient.v2_0 import client

class Permissions(Page):
	name = 'Permissions Management'
	
	def __init__(self):
		self.generate_tables()
		Page.__init__(self)
		
	def generate_tables(self):

		token = 'ADMIN'
                endpoint = 'http://10.29.125.11:35357/v2.0/'

                keystone = client.Client(token=token, endpoint=endpoint)

		###DEAL WITH POST FIRST
		####################
		form = cgi.FieldStorage()
		
		###################

		tenlist = keystone.tenants.list()
		
                tenant_id = form.getvalue('tenant')

                if tenant_id == None:
			self.addContent('<table border="1"><tr><th>Name</th><th>ID</th><th>description</th><th>Enabled</th><th>Modify</th></tr>')

                        for i in range(len(tenlist)):
                        	self.addContent('<tr>')
                                self.addContent('<td>' + tenlist[i].name + '</td>')
                                self.addContent('<td>' + tenlist[i].id + '</td>')
                                self.addContent('<td>' + str(tenlist[i].description) + '</td>')
                                if tenlist[i].enabled == True:
                                	self.addContent('<td>True</td>')
                                else:
                                        self.addContent('<td>False</td>')
                                        self.addContent('</tr>')
 				self.addContent('<td> <form action="permissions.cgi" method="get"> <button type="submit" name="tenant" value="'+ tenlist[i].id +'">Modify</button></form></td>')
                        self.addContent('</table>')                       
 
                else:
			tenlist = keystone.tenants.list()
			ten_valid = False
			##Ensure that tenant_id is valid (HTTP GET)
			for i in range(len(tenlist)):
				if tenant_id == tenlist[i].id:
					ten_valid = True
					break
			if ten_valid == False:
          		      	self.addContent('Not a valid tenant_ID')###change this to make it spit out a list of tenants					
			else:
				grant_user_id = form.getvalue('grantuserid')
				grant_role_id = form.getvalue('grantroleid')

				if ((grant_user_id != None) and (grant_role_id != None)):
					try:
						keystone.tenants.add_user(tenant=tenant_id,user=grant_user_id,role=grant_role_id)
					except:
						pass
				revoke_user_id = form.getvalue('revokeuserid')
                                revoke_role_id = form.getvalue('revokeroleid')

				if ((revoke_user_id != None) and (revoke_role_id != None)):
                                        try:
						keystone.tenants.remove_user(tenant=tenant_id,user=revoke_user_id,role=revoke_role_id)
					except:
						pass
				userlist =  keystone.tenants.list_users(tenant=tenant_id)
				
				self.addContent('<table border="1"><tr><th>Name</th><th>ID</th><th>Email</th><th>Enabled</th><th>Roles</th></tr>')
				for i in range(len(userlist)):
                        		self.addContent('<tr>')
                        		self.addContent('<td>' + str(userlist[i].name) + '</td>')
                        		self.addContent('<td>' + str(userlist[i].id) + '</td>')
                        		self.addContent('<td>' + str(userlist[i].email) + '</td>')
                        		if userlist[i].enabled == True:
                                		self.addContent('<td> True </td>')
                        		else:
                                		self.addContent('<td> False </td>')
       	                 			self.addContent('</tr>')
					self.addContent('<td>')
					user_roles_list = keystone.users.list_roles(user=userlist[i], tenant=tenant_id)
					for x in range(len(user_roles_list)):
						self.addContent(user_roles_list[x].name)
						if x+1 != len(user_roles_list):
							self.addContent(', ')
					self.addContent('</td>')
		                self.addContent('</table>')
	
				self.addContent('<br><b>Grant permissions:</b><br>')
                                self.addContent('<form action="permissions.cgi?tenant='+tenant_id+'" method="post">')
                                self.addContent('''<b>User: </b><input type="text" name="grantuserid" />''')
				self.addContent('<select name="grantroleid">')
				roles = keystone.roles.list()
				for i in range(len(roles)):
					self.addContent('<option value="' + roles[i].id +'">' + roles[i].name + '</option>')	
				self.addContent('''<input type="submit" name="grantsubmit" /></form>''');


				self.addContent('<br><b>Revoke permissions:</b><br>')
                                self.addContent('<form action="permissions.cgi?tenant='+tenant_id+'" method="post">')
                                self.addContent('''<b>User: </b><input type="text" name="revokeuserid" />''')
                                self.addContent('<select name="revokeroleid">')
                                for i in range(len(roles)):
                                        self.addContent('<option value="' + roles[i].id +'">' + roles[i].name + '</option>')
                                self.addContent('''<input type="submit" name="revokesubmit" /></form>''');


Page = Permissions()
