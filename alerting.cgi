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

                f = open("alerting.dat", "r")
                alerts = []
                for line in f:
                        alerts.append(line)

                if (alerts[0]== '\n') and (alerts[1] == '{}'):
                        self.addContent('No issues detected. Cluster is OK.')
                else:
                        self.addContent('Openstack Swift Alert!<br><br>')

                if alerts[0] != '\n':
                        unpingable_nodes = alerts[0].split(',')
                        self.addContent('Node issues detected!<br>The following Nodes are unpingable:<br><br>')
                        self.addContent('<table border=1><th>Node IP</th>')
                        for ip in range(len(unpingable_nodes)):
                                self.addContent('<tr><td>' + unpingable_nodes[ip] + '</td></tr>')
                        self.addContent('</table><br>')
                if alerts[1] != '{}':
                        unmounted_drives  = ast.literal_eval(str(alerts[1]))
                        self.addContent('Drive errors detected!<br>The following drives have been automatically unmounted to avoid further issues:<br><br>')
                        for ip in unmounted_drives:
                                self.addContent('<table border=1><th>Node IP</th><th>Disk</th>')
                                for x in range(len(unmounted_drives[ip])):
                                        self.addContent('<tr><td>' + ip + '</td><td>' + unmounted_drives[ip][x]['device'] + '</td><tr>')
                                self.addContent('</table>')


page = Alerting()

