#!/usr/bin/env python

import json
from keystoneclient.v2_0 import client
from swiftclient import Connection


token = 'ADMIN'
endpoint = 'http://10.29.125.11:35357/v2.0/'

keystone = client.Client(token=token, endpoint=endpoint)
tenlist =  keystone.tenants.list() # List tenantus

#for i in range(len(tenlist)):
#	print tenlist[i].name
#	print tenlist[i].id
#	print tenlist[i].description
#	print tenlist[i].enabled
	
user_name='admin'
account_name=''
password='secrete'

conn = ''

for i in range(len(tenlist)):
	
        account_name=tenlist[i].name
	print account_name
        creds=account_name + ':' + user_name
	print creds
	
        conn = Connection(authurl=endpoint, user=creds, key=password, auth_version='2')
        headers = conn.head_account()

        print headers.get('x-account-container-count', 0)
        print headers.get('x-account-object-count', 0)

print "yeboi?"
