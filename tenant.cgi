#!/usr/bin/env python

from components import Page
from swiftclient import Connection

import cgi

import json
from keystoneclient.v2_0 import client

class Tenants(Page):
    name = 'Tenant Management'
    policy_types = {"expiry":["expirytype","expiryduration"]}
    
    def __init__(self):
        self.generate_header()
        self.generate_tables()
        Page.__init__(self)
    
    def generate_header(self):
        self.headerresources += '''
            <script src="js/jquery-1.9.0.min.js"></script>
            <script src="js/jquery.dataTables.min.js"></script>
            <link rel="stylesheet" href="css/jquery.dataTables.css" media="screen">
            <style type="text/css">
                #containertable {
                    float: left;
                }
                #policyform {
                    float: left;
					margin: 10px;
                }
            </style>
            <script type="text/javascript">
                $(function () {
                    $('#policyform').hide();
                    $(".unselectable").each(function() {this.onselectstart = function() { return false; };});
                    $(".setpolicies").click(function() {
                        $('#policyform').show();
                        $('#modcontname').val($(this).val());
                        $('#containeredit').text($(this).val());
                    });
                    $(".setpolicy").click(function() {
                        var duration = parseInt($("#expiryduration").val());
                        if(isNaN(duration)) {
                            $("#errortext").text("Not a valid number provided for duration!").show().fadeOut(1000);
                        } else {
                        $("#setpolicyform").submit();
                        }
                    });
                } );
            </script>
        '''
    
    def generate_tables(self):

	f = open("settings.dat", "r")
        settings = []
        for line in f:
                settings.append(line.split('\n')[0])

        keystone = client.Client(token=settings[3], endpoint=settings[4])

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
            self.addContent('''
                            </table>
                            <br><br><br>
                            <b>Add Tenant:</b>
                            <br>''')
            self.addContent('''<form action="tenant.cgi" method="post">
                        <b>Name: </b><input type="text" name="name" />
                        <b>Description: </b><input type="text" name="description" />
                        <b>Enabled: </b><input type="checkbox" name="enabled" value="true">
                        <input type="submit" name="addtensubmit" />
                        </form>''')

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

                user_name=settings[5]
                password=settings[6]
                account_name=tenant_name
                creds=account_name + ':' + user_name
        
                conn = Connection(authurl=settings[4], user=creds, key=password, auth_version='2')
    
                add_cont_name = form.getvalue("addcontname")            
                if add_cont_name != None:
                    conn.put_container(add_cont_name)

                del_cont_name = form.getvalue("delcontname")
                if del_cont_name != None:
                    conn.delete_container(del_cont_name)
                
                mod_cont_name = form.getvalue("modcontname")
                if mod_cont_name != None:
                    mod_cont_pol_type = form.getvalue("policytype")
                    del_cont_pol_type = form.getvalue("delpolicytype")
                    if mod_cont_pol_type != None:
                        if mod_cont_pol_type in self.policy_types:
                            values = ""
                            sep = ""
                            try: 
                                for field in self.policy_types[mod_cont_pol_type]:
                                    val = form.getvalue(field)
                                    if val != None:
                                        values += sep + str(val)
                                        sep = "-"
                                    else:
                                        raise Exception # incomplete set of fields for policy
                                conn.post_container(mod_cont_name, {("x-container-meta-"+mod_cont_pol_type):values})
                            except Exception:
                                pass
                    elif del_cont_pol_type != None:
                        if del_cont_pol_type in self.policy_types:
                            conn.post_container(mod_cont_name, {("x-remove-container-meta-"+del_cont_pol_type):""})
                headers, body = conn.get_account()
                ### DEAL WITH A 'NO DATA' RESPONSE CODE

                self.addContent('<h2>Managing Tenant: ' +  account_name + '</h2>')
                self.addContent('<div id="containertable">')
                self.addContent('''
                    <table border='1'>
                    <thead><tr>
                        <th>Containers</th>
                        <th>Policies</th>
                        <th>Action</th>
                    </tr></thead>
                    <tbody>''')
                for x in range(len (body)):
                    cont_inf = body[x]
                    cont_values = cont_inf.values()
                    cont_name = cont_values[2]
                    cont_headers, cont_body = conn.get_container(cont_name)
                    self.addContent('<tr>')
                    self.addContent('<td>' + cont_name + '</td>')
                    self.addContent('<td>' + self.get_policies(cont_headers, tenant_id, cont_values[2]) +'</td>')
                    self.addContent('''
                                <td>
                                <form action="tenant.cgi?tenant='''+tenant_id+'''" method="post">
                                <button type="button" class="setpolicies" value="''' + cont_values[2] + '''">Set Policies</button>
                                <button type="submit" name="delcontname" value="''' + cont_values[2] + '''">Delete</button>
                                </form>
                                </td>''')
                    self.addContent('</tr>')
                self.addContent('''
                    </tbody>
                    </table>''')
        
                self.addContent('<br><b>Add Container:</b><br>')
                self.addContent('<form action="tenant.cgi?tenant='+tenant_id+'" method="post">')
                self.addContent('''<b>Container name: </b><input type="text" name="addcontname" />
                                <input type="submit" name="addcontsubmit" />
                                </form>''');
                self.addContent('</div>')

                self.addContent('''
                        <div id="policyform">
                            <form id="setpolicyform" name="setpolicyform">
                                <input type="hidden" id="tenant" name="tenant" value="'''+tenant_id+'''">
                                <input type="hidden" id="modcontname" name="modcontname" value="">
                                <div id="containeredit"> </div>
                                <div>Policy Type: <select name="policytype" id="policytype">
                                    <option value="expiry">Expiry</option>
                                </select></div>
                                <div>Expiry Type: <select name="expirytype" id="expirytype">
                                    <option value="UNTOUCHED">Untouched</option>
                                    <option value="UNMODIFIED">Unmodified</option>
                                    <option value="FIXED">Fixed</option>
                                </select></div>
                                <div>Duration: <input name="expiryduration" id="expiryduration" type="textbox"></input></div>
                                <div><button class="setpolicy" type="button">Set Policy</button></div>
                            </form>
                            <div id="errortext"></div>
                        </div>''')

    
            else:
                self.addContent('Not a valid tenant_ID')###change this to make it spit out a list of tenants

    def get_policies(self, headers, tenant_id, container):
        policies = ""
        for policy_type in self.policy_types:
            meta = "x-container-meta-"+policy_type
            if meta in headers:
                removeurl = '<a href="tenant.cgi?tenant='+tenant_id+'&modcontname='+container+'&delpolicytype='+policy_type+'"> X</a>'
                policies += policy_type + ": " + headers[meta] + removeurl
        return policies
        
Page = Tenants()
