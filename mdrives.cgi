#!/usr/bin/env python
from components import Page
import cgi
import json
import os
import pcap

class mdrives(Page):
        name = "Drive management"

        def __init__(self):
		self.runPyFunc(cgi.FieldStorage())
		self.addContent(self.listDrives())
		self.addContent(self.inputForm())
                Page.__init__(self)
	
	def runPyFunc(self, args):
		if "pyFunc" in args:
			py_func = args["pyFunc"].value.split("_")
			if py_func[0] == "delete":
				retval = pcap.removeDrive(py_func[1], py_func[2], py_func[3])
				if retval == 0:
					self.addContent("Device " + str(py_func[2] ) + "/" + str(py_func[3]) + " has been marked for removal. Please rebalance for the changes to take effect<br/>")
				else:
					self.addContent("Something may have gone wrong. Perhaps rebanace the " + str(py_func[1]) + " server.<br/>")
				return retval
			if py_func[0] == "rebalance":
				retval =  pcap.rebalance(py_func[1])
				if retval == 0:
					self.addContent( str(py_func[1]) + " rebalanced successfully.<br/>")
				else:
					self.addContent("Too early to reballance " + str(py_func[1]) + "<br/>")
				return retval
		return ""

	def listDrives(self):
		object_drive = pcap.drivesInBuilder("object")
		account_drive = pcap.drivesInBuilder("account")
		container_drive = pcap.drivesInBuilder("container")
		return '''
		<b>Object Server</b> <form method="post"><button name="pyFunc" value="rebalance_object" type="submit">Rebalance</button></form> <br /> ''' + self.generateTables(object_drive, "object") + '''
		<b>Account Server</b> <form method="post"><button name="pyFunc" value="rebalance_account" type="submit">Rebalance</button></form> <br /> ''' + self.generateTables(account_drive, "account") + '''
		<b>Container Server</b> <form method="post"><button name="pyFunc" value="rebalance_container" type="submit">Rebalance</button></form><br /> ''' + self.generateTables(container_drive, "container")

	def generateTables(self, drive, builder):
		table_rows = ""
                for d in drive:
                        table_rows = table_rows + '''
                                <tr>
                                        <td>%(zone)s</td>
                                        <td>%(ip address)s</td>
                                        <td>%(port)s</td>
					<td>%(name)s</td>
					<td>%(weight)s</td>
					<td>%(balance)s</td>
                                        <td><form method="post">
                                                <button name="pyFunc" value="delete_''' % d + builder + '''_%(ip address)s_%(name)s" type="submit">Delete</button>
                                        </form></td>
                                </tr>''' % d
                return '''
		<table border="1">
                        <tr>
                                <th>Zone</th>
                                <th>IP</th>
                                <th>Port</th>
				<th>Name</th>
				<th>Weight</th>
				<th>Balance</th>
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

