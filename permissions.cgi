#!/usr/bin/env python

from components import Page
from swiftclient import Connection

import cgi

import json
from keystoneclient.v2_0 import client

class Permissions(Page):
    name = 'Permissions Management'
    
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
            $('#tenants').dataTable({"sPaginationType": "full_numbers", "aaSorting": []});
			$('#usertable').dataTable({"sPaginationType": "full_numbers", "aaSorting": []});
			$('#accesstable').dataTable({"sPaginationType": "full_numbers", "aaSorting": []});
			});</script>'''
        
    def generate_tables(self):

        f = open("settings.conf", "r")
        settings = []
        for line in f:
                settings.append(line.split('\n')[0])

        keystone = client.Client(token=settings[3], endpoint=settings[4])

        ###DEAL WITH POST FIRST
        ####################
        form = cgi.FieldStorage()
        
        tenlist = keystone.tenants.list()
        
        tenant_id = form.getvalue('tenant')
        
	if tenant_id == None:
            self.addContent('''
            <table id="tenants"><thead>
            <tr>
            <th>Name</th>
            <th>ID</th>
            <th>description</th>
            <th>Enabled</th>
            <th>Modify</th>
            </tr></thead><tbody>''')

            for i in range(len(tenlist)):
                self.addContent('<tr>')
                self.addContent('<td>' + tenlist[i].name + '</td>')
                self.addContent('<td>' + tenlist[i].id + '</td>')
                self.addContent('<td>' + str(tenlist[i].description) + '</td>')
		if tenlist[i].enabled != None:
			self.addContent('<td>' + str(tenlist[i].enabled) + '</td>')
			self.addContent('''
                                <td>
                                    <form action="permissions.cgi" method="get">
                                    <button type="submit" name="tenant" value="'''+ tenlist[i].id +'''">Modify</button>
                                    </form>
                                </td</tr>
                                ''')
		else:
			self.addContent('<td>False</td>')
                	self.addContent('<td>N/A</td></tr>')                     
            self.addContent('</tbody></table>')
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
		permission = form.getvalue('permissionsubmit')
		
		if permission == 'Grant':
			grant_permission_user_id = form.getvalue('grantpermissionuserid')
                	grant_permission_role_id = form.getvalue('grantpermissionroleid')
			if ((grant_permission_role_id != None) and (grant_permission_user_id != None)):
                        	try:
                                	keystone.tenants.add_user(tenant=tenant_id,user=grant_permission_user_id,role=grant_permission_role_id)
                        	except:
                            		pass
		elif (permission == 'Revoke'):
			revoke_permission_user_id = form.getvalue('revokepermissionuserid')
                	revoke_permission_role_id = form.getvalue('revokepermissionroleid')
			if ((revoke_permission_role_id != None) and (revoke_permission_user_id != None)):
                        	try:
                        		keystone.tenants.remove_user(tenant=tenant_id,user=revoke_permission_user_id,role=revoke_permission_role_id)
				except:
                            		pass
                
		####TENANT NAME
		self.addContent('<h2>Tenant: '+tenlist[i].name+'</h2>')
                userlist =  keystone.tenants.list_users(tenant=tenant_id)
                self.addContent('<div class="tablesection"><h3>Users:</h3>') 
                self.addContent('<table id="usertable"><thead><tr><th>Name</th><th>Email</th><th>Enabled</th><th>Roles</th></tr></thead><tbody>')
                for i in range(len(userlist)):
                    self.addContent('<tr>')
                    self.addContent('<td>' + str(userlist[i].name) + '</td>')
                    #self.addContent('<td>' + str(userlist[i].id) + '</td>')
                    self.addContent('<td>' + str(userlist[i].email) + '</td>')
                    if userlist[i].enabled == True:
                        self.addContent('<td> True </td>')
                    else:
                        self.addContent('<td> False </td>')
                        self.addContent('</tr>')
                    self.addContent('<td>')
                    user_roles_list = keystone.users.list_roles(user=userlist[i], tenant=tenant_id)
		    self.addContent('<form action="permissions.cgi?tenant='+tenant_id+'" method="post">')
		    self.addContent('<select name="revokepermissionroleid">')
                    for x in range(len(user_roles_list)):
                        self.addContent('<option value="' + user_roles_list[x].id +'">' + user_roles_list[x].name + '</option>')
		    self.addContent('<input type="hidden" name="revokepermissionuserid" value="'+userlist[i].id+'">')
		    self.addContent('''<input type="submit" name="permissionsubmit" value="Revoke" /></form>''');

                    self.addContent('</td>')
                self.addContent('</tbody></table></div>')
		
		#############################
		keyst_users = keystone.users.list()
		self.addContent('<div class="tablesection"><h3>Grant Access:</h3>')
		self.addContent('<table id="accesstable"><thead><tr><th>Name</th><th>Email</th><th>Enabled</th><th>Roles</th></tr></thead><tbody>')
                for i in range(len(keyst_users)):
                    self.addContent('<tr>')
                    self.addContent('<td>' + str(keyst_users[i].name) + '</td>')
                    #self.addContent('<td>' + str(keyst_users[i].id) + '</td>')
                    self.addContent('<td>' + str(keyst_users[i].email) + '</td>')
		    if keyst_users[i].enabled == True:
                        self.addContent('<td> True </td>')
                    else:
                        self.addContent('<td> False </td>')

		    self.addContent('<td> <form action="permissions.cgi?tenant='+tenant_id+'" method="post">')
		    self.addContent('<input type="hidden" name="grantpermissionuserid" value="'+keyst_users[i].id+'">')
		    self.addContent('<select name="grantpermissionroleid">')
		    roles = keystone.roles.list()
		    for x in range(len(roles)):
                    	self.addContent('<option value="' + roles[x].id +'">' + roles[x].name + '</option>')
		    self.addContent('''<input type="submit" name="permissionsubmit" value="Grant" /></form></td>''');
                    self.addContent('</tr>')
                self.addContent('</tbody></table></div>')

Page = Permissions()
