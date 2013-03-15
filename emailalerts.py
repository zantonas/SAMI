#!/usr/bin/env python
import httplib
import smtplib
import json
import ast
import os
import argparse
from email.mime.text import MIMEText

parser = argparse.ArgumentParser(description='absolute_path_to_SAMI')
parser.add_argument('SAMI_DIR', type=str)
args=parser.parse_args()
try:
	f = open(args.SAMI_DIR+"alerting.dat", "r")
except:
	print "Please wait for the data to be collected. This will only take a moment."
	quit()	
alerts = []
for line in f:
        alerts.append(line.rstrip())

message = ''
if (alerts[0] == '-') and (alerts[1] == '{}') and (alerts[2] == '-'):
        pass
else:
        message+='Openstack Swift Alert!\n\n'

if alerts[0] != '-':
        unpingable_nodes = alerts[0].split(',')
        message+='Node issues detected!\nThe following Nodes are unpingable:\n\n'
        for ip in range(len(unpingable_nodes)):
                message+= unpingable_nodes[ip] + '\n'
if alerts[1] != '{}':
        unmounted_drives  = ast.literal_eval(str(alerts[1]))
        message+='\nDrive errors detected!\nThe following drives have been automatically unmounted to avoid further issues:\n\n'
        for ip in unmounted_drives:
                for x in range(len(unmounted_drives[ip])):
                        message+= ip + ' --- ' + unmounted_drives[ip][x]['device'] + '\n'

if alerts[2] != '-':
	message+=alerts[2] + '\n'

if message == '':
        print "No errors detected. Cluster is OK"
else:
        print message
        #Creds
	f = open(args.SAMI_DIR+"settings.conf", "r")
        settings = []
        for line in f:
                settings.append(line.split('\n')[0])

        smtpuser = settings[12]
        smtppass = settings[13]

        server = smtplib.SMTP(settings[14],587)
        recipients = settings[15].split(',')
        msg = MIMEText(message)
        msg['Subject'] = "OpenStack Swift Alert!"
        msg['From'] = smtpuser
        msg['To'] = ", ".join(recipients)
        try:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(smtpuser, smtppass)
                server.sendmail(smtpuser,recipients,msg.as_string())
                server.close()
                print "email sent."
        except Exception:
                print "email failed to send."
