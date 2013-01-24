#!/usr/bin/env python
from components import Page
import httplib
import smtplib
from email.mime.text import MIMEText

conn = httplib.HTTPConnection("127.0.0.1:6000")
conn.request("GET", "/recon/unmounted")
r1 = conn.getresponse()
body = r1.read()	

if body == "[]":
	print "No errors detected. Drives are OK."
else:
	#Creds
	smtpuser = 'INSERT SENDER EMAIL HERE' 
	smtppass = 'INSERT PASSWORD HERE' 

	server = smtplib.SMTP('smtp.gmail.com',587)
	recipients = ['INSERT RECIPIENT EMAIL', 'INSERT RECIPIENT EMAIL', 'INSERT RECIPIENT EMAIL']
	msg = MIMEText("OpenStack Swift Alert! Drive errors detected!\nThe following drives have been automatically unmounted to avoid further issues: \n\n" + body)
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
