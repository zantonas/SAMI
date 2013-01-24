#!/usr/bin/env python
from components import Page
from swiftclient import Connection
from swift.common.ring.ring import Ring
from swift.common.ring.ring import RingData

class Pcap(Page):
	name = "Physical Capacity"

	def __init__(self):
		self.headerresources += '''
			<script src="/js/jquery-1.9.0.min.js"></script>
			<script src="/js/raphael-min.js"></script>
			<script src="/js/container-pie.js"></script>
			<script src="/js/jquery.dataTables.min.js"></script>
			<style media="screen"> 	#holder {     margin: -350px 0 0 -350px;  width: 700px; height: 700px;}</style>
			<link rel="stylesheet" href="css/jquery.dataTables.css" media="screen">
			<link rel="stylesheet" href="css/pie.css" media="screen">
			<style type="text/css">
				.zone {
					margin: 40px 0;
				}
				.unselectable{
					-moz-user-select:none;
					-khtml-user-select: none;
					cursor: hand; cursor: pointer;
				}
				.expander {
					float: left;
					margin: 0 20px;
				}
			</style>
			<script type="text/javascript">
				$(function () {
					$(".unselectable").each(function() {this.onselectstart = function() { return false; };});
					$('.zone').each(function( index ) {
						$(this).children('h2').click(function () {
							$table = $(this).parent().children("#table");
								if($table.is(":visible")) {
									$(this).parent().children(".expander").text("+");
								} else {
									$(this).parent().children(".expander").text("-");
								}
							
							$table.toggle('slow');
							
						});
						if(index != 0) { $(this).children("#table").hide();  $(this).children(".expander").text("+");}
					});
					$('table').dataTable({"sPaginationType": "full_numbers"});
					
					var pies = [
						{"holder":"pie1","datatable":"#tenanttable","title":"System Capacity"},
						{"holder":"pie3","datatable":"#zonetable","title":"Disk Capacity"},
						{"holder":"pie2","datatable":"#tenanttable","title":"Zone Capacity"}
					];
					
					$.each(pies, createPie);
				} );
			</script>
			'''
			
		self.generate_pies()
		self.generate_tables()
		Page.__init__(self)
	
	def generate_pies(self):
		self.content += '<div class="piestrip">\n'
		self.content += '<div id="pie3" class="piechart"></div>\n'
		self.content += '<div id="pie1" class="piechart"></div>\n'
		self.content += '<div id="pie2" class="piechart"></div>\n'
		self.content += '</div>\n'
	
	def generate_tables(self):
		zoned_devs = self.fetchAllDrives()
		for zone in zoned_devs:
			self.addContent("<div class=\"zone\">")
			self.addContent("<h2 class=\"expander unselectable\" >-</h2><h2 class=\"unselectable\">Zone " + str(zone) + "</h2>")
			self.addContent("""
				<div id="table">
				<table id="zonetable">
					<thead><tr>
						<th>Device</th>
						<th>Used</th>
						<th>Free</th>
						<th>Total</th>
					</tr></thead>
				<tbody>
				""");
			for device in zoned_devs[zone]:
				self.addContent("""
					<tr>
						<td>"""+device["ip"]+"/"+device["device"]+"""</td>
						<td>TBD</td>
						<td>TBD</td>
						<td>TBD</td>
					</tr>""");
			self.addContent("</tbody></table></div></div>")
			

	def fetchDrives(self, zone):
		iZone = int(zone) #Is this how casting shit works?
		conf = {}
                swift_dir = conf.get('swift_dir', '/etc/swift')
                self.object_ring = Ring(swift_dir, ring_name='object')
		device_list = self.object_ring.devs
		zoned_devs = dict()
                for iDev in device_list[:]:
                        if iDev['zone'] in zoned_devs:
                                zoned_devs[iDev['zone']].append(iDev)
                        else:
                                zoned_devs[iDev['zone']] = [iDev]
		if iZone in zoned_devs:
			return zoned_devs[iZone]
		else:
	
			return '[{}]'
		
	def fetchAllDrives(self):
            	conf = {}
		swift_dir = conf.get('swift_dir', '/etc/swift')
		self.object_ring = Ring(swift_dir, ring_name='object')
		device_list = self.object_ring.devs
		zoned_devs = dict()
		for iDev in device_list[:]:
			if iDev['zone'] in zoned_devs:
				zoned_devs[iDev['zone']].append(iDev)
			else:
				zoned_devs[iDev['zone']] = [iDev]
		return zoned_devs
					 
	def fetchAllDriveUsage(self):
		pass
page = Pcap()
