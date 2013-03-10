#!/usr/bin/env python
from components import Page
import json
import ast

class Alerting(Page):
        name = "Alerting"

        def __init__(self):
                self.establishConnection()
                Page.__init__(self)
        def establishConnection(self):
		try:
		        f = open("alerting.dat", "r")
		except:
			self.addContent('No data is availible. <b>Have you set up a cron job to run alerting.py?</b><br><b>If you have</b>, it may be that data is currently being gathered. Please wait a moment before refreshing the page.')
			return
		alerts = []
	        for line in f:
       	            	alerts.append(line.rstrip())

                if (alerts[0]== '-') and (alerts[1] == '{}') and (alerts[2] == '-'):
                       	self.addContent('No issues detected. Cluster is OK.')
                else:
                       	self.addContent('Openstack Swift Alert!<br><br>')

                if alerts[0] != '-':
                       	unpingable_nodes = alerts[0].split(',')
                       	self.addContent('Node issues detected!<br>The following Nodes are unpingable:<br><br>')
                       	self.addContent('<table border=1><th>Node IP</th>')
                       	for ip in range(len(unpingable_nodes)):
                               	self.addContent('<tr><td>' + unpingable_nodes[ip] + '</td></tr>')
                	self.addContent('</table><br>')
                if alerts[1] != '{}':
                       	unmounted_drives  = ast.literal_eval(str(alerts[1]))
                       	self.addContent('Drive errors detected!<br>The following drives have been automatically unmounted to avoid further issues:<br><br>')
			self.addContent('<table border=1><th>Node IP</th><th>Disk</th>')
                       	for ip in unmounted_drives:
                               	for x in range(len(unmounted_drives[ip])):
                                       	self.addContent('<tr><td>' + ip + '</td><td>' + unmounted_drives[ip][x]['device'] + '</td><tr>')
                        self.addContent('</table><br>')
		if alerts[2] != '-':
			self.addContent('<b>'+alerts[2]+'<b>')

page = Alerting()

