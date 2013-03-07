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

        f = open("settings.conf", "r")
        settings = []
        for line in f:
                settings.append(line.split('\n')[0])

        keystone = client.Client(token=settings[3], endpoint=settings[4])

        ###DEAL WITH POST FIRST
        ####################
        form = cgi.FieldStorage()
        
        ###################

        tenlist = keystone.tenants.list()
        
        tenant_id = form.getvalue('tenant')

        if tenant_id == None:
            self.addContent('''
            <table border="1">
            <tr>
            <th>Name</th>
            <th>ID</th>
            <th>description</th>
            <th>Enabled</th>
            <th>Modify</th>
            </tr>''')

            for i in range(len(tenlist)):
                self.addContent('<tr>')
                self.addContent('<td>' + tenlist[i].name + '</td>')
                self.addContent('<td>' + tenlist[i].id + '</td>')
                self.addContent('<td>' + str(tenlist[i].description) + '</td>')
                self.addContent('<td>' + str(tenlist[i].enabled) + '</td>')
                self.addContent('''
                                <td>
                                    <form action="permissions.cgi" method="get">
                                    <button type="submit" name="tenant" value="'''+ tenlist[i].id +'''">Modify</button>
                                    </form>
                                </td>
                                ''')                     
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
                permission = form.getvalue('permission')
                permission_user_id = form.getvalue('permissionuserid')
                permission_role_id = form.getvalue('permissionroleid')
                
                if ((permission_user_id != None) and (permission_role_id != None) and (permission != None)):
                    if permission == 'grant': 
                        try:
                            keystone.tenants.add_user(tenant=tenant_id,user=permission_user_id,role=permission_role_id)
                        except:
                            pass
                    elif permission == 'revoke':
                        try:
                            keystone.tenants.remove_user(tenant=tenant_id,user=permission_user_id,role=permission_role_id)
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
    
                self.addContent('<br><b>Permissions:</b><br>')
                self.addContent('<form action="permissions.cgi?tenant='+tenant_id+'" method="post">')
                self.addContent('<select name="permission"> <option value="grant"> grant </option> <option value="revoke"> revoke </option>')
                self.addContent('''<b>User: </b><input type="text" name="permissionuserid" />''')
                self.addContent('<select name="permissionroleid">')
                roles = keystone.roles.list()
                for i in range(len(roles)):
                    self.addContent('<option value="' + roles[i].id +'">' + roles[i].name + '</option>')    
                self.addContent('''<input type="submit" name="permissionsubmit" /></form>''');


                #self.addContent('<br><b>Revoke permissions:</b><br>')
                                #self.addContent('<form action="permissions.cgi?tenant='+tenant_id+'" method="post">')
                                #self.addContent('''<b>User: </b><input type="text" name="revokeuserid" />''')
                                #self.addContent('<select name="revokeroleid">')
                                #for i in range(len(roles)):
                                #        self.addContent('<option value="' + roles[i].id +'">' + roles[i].name + '</option>')
                                #self.addContent('''<input type="submit" name="revokesubmit" /></form>''');


Page = Permissions()
