#!/usr/bin/env python

from components import Page
from swiftclient import Connection

import cgi

import json
from keystoneclient.v2_0 import client

class Tenants(Page):
	name = 'Tenant Management'
	
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
                ten_name = form.getvalue("name")

                if ten_name != None:
                        enable = form.getvalue("enabled")
                        desc = form.getvalue("description")
                        if enable == 'true':
                                keystone.tenants.create(tenant_name=ten_name, description=desc)
                        else:
                                keystone.tenants.create(tenant_name=ten_name, description=desc, enabled=enable)

                ten_id = form.getvalue("id")
                if ten_id != None:
                        keystone.tenants.delete(ten_id)

		###################

		tenlist = keystone.tenants.list()
		
                tenant_id = form.getvalue('tenant')

                if tenant_id == None:
			self.addContent('<table border="1"><tr><th>Name</th><th>ID</th><th>description</th><th>Enabled</th><th>Modify</th><th>Delete</th></tr>')

                        for i in range(len(tenlist)):
                        	self.addContent('<tr>')
                                self.addContent('<td>' + tenlist[i].name + '</td>')
                                self.addContent('<td>' + tenlist[i].id + '</td>')
                                self.addContent('<td>' + str(tenlist[i].description) + '</td>')
                                if tenlist[i].enabled == True:
                                	self.addContent('<td>True</td>')
                                else:
                                        self.addContent('<td>False</td>')
				self.addContent('<td> <form action="tenant.cgi" method="get"> <button type="submit" name="tenant" value="'+ tenlist[i].id +'">Modify</button></form></td>')
                                self.addContent('<td> <form action="tenant.cgi" method="post"> <button type="submit" name="deltensubmit" value="' + tenlist[i].id + '">Delete</button></form>  </td>')
				self.addContent('</tr>')

                        self.addContent('</table>')                       

			self.addContent('<br><br>')


                	self.addContent('<br><b>Add Tenant:</b><br>')
                	self.addContent('''<form action="tenant.cgi" method="post">
                                <b>Name: </b><input type="text" name="name" />
                                <b>Description: </b><input type="text" name="description" />
                                <b>Enabled: </b><input type="checkbox" name="enabled" value="true">
                                <input type="submit" name="addtensubmit" />
                                </form>''');

                	#self.addContent('<b>Delete Tenant:</b><br>')
                	#self.addContent('''<form action="tenant.cgi" method="post">
                        #        <b>Tenant ID: </b><input type="text" name="id" />
                        #        <input type="submit" name="deltensubmit" />
                        #        </form>''');

 
                else:
			tenlist = keystone.tenants.list()
			ten_valid = False
			tenant_name = ''
			##Ensure that tenant_id is valid (HTTP GET)
			for i in range(len(tenlist)):
				if tenant_id == tenlist[i].id:
					ten_valid = True
					tenant_name = tenlist[i].name
					break
			if ten_valid == True:

				user_name='admin'
                		password='secrete'
                		account_name=tenant_name
                		creds=account_name + ':' + user_name
				
        		        conn = Connection(authurl=endpoint, user=creds, key=password, auth_version='2')
	
				add_cont_name = form.getvalue("addcontname")			
				if add_cont_name != None:
					conn.put_container(add_cont_name)

				del_cont_name = form.getvalue("delcontname")
				if del_cont_name != None:
					conn.delete_container(del_cont_name)
				
								
				body = conn.get_account()
				### DEAL WITH A 'NO DATA' RESPONSE CODE

 				self.addContent('<b>' +  account_name + '</b>')
		                self.addContent('''<table border='1'><tr><th>Containers</th><th>Delete</th></tr>''')
                		for x in range(len (body[1])):
                        		cont_inf = body[1][x]
                        		cont_values = cont_inf.values()
                        		self.addContent('<tr>')
                        		self.addContent('<td>' + cont_values[2] + '</td>')
					self.addContent('<td> <form action="tenant.cgi?tenant='+tenant_id+'" method="post"> <button type="submit" name="delcontname" value="' + cont_values[2] + '">Delete</button></form></td>')
                        		self.addContent('</tr>')
	                	self.addContent('</table>')
		
				self.addContent('<br><b>Add Container:</b><br>')
                        	self.addContent('<form action="tenant.cgi?tenant='+tenant_id+'" method="post">')
                                self.addContent('''<b>Container name: </b><input type="text" name="addcontname" />
                                <input type="submit" name="addcontsubmit" />
                                </form>''');


				#self.addContent('<br><b>Delete Container:</b><br>')
                                #self.addContent('<form action="tenant.cgi?tenant='+tenant_id+'" method="post">')
                                #self.addContent('''<b>Container name: </b><input type="text" name="delcontname" />
                                #<input type="submit" name="delcontsubmit" />
                                #</form>''');


								
				###############################

				#LIST CONTAINERS FOR TENANT, ADD CONTAINERS

				#################################
			else:
				self.addContent('Not a valid tenant_ID')###change this to make it spit out a list of tenants


Page = Tenants()
