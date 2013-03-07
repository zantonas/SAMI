#!/usr/bin/env python
from components import Page
import cgi
import json
import os
from  pcap import fetchDrivesInBuilder

class mdrives(Page):
        name = "Drive management"

        def __init__(self):
		self.addContent(self.listDrives())
		self.addContent(self.inputForm())
                Page.__init__(self)

	def listDrives(self):
		return '''
		<b>Object Server</b> <br />
		''' + str(fetchDrivesInBuilder('object')) + ''' <br /><br />
		<b>Account Server</b> <br />
		''' + str(fetchDrivesInBuilder('account')) + ''' <br /><br />
		<b>Container Server</b> <br />
		''' + str(fetchDrivesInBuilder('container'))
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

