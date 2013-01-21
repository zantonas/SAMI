#!/usr/bin/env python

from components import Page
from swiftclient import Connection

class Lcap(Page):
	name = 'Logical Capacity'
	
	def __init__(self):
		self.headerresources += '''
			<script src="/js/jquery-1.9.0.min.js"></script>
			<script src="/js/raphael-min.js"></script>
			<script src="/js/container-pie.js"></script>
			<script src="/js/jquery.dataTables.min.js"></script>
			<style media="screen"> 	#holder {     margin: -350px 0 0 -350px;  width: 700px; height: 700px;}</style>
			<link rel="stylesheet" href="css/jquery.dataTables.css" media="screen">
			<link rel="stylesheet" href="css/pie.css" media="screen">
			'''
		self.generate_pies()
		Page.__init__(self)
		
	def generate_pies(self):
		
		self.content += '<div class="piestrip">\n'
		self.content += '<div id="pie3" class="piechart"></div>\n'
		self.content += '<div id="pie1" class="piechart"></div>\n'
		self.content += '<div id="pie2" class="piechart"></div>\n'
		self.content += '</div>\n'
		
		self.content += '<div id="tables">\n'
		tentanttable = '''
			<div id="lefttable">
				<h2>Tenants</h2>
				<table id="tenanttable" class="display">
					<thead><tr>
						<th>Tenant Name</th>
						<th># of Objs</th>
						<th>Total Capacity</th>
					</tr></thead>
				<tbody>
			'''
		containertable = '''
			<div id="righttable">
				<h2>Containers</h2>
				<table id="containertable" class="display">
					<thead><tr>
						<th>Container Name</th>
						<th># of Objs</th>
						<th>Total Capacity</th>
					</tr></thead>
				<tbody>
			'''
		for i in range(150):
			tentanttable += '<tr>'
			tentanttable += '<td>Tenant '+str(i)+'</td>'
			tentanttable += '<td>'+str(i*100)+'</td>'
			tentanttable += '<td>'+str(i*1000)+'</td>'
			tentanttable += '</tr>'
			
			containertable += '<tr>'
			containertable += '<td>Container '+str(i)+'</td>'
			containertable += '<td>'+str(i*100)+'</td>'
			containertable += '<td>'+str(i*1000)+'</td>'
			containertable += '</tr>'
			
		tentanttable += '</tbody></table></div>\n'
		containertable += '</tbody></table></div>\n'
		
		self.content += tentanttable
		self.content += containertable
		self.content += '</div>\n'
		
		user_name='tester'
		account_name='test'
		password='testing'

		creds=account_name + ':' + user_name

		conn = Connection(authurl='http://127.0.0.1:8080/auth/v1.0/', user=creds, key=password)
		headers = conn.head_account()

		total_containers = headers.get('x-account-container-count', 0)
		total_objects = headers.get('x-account-object-count', 0)
		total_bytes = headers.get('x-account-bytes-used', 0)
		'''
		self.content += '<br/> ======================================='
		self.content += '<br/> Tenant: ' + account_name
		self.content += '<br/> ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
		self.content += '<br/> Total containers ' + total_containers
		self.content += '<br/> Total objects ' + total_objects
		self.content += '<br/> Total bytes ' + total_bytes
		'''
		self.content += '<table id="tenantdatatable"><tbody>'
		self.content += '<tr><th scope"row">' + account_name + '\nTotal containers: ' + total_containers + '\nTotal objects: ' + total_objects + '\nTotal bytes: ' + total_bytes + '</th>'
		self.content += '<td>' + total_bytes + '</td>'
		self.content += '</tr>'
		self.content += '<tr><th scope"row">' + account_name + '\nTotal containers: ' + total_containers + '\nTotal objects: ' + total_objects + '\nTotal bytes: ' + total_bytes + '</th>'
		self.content += '<td>' + total_bytes + '</td>'
		self.content += '</tr>'
		self.content += '</tbody></table>'

		body = conn.get_account()
	
		self.content += '<table id="datatable"><tbody>'

	        for x in range(int (total_containers)):
                        cont_inf = body[1][x]
                        cont_values = cont_inf.values()
                        self.content += '<tr>'
                        self.content += '<th scope="row"> ' + cont_values[2] + '\nTotal objects: ' + str (cont_values[0]) + '\nTotal bytes: ' + str (cont_values[1]) + '</th>'
                        self.content += '<td>' + str (cont_values[0]) + '</td>'
			self.content += '</tr>'
		self.content += '</tbody></table>'

		
page = Lcap()

