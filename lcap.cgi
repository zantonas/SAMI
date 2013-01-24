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
			<script type="text/javascript">
				
			$(function () {

					$('#tenanttable').dataTable({"sPaginationType": "full_numbers"});
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
		self.addContent('<div id="pie2" class="piechart"></div>\n')
		self.addContent('</div>\n');
	
	def generate_tables(self):

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
		self.addContent('<br/> ======================================='
		self.addContent('<br/> Tenant: ' + account_name
		self.addContent('<br/> ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
		self.addContent('<br/> Total containers ' + total_containers
		self.addContent('<br/> Total objects ' + total_objects
		self.addContent('<br/> Total bytes ' + total_bytes
		'''
		
		self.addContent('<div id="tables">\n')
		self.addContent('''
		<div id="lefttable">
			<h2>Tenants</h2>
			<table id="tenanttable" class="display">
				<thead><tr>
					<th>Tenant Name</th>
					<th># of Objs</th>
					<th>Total Capacity</th>
				</tr></thead>
			<tbody>
		''')
		
		self.addContent('<tr>')
		self.addContent('<td>' + account_name + '</td>')
		self.addContent('<td>' + total_objects + '</td>')
		self.addContent('<td>' + total_bytes + '</td>')
		self.addContent('</tr>')
		
		self.addContent('</tbody></table></div>')
		

		body = conn.get_account()
	
		self.addContent('''
		<div id="righttable">
			<h2>Containers</h2>
			<table id="containertable" class="display">
				<thead><tr>
					<th>Container Name</th>
					<th># of Objs</th>
					<th>Total Capacity</th>
				</tr></thead>
			<tbody>
		''')
	        for x in range(int (total_containers)):
					cont_inf = body[1][x]
					cont_values = cont_inf.values()
					self.addContent('<tr>')
					self.addContent('<td>' + cont_values[2] + '</td>')
					self.addContent('<td>' + str (cont_values[0]) + '</td>')
					self.addContent('<td>' + str (cont_values[1]) + '</td>')
					self.addContent('</tr>')
		self.addContent('</tbody></table></div>')
		self.addContent('</div>\n')
		
page = Lcap()

