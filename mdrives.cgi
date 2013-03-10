#!/usr/bin/env python
from components import Page
import cgi
import json
import os
import pcap

class mdrives(Page):
        name = "Drive management"

        def __init__(self):
		self.addContent(self.listDrives())
		self.addContent(self.inputForm())
                Page.__init__(self)

	def listDrives(self):
		object_drive = pcap.drivesInBuilder("object")
		account_drive = pcap.drivesInBuilder("account")
		container_drive = pcap.drivesInBuilder("container")
		return '''
		<b>Object Server</b> <br /> ''' + self.generateTables(object_drive) + '''
		<b>Account Server</b> <br /> ''' + self.generateTables(account_drive) + '''
		<b>Container Server</b> <br /> ''' + self.generateTables(container_drive)

	def generateTables(self, drive):
		table_rows = ""
                for d in drive:
                        table_rows = table_rows + '''
                                <tr>
                                        <td>%(zone)s</td>
                                        <td>%(ip address)s</td>
                                        <td>%(port)s</td>
                                        <td>
                                                <button type="button">Delete</button>
                                        </td>
                                </tr>''' % d
                return '''
		<table border="1">
                        <tr>
                                <th>Zone</th>
                                <th>IP</th>
                                <th>Port</th>
                                <th>Delete</th>
                        </tr>
                ''' +  table_rows + ''' </table><br /><br />'''

	def inputForm(self):
		return ''' <hr/> <b> ADD DRIVE </b><br />
		<form action="addDrive.cgi" method="get" target="_blank">
		  
			Weight: <input type="text" name="weight"><br>
		 	Zone: <input type="text" name="zone"><br>
		 	IP: <input type="text" name="ip"><br>			  
		 	Port: <input type="text" name="port"><br>			  
		 	Device: <input type="text" name="device"><br>			  
		 	Meta: <input type="text" name="meta"><br>
			Object server <input type="checkbox" name="objserver"><br>
			Container server <input type="checkbox" name="contserver"><br>
			Account server <input type="checkbox" name="accserver"><br>
		 	<input type="submit" value="Submit">
		</form>
		'''

Page = mdrives()

