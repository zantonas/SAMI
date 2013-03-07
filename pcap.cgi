#!/usr/bin/env python
from components import Page
from reconWrapping import CallRecon
from swiftclient import Connection
from swift.common.ring.ring import Ring
from swift.common.ring.ring import RingData
import json
import os
import cgi
from  pcap import fetchDrivesInBuilder

class Pcap(Page):
	name = "Physical Capacity"

	def __init__(self):
		#self.testZoneThings()
		self.generate_header()
		self.generate_pies()
		self.generate_tables()
		Page.__init__(self)
	
	def testZoneThings(self):
		recon = CallRecon('192.168.1.121', '6010').establishConnection()
                zDrives = fetchDrivesInBuilder("object")
                reconData = {}
		for zone in zDrives:
                        self.addContent("<br/>Zone: " + str(zDrives[zone][0]['zone']))
                        for device in zDrives[zone]:
                                #self.addContent("<br/> Device " + str(device['device']))
				if device['ip'] not in reconData:
                                	reconData[device['ip']] = json.loads(CallRecon(device['ip'], device['port']).establishConnection())
				for reconDevice in reconData:
					#self.addContent("<br/>" + str(reconData[reconDevice]))
					for dev in reconData[reconDevice]:
						if dev['device'] == device['device']:
							device['used'] = dev['used']
							device['size'] = dev['size']
		return reconData	

	def generate_header(self):
		self.headerresources += '''
			<script src="js/jquery-1.9.0.min.js"></script>
			<script src="js/raphael-min.js"></script>
			<script src="js/container-pie.js"></script>
			<script src="js/jquery.dataTables.min.js"></script>
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
					$('#zonetotaltable').dataTable({"sPaginationType": "full_numbers"});
					$('#zonetable').dataTable({"sPaginationType": "full_numbers"});
					
					var pies = [
						{"holder":"pie1","datatable":"#systemtable","title":"System Capacity"},
						{"holder":"pie3","datatable":"#zonetable","title":"Disk Capacity"},
						{"holder":"pie2","datatable":"#zonetotaltable","title":"Zone Capacity"}
					];
					
					$.each(pies, createPie);
				} );
			</script>
			'''
	
	def generate_pies(self):
		self.addContent('''
			<div class="piestrip">
				<div id="pie3" class="piechart"></div>
				<div id="pie1" class="piechart"></div>
				<div id="pie2" class="piechart"></div>
			</div>''');
	
	def generate_tables(self):
		zoned_devs = fetchDrivesInBuilder("object")
		
		total_capacity = 0
		total_used = 0
		zonetotaltable = '''
		<div class="datatable">
			<h2>Zones</h2>
			<table id="zonetotaltable" class="display">
				<thead><tr>
					<th>Zone</th>
					<th>Used</th>
					<th>Free</th>
					<th>Total</th>
				</tr></thead>
				<tbody>
			'''
			
		form = cgi.FieldStorage()
		selected_zone = form.getvalue('zone', "")
		zonetablebody = ""
		total_sys_capacity = 0
		total_sys_used = 0
		for zone in zoned_devs:
			if selected_zone == "":
				selected_zone = str(zone)
			total_zone_capacity = 0
			for device in zoned_devs[zone]:
				total_zone_capacity += device["size"]
				total_used += device["used"]
				if selected_zone == str(zone):
					zonetablebody += '''
							<tr>
								<td>'''+device["ip"]+"/"+device["device"]+'''</td>
								<td>'''+str(device["used"])+'''</td>
								<td>'''+str(device["size"]-device["used"])+'''</td>
								<td>'''+str(device["size"])+'''</td>
							</tr>'''
			zonetotaltable += '''
							<tr class="'''+("row_selected" if (selected_zone==str(zone)) else "")+'''" onclick=\"document.location =\'?zone='''+str(zone)+'''\';\">
								<td>'''+str(zone)+'''</td>
								<td>'''+str(total_used)+'''</td>
								<td>'''+str(total_zone_capacity - total_used)+'''</td>
								<td>'''+str(total_zone_capacity)+'''</td>
							</tr>'''
			total_sys_capacity += total_zone_capacity
			total_sys_used += total_used
		zonetotaltable += '''
					</tbody>
				</table>
				</div>
				'''
				

		self.addContent('''
				<table id="systemtable" style="display:none;" >
					<thead><tr>
						<th></th>
						<th></th>
					</tr></thead>
					<tbody>
						<tr><td>Total Used</td><td>'''+str(total_sys_used)+'''</td></tr>
						<tr><td>Total Available</td><td>'''+str(total_sys_capacity - total_sys_used)+'''</td></tr>
					</tbody>
				</table>
				''');
		
		self.addContent(zonetotaltable)
		
		self.addContent('''
		<div class="datatable">
			<h2>Zone: '''+str(selected_zone)+'''</h2>
			<table id="zonetable">
				<thead><tr>
					<th>Zone</th>
					<th>Used</th>
					<th>Free</th>
					<th>Total</th>
				</tr></thead>
				<tbody>
			''' + zonetablebody + '''
				</tbody>
			</table>
		</div>	
			''')
		
	def fetchDrives(self, zone):
		iZone = int(zone) #Is this how casting shit works?
		conf = {}
		try:
			swift_dir = conf.get('swift_dir', '/etc/swift')
		except:
			os.system("sudo /bin/chmod 710 /etc/swift/")
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
		try:
			swift_dir = conf.get('swift_dir', '/etc/swift')
		except:
			os.system("sudo /bin/chmod 710 /etc/swift/")
			swift_dir = conf.get('swift_dir', '/etc/swift')
				
		self.object_ring = Ring(swift_dir, ring_name='object')
		device_list = self.object_ring.devs
		zoned_devs = dict()
		reconData = {}
		for iDev in device_list[:]:
			if iDev is not None:
				if iDev['zone'] in zoned_devs:
					zoned_devs[iDev['zone']].append(iDev)
				else:
					zoned_devs[iDev['zone']] = [iDev]
					if iDev['ip'] not in reconData:
						reconData[iDev['ip']] = json.loads(CallRecon(iDev['ip'], iDev['port']).establishConnection())
						for reconDevice in reconData:
								for dev in reconData[reconDevice]:
										if dev['device'] == iDev['device']:
												iDev['used'] = dev['used']
												iDev['size'] = dev['size']
		return zoned_devs

	def fetchDrivesInBuilder(self, builder):
                conf = {}
                swift_dir = conf.get('swift_dir', '/etc/swift')
                self.object_ring = Ring(swift_dir, ring_name=builder)
                device_list = self.object_ring.devs
                zoned_devs = dict()
                reconData = {}
                for iDev in device_list[:]:
                        if iDev['zone'] in zoned_devs:
                                zoned_devs[iDev['zone']].append(iDev)
                        else:
                                zoned_devs[iDev['zone']] = [iDev]
                                if iDev['ip'] not in reconData:
                                        reconData[iDev['ip']] = json.loads(CallRecon(iDev['ip'], iDev['port']).establishConnection())
                                for reconDevice in reconData:
                                        for dev in reconData[reconDevice]:
                                                if dev['device'] == iDev['device']:
                                                        iDev['used'] = dev['used']
                                                        iDev['size'] = dev['size']
                return zoned_devs
	
			 
	def fetchAllDriveUsage(self):
		pass
page = Pcap()
