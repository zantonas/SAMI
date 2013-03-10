#!/usr/bin/env python

from components import Page
from swiftclient import Connection

import cgi

import json
from keystoneclient.v2_0 import client

class Tenants(Page):
    name = 'Tenant Management'
    policy_types = {"expiry":["expirytype","expiryduration"]}
    quota_types = {"quota-bytes":"Max Bytes", "quota-count":"Max Objects"}
    
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
                #containers {
                    float: left;
                    min-width: 600px;
                }
                #containertable { float: left;}
                .hiddenform {
                    float: left;
                    margin: 10px;
                    border: 1px solid;
                    padding: 2px;
                }
                #content {
                    width: 100%;
                    min-width: 600px;
                }
                #addcontform {
                    clear: both;
                     margin: 10px;
                }
				form {
					float: left;
				}
            </style>
            <script type="text/javascript">
                $(function () {
                    $(".unselectable").each(function() {this.onselectstart = function() { return false; };});
                    
                    
                    $('#policyform').hide();
                    $(".setpolicies").click(function() {
                        $('#quotaform').hide();
                        $('#policyform').show();
                        $('#modcontnamepol').val($(this).val());
                        $('#containerpoledit').text("Setting policy on " + $(this).val());
                    });
                    
                    $('#quotaform').hide();
                    $(".setquotas").click(function() {
                        $('#policyform').hide();
                        $('#quotaform').show();
                        $('#modcontnamequot').val($(this).val());
                        $('#containerquotedit').text("Setting quota on " + $(this).val());
                    });
                    
                    $(".cancelPolicy").click(function () {
                        $('#policyform').hide();
                    });
                    
                    $(".cancelQuota").click(function () {
                        $('#quotaform').hide();
                    });
                    
                    $("#setpolicyform").submit(function(event) {
                        var duration = parseInt($("#expiryduration").val());
                        if(isNaN(duration)) {
                            event.preventDefault();
                            $("#policyerrortext").text("Not a valid number provided for duration!").show().fadeOut(3000);
                        }
                    });
                    
                    $("#setquotaform").submit(function(event) {
                        var max_objs = $("#quotamaxobj").val();
                        var max_bytes = $("#quotamaxbyte").val();
                        var errortxt ="";
                        if(max_objs != "" && isNaN(max_objs)) {
                            errortxt+= "Not a valid number provided for max objects! ";
                        }
                        if(max_bytes != "" && isNaN(max_bytes)) {
                            errortxt+= "Not a valid number provided for max bytes!";
                        }
                        if(max_objs == "" && max_bytes == "") {
                            errortxt+= "No fields set!";
                        }
                        if(errortxt != "") { $("#quotaerrortext").text(errortxt).show().fadeOut(3000); event.preventDefault();}
                    });
					$('#tenanttable').dataTable({"sPaginationType": "full_numbers", "aaSorting": []});
                    $('#containertable').dataTable({"sPaginationType": "full_numbers", "aaSorting": []});
                } );
            </script>
        '''
    
    def generate_tables(self):
        self.addContent('<div id="content">')
        f = open("settings.conf", "r")
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
        
            tenlist = keystone.tenants.list()
            add_ten_perm = ''
            for i in range(len(tenlist)):
                if ten_name == tenlist[i].name:
                    add_ten_perm = tenlist[i].id
                    break
            keystone.tenants.add_user(tenant=add_ten_perm,user=settings[7],role=settings[8])

 
        ten_id = form.getvalue("deltensubmit")
        if ten_id != None:
            keystone.tenants.delete(ten_id)


	enable = form.getvalue("enable")
        if enable != None:
            keystone.tenants.update(tenant_id=enable, enabled=True)
        disable = form.getvalue("disable")
        if disable != None:
            keystone.tenants.update(tenant_id=disable, enabled=False)


        ###################
        tenant_id = form.getvalue('tenant')
        tenlist = keystone.tenants.list()
        

        if tenant_id == None:
            self.addContent('''
			<table id="tenanttable">
				<thead>
					<tr>
						<th>Name</th>
						<th>ID</th>
						<th>description</th>
						<th>Enabled</th>
						<th>Action</th>
					</tr>
				</thead>
				<tbody>''')

            for i in range(len(tenlist)):
                self.addContent('<tr>')
                self.addContent('<td>' + tenlist[i].name + '</td>')
                self.addContent('<td>' + tenlist[i].id + '</td>')
                self.addContent('<td>' + str(tenlist[i].description) + '</td>')
                if tenlist[i].enabled == True:
                    self.addContent('<td>True</td>')
		    self.addContent('<td><form action="tenant.cgi" method="post"> <button type="disable" name="disable" value="' + tenlist[i].id + '">Disable</button></form>')
		    self.addContent('<form action="tenant.cgi" method="get"> <button type="submit" name="tenant" value="'+ tenlist[i].id +'">Modify</button></form>')
                else:
                    self.addContent('<td>False</td>')
		    self.addContent('<td><form action="tenant.cgi" method="post"> <button type="disable" name="enable" value="' + tenlist[i].id + '">Enable</button></form>')
                self.addContent('<form action="tenant.cgi" method="post"> <button type="submit" name="deltensubmit" value="' + tenlist[i].id + '">Delete</button></form>  </td>')
                self.addContent('</tr>')
            self.addContent('''
							</tbody>
                            </table>
							''')
            self.addContent('''
					<div id="addcontform">
					<h2>Add Tenant:</h2>
					<form action="tenant.cgi" method="post">
                        Name: <input type="text" name="name" />
                        Description: <input type="text" name="description" />
                        Enabled: <input type="checkbox" name="enabled" value="true">
                        <input type="submit" name="addtensubmit" />
					</form>
					</div>''')

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
                    conn.post_container(add_cont_name, {("X-Container-Read"):settings[9]})
                    conn.post_container(add_cont_name, {("X-Container-Write"):settings[9]})

                del_cont_name = form.getvalue("delcontname")
                if del_cont_name != None:
                    conn.delete_container(del_cont_name)
                
                mod_cont_name = form.getvalue("modcontname")
                if mod_cont_name != None:
                    mod_cont_pol_type = form.getvalue("policytype")
                    del_cont_pol_type = form.getvalue("delpolicytype")
                    mod_cont_quot_byte = form.getvalue("quotamaxbyte")
                    mod_cont_quot_obj = form.getvalue("quotamaxobj")
                    del_cont_quot_type = form.getvalue("delquotatype")

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
                    elif mod_cont_quot_byte != None or mod_cont_quot_obj != None:
                        quot_headers = {}
                        if mod_cont_quot_byte != None:
                            quot_headers.update({"X-Container-Meta-Quota-Bytes":mod_cont_quot_byte})
                        if mod_cont_quot_obj != None:
                            quot_headers.update({"X-Container-Meta-Quota-Count":mod_cont_quot_obj})
                        conn.post_container(mod_cont_name, quot_headers)
                    elif del_cont_quot_type != None:
                        if del_cont_quot_type in self.quota_types:
                            conn.post_container(mod_cont_name, {("x-remove-container-meta-"+del_cont_quot_type):""})
                headers, body = conn.get_account()
                ### DEAL WITH A 'NO DATA' RESPONSE CODE

                self.addContent('<h2>Managing Tenant: ' +  account_name + '</h2>')
                self.addContent('<div id="containers">')
                self.addContent('''
                    <table id="containertable">
                    <thead><tr>
                        <th>Containers</th>
                        <th>Quota</th>
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
                    self.addContent('<td>' + self.get_quotas(cont_headers, tenant_id, cont_values[2]) + '</td>')
                    self.addContent('<td>' + self.get_policies(cont_headers, tenant_id, cont_values[2]) +'</td>')
                    self.addContent('''
                                <td>
                                <form action="tenant.cgi?tenant='''+tenant_id+'''" method="post">
                                <button type="button" class="setpolicies" value="''' + cont_values[2] + '''">Set Policies</button>
                                <button type="button" class="setquotas" value="''' + cont_values[2] + '''">Set Quota</button>
                                <button type="submit" name="delcontname" value="''' + cont_values[2] + '''">Delete</button>
                                </form>
                                </td>''')
                    self.addContent('</tr>')
                self.addContent('''
                    </tbody>
                    </table>''')
                #Policy form
                self.addContent('''
                        </div>
                        <div id="policyform" class="hiddenform">
                            <form id="setpolicyform" name="setpolicyform" action="tenant.cgi?tenant='''+tenant_id+'''" method="POST">
                                <input type="hidden" id="modcontnamepol" name="modcontname" value="" />
                                <div id="containerpoledit"> </div>
                                <div>Policy Type: <select name="policytype" id="policytype">
                                    <option value="expiry">Expiry</option>
                                </select></div>
                                <div>Expiry Type: <select name="expirytype" id="expirytype">
                                    <option value="UNTOUCHED">Untouched</option>
                                    <option value="UNMODIFIED">Unmodified</option>
                                    <option value="FIXED">Fixed</option>
                                </select></div>
                                <div>Duration: <input name="expiryduration" id="expiryduration" type="textbox"/></div>
                                <div><input class="setpolicy" type="submit" value="Set Policy"/>
                                <input class="cancelpolicy" type="button" value="Cancel"/></div>
                            </form>
                            <div id="policyerrortext"></div>
                        </div>''')
                
                #Quota form
                self.addContent('''
                        <div id="quotaform" class="hiddenform">
                            <form id="setquotaform" name="setquotaform" action="tenant.cgi?tenant='''+tenant_id+'''" method="POST">
                                <input type="hidden" id="modcontnamequot" name="modcontname" value="" />
                                <div id="containerquotedit"> </div>
                                <div>Max Bytes: <input name="quotamaxbyte" id="quotamaxbyte" type="textbox" size="10"/></div>
                                <div>Max Objects: <input name="quotamaxobj" id="quotamaxobj" type="textbox" size="10"/></div>
                                <div><input class="setquota" type="submit" value="Set Quota"/>
                                <input class="cancelquota" type="button" value="Cancel"/></div>
                            </form>
                            <div id="quotaerrortext"></div>
                        </div>''')
                
                
                self.addContent('''
                                <div id="addcontform">
                                    <h3>Add Container</h3>
                                    <form action="tenant.cgi?tenant='''+tenant_id+'''" method="post">
                                        <b>Container name: </b><input type="text" name="addcontname" />
                                        <input type="submit" name="addcontsubmit" />
                                    </form>
                                </div>

                                ''')

                

    
            else:
                self.addContent('Not a valid tenant_ID')###change this to make it spit out a list of tenants
        self.addContent('</div>')
        
    def get_quotas(self, headers, tenant_id, container):
        quotas = ""
        for qtype in self.quota_types:
            meta = "x-container-meta-" + qtype
            quotas += '<div class="data">' + self.quota_types[qtype]
            if meta in headers:
                quotas += ": " + headers[meta] + "</div>"
                quotas += '''
                    <form id="removequotaform" action="tenant.cgi?tenant='''+tenant_id+'''" method="post">
                        <input type="hidden" name="modcontname" value="'''+container+'''"/>
                        <input type="hidden" name="delquotatype" value="'''+qtype+'''"/>
                        <input type="submit" value="Remove" />
                    </form>'''
            else:
                quotas += ": Not Set</div>"
            quotas += "<br/>"
        return quotas
                
    def get_policies(self, headers, tenant_id, container):
        policies = ""
        for policy_type in self.policy_types:
            meta = "x-container-meta-"+policy_type
            if meta in headers:
                removeform = '''
                    <form id="delpolicyform" action="tenant.cgi?tenant='''+tenant_id+'''" method="post">
                        <input type="hidden" name="modcontname" value="'''+container+'''"/>
                        <input type="hidden" name="delpolicytype" value="'''+policy_type+'''"/>
                        <input type="submit" value="Remove" />
                    </form>'''
                policies += '<div class="data">' + policy_type + ': ' + headers[meta] + '</div>' + removeform
        if policies == "": policies = "No Policies"
        return policies

Page = Tenants()
