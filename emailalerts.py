#!/usr/bin/env python
import httplib
import smtplib
import json
import ast
from email.mime.text import MIMEText

f = open("alerting.dat", "r")
alerts = []
for line in f:
        alerts.append(line)


message = ''
if (alerts[0] == '\n') and (alerts[1] == '{}'):
        pass
else:
        message+='Openstack Swift Alert!\n\n'

if alerts[0] != '\n':
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

if message == '':
        print "No errors detected. Cluster is OK"
else:
        print message
        #Creds
        smtpuser = '[INPUT_USER_EMAIL]'
        smtppass = '[INPUT_USER_PASS]'

        server = smtplib.SMTP('smtp.gmail.com',587)
        recipients = ['[RECIPIENT_EMAIL]', '[RECIPIENT_EMAIL]']
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
