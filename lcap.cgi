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
                    
                    $('#tenanttable').dataTable({"sPaginationType": "full_numbers"});
                    //$("#tenanttable table").each(function () {
                    //  $(this).dataTable({"sPaginationType": "full_numbers"});
                    //});
                    $('#containertable').dataTable({"sPaginationType": "full_numbers"});
                    
                    var pies = [
                        {"holder":"pie1","datatable":"#tenanttable","title":"Tenant Pie"},
                        {"holder":"pie3","datatable":"#containertable","title":"Container Pie"},
                        {"holder":"pie2","datatable":"#tenanttable","title":"System Pie"}
                    ];
                    
                    $.each(pies, createPie);
            } );

            </script>
            '''
        self.generate_pies()
        self.generate_tables()
        Page.__init__(self)
        
    def generate_pies(self):
        
        self.addContent('<div class="piestrip">\n')
        self.addContent('<div id="pie3" class="piechart"></div>\n')
        self.addContent('<div id="pie1" class="piechart"></div>\n')

        self.addContent('</div>\n');
    
    def generate_tables(self):

        token = 'ADMIN'
        endpoint = 'http://10.29.125.11:35357/v2.0/'

        keystone = client.Client(token=token, endpoint=endpoint)
        tenlist =  keystone.tenants.list() # List tenantus

        user_name='admin'
        password='secrete'
        account_name=''     
        creds=account_name + ':' + user_name
        

        self.addContent('<div id="tables">\n')
        self.addContent('''
            <div id="lefttable">
            <h2>Tenants</h2>
                <table id="tenanttable" class="display">
                    <thead><tr>
                            <th>Tenant Name</th>
                                <th># of Objs</th>
                                <th>Used Capacity</th>
                                <th>Total Containers</th>
            </tr></thead>
                        <tbody>
            ''')
                    
        form = cgi.FieldStorage()
        account_name = form.getvalue('tenant')
        
        if account_name == None:
            creds='demo' + ':' + user_name
        else:
            creds=account_name + ':' + user_name

        conn = Connection(authurl=endpoint, user=creds, key=password, auth_version='2')

        body = conn.get_account()   
        
        for i in range(len(tenlist)):
            
            account_name = tenlist[i].name
            creds=account_name + ':' + user_name
            
            
            conn = Connection(authurl=endpoint, user=creds, key=password, auth_version='2')
            
            headers = conn.head_account()
            
            
            ####NEED TO CATCH RESPONSE CODE HERE - IF NOT 200 THEN RETURN 0,0,0 bytes IN TABLE (AND MARK AS CANNOT READ INFO).

            total_containers = headers.get('x-account-container-count', 0)
            total_objects = headers.get('x-account-object-count', 0)
            total_bytes = headers.get('x-account-bytes-used', 0)
            
            self.addContent('<tr onclick=\"document.location =\'?tenant='+account_name+'\';\">')
            self.addContent('<td>' + account_name + '</td>')
            self.addContent('<td>' + str (total_objects) + '</td>')
            self.addContent('<td>' + str (total_bytes) + '</td>')
            self.addContent('<td>' + str (total_containers) + '</td>')
            self.addContent('</tr>')



        self.addContent('</tbody></table></div>')
        self.addContent('''
                        <h2>Containers</h2>
                        <table id="containertable" class="display">
                            <thead><tr>
                                <th>Container Name</th>
                                <th># of Objs</th>
                                <th>Used Capacity</th>
                            </tr></thead>
                        <tbody>
                    ''')

        for x in range(len (body[1])):
            cont_inf = body[1][x]
            cont_values = cont_inf.values()
            self.addContent('<tr>')
            self.addContent('<td>' + cont_values[2] + '</td>')
            self.addContent('<td>' + str (cont_values[0]) + '</td>')
            self.addContent('<td>' + str (cont_values[1]) + '</td>')
            self.addContent('</tr>')
        self.addContent('</tbody></table>')   

    
Page = Lcap()

