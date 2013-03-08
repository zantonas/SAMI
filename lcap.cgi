#!/usr/bin/env python

from components import Page
from swiftclient import Connection

import cgi

import json
from keystoneclient.v2_0 import client

class Lcap(Page):
    name = 'Logical Capacity'
    
    def __init__(self):
        self.headerresources += '''
            <script src="js/jquery-1.9.0.min.js"></script>
            <script src="js/raphael-min.js"></script>
            <script src="js/container-pie.js"></script>
            <script src="js/jquery.dataTables.min.js"></script>
            <style media="screen">  #holder {     margin: -350px 0 0 -350px;  width: 700px; height: 700px;}</style>
            <link rel="stylesheet" href="css/jquery.dataTables.css" media="screen">
            <link rel="stylesheet" href="css/pie.css" media="screen">
            <script type="text/javascript">
                
            $(function () {
                    
					/* Add a click handler to the rows - this could be used as a callback */
					$("#tenanttable tbody").click(function(event) {
						$(oTable.fnSettings().aoData).each(function (){
							$(this.nTr).removeClass('row_selected');
						});
						$(event.target.parentNode).addClass('row_selected');
					});
			
                    oTable = $('#tenanttable').dataTable({"sPaginationType": "full_numbers", "aaSorting": []});
                    //$("#tenanttable table").each(function () {
                    //  $(this).dataTable({"sPaginationType": "full_numbers", "aaSorting": []});
                    //});
                    $('#containertable').dataTable({"sPaginationType": "full_numbers", "aaSorting": []});
                    
                    var pies = [
                        {"holder":"tenantpie","datatable":"#tenanttable","title":"Tenant Pie"},
                        {"holder":"containerpie","datatable":"#containertable","title":"Container Pie"},
                    ];
                    
                    $.each(pies, createPie);
            } );
			
            </script>
            '''
        self.generate_tables()
        Page.__init__(self)
        
    
    def generate_tables(self):

	f = open("settings.conf", "r")
	settings = []
	for line in f:
        	settings.append(line.split('\n')[0])
	

        keystone = client.Client(token=settings[3], endpoint=settings[4])
        tenlist =  keystone.tenants.list() # List tenantus

        user_name=settings[5]
        password=settings[6]

        self.addContent('<div id="tables">\n')
        self.addContent('''
            <div id="tenantpie" class="logicalpie"></div>
            <div class="datatable">
            <h2>Tenants</h2>
                <table id="tenanttable" class="display">
                    <thead><tr>
                            <th>Tenant Name</th>
                                <th># of Objs</th>
                                <th>Total Containers</th>
                                <th>Used Capacity</th>
            </tr></thead>
                        <tbody>
            ''')
                    
        form = cgi.FieldStorage()
        selected_account = form.getvalue('tenant')
        for i in range(len(tenlist)):
           
	    if tenlist[i].enabled == True:
            	account_name = tenlist[i].name
            	creds=account_name + ':' + user_name

            	conn = Connection(authurl=settings[4], user=creds, key=password, auth_version='2')
            
            	headers = conn.head_account()
            
            
            	####NEED TO CATCH RESPONSE CODE HERE - IF NOT 200 THEN RETURN 0,0,0 bytes IN TABLE (AND MARK AS CANNOT READ INFO).

            	total_containers = headers.get('x-account-container-count', 0)
            	total_objects = headers.get('x-account-object-count', 0)
            	total_bytes = headers.get('x-account-bytes-used', 0)
            
            	self.addContent('<tr class="'+("row_selected" if (selected_account==account_name or (selected_account == None and i == 0)) else "")+'" onclick=\"document.location =\'?tenant='+account_name+'\';\">')
            	self.addContent('<td>' + account_name + '</td>')
            	self.addContent('<td>' + str (total_objects) + '</td>')
           	self.addContent('<td>' + str (total_containers) + '</td>')
            	self.addContent('<td>' + str (total_bytes) + '</td>')
            	self.addContent('</tr>')
            	if selected_account == None: selected_account = account_name

        self.addContent('</tbody></table></div>')
        self.addContent('''
                        <div id="containerpie" class="logicalpie"></div>
						<div class="datatable">
                        <h2>Containers</h2>
                        <table id="containertable" class="display">
                            <thead><tr>
                                <th>Container Name</th>
                                <th># of Objs</th>
                                <th>Used Capacity</th>
                            </tr></thead>
                        <tbody>
                    ''')
					

        creds=selected_account + ':' + user_name

        conn = Connection(authurl=settings[4], user=creds, key=password, auth_version='2')

        headers, body = conn.get_account()   

        for x in range(len (body)):
            cont_inf = body[x]
            cont_values = cont_inf.values()
            self.addContent('<tr>')
            self.addContent('<td>' + cont_values[2] + '</td>')
            self.addContent('<td>' + str (cont_values[0]) + '</td>')
            self.addContent('<td>' + str (cont_values[1]) + '</td>')
            self.addContent('</tr>')
        self.addContent('</tbody></table></div>')   

    
Page = Lcap()

