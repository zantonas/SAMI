#!/usr/bin/env python

from components import Page
from swiftclient import Connection

import cgi

import json
from keystoneclient.v2_0 import client

class Policies(Page):
	name = 'Policy Management'
	
	def __init__(self):
		self.headerresources += ''
		
		Page.__init__(self)
	
	def generate_page(self):
		token = 'ADMIN'
		endpoint = 'http://10.29.125.11:35357/v2.0/'

		keystone = client.Client(token=token, endpoint=endpoint)
		tenlist =  keystone.tenants.list() # List tenantus

		user_name='admin'
		password='secrete'
		account_name=''		
		creds=account_name + ':' + user_name

Page = Policies()