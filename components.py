#!/usr/bin/env python
import Cookie, datetime, random, os
import json

class Page():
	name = "Dashboard"
	headerp1 = """
		<html>
		<head>
	 	<link rel="stylesheet" href="pie.css"media="screen">
		<title>Swift Interface: 
		"""
	
	headerp2 = """
		</title>
		<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\" />
		"""
	
	headerresources = ""
	
	headerp3 = """
		</head>
		<body>
		"""
	
	
	pageheaderp1 = """
		<div class=\"main\">
		<div class=\"header\">
		<div id="title">
		"""
	pageheaderp2 = """
		</div>
		<div class="systeminfo">System Info</div>
		</div>
		<div class=\"page\">
		"""
	
	content = ""
		
	footer = """
		<div class="footer"></div>
		</div>
		</body>
		</html>
		"""
		
	navigation = None
	
	def __init__(self):
		print "Content-type: text/html"
		if self.auth_check():
			print "\n"
		else:
			print "Location: login.cgi"
		self.navigation = Navigation()
		self.print_self()
		
		
	def print_self(self):
		print self.headerp1 + self.name + self.headerp2 + self.headerresources + self.headerp3
		self.navigation.print_self()
		print self.pageheaderp1 + self.name + self.pageheaderp2
		print self.content
		print self.footer
	
	def auth_check(self):
		if "HTTP_COOKIE" in os.environ:
			try:
				cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])["session"].value
				if cookie == "swiftpassword":
					return True
				else:
					return False
			except (Cookie.CookieError, KeyError):
				return False
		
		

class Navigation():
	scriptmap = {}
	navhtml = ""

	def __init__(self):
		self.navhtml = """
		<div class=\"navigation\">
		<div class="logo">
			<a href="/"><img src=\"./openstack.jpg\" /></a></br>
			Swift Interface
		</div>
		"""
		json_data = open('nav.conf')
		data = json.load(json_data)
		
		for cat in data:
			self.navhtml += """
			<div class="section">
			<div class="section-header">
			"""+cat['name']+"</div>"
			i = 0
			for page in cat['pages']:
				self.navhtml += "<div class=\"entry\"><a href=\""+page['script']+"\">"+page['name']+"</a></div>"
				self.scriptmap[page['script']] = page['name']
			self.navhtml += "</div>"
				
		
		self.navhtml += "</div>"
	
	def print_self(self):
		print self.navhtml
