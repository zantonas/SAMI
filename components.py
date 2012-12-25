#!/usr/bin/env python
import json


class Page():
	name = ""
	headerp1 = """
		<html>
		<head>
		<title>Swift Interface: """ 

	headerp2 ="""
		</title>
		<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\" />
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
		</div>
		</body>
		</html>
		"""
		
	navigation = None
	
	def __init__(self, name):
		self.name = name
		self.navigation = Navigation()
		if self.name +'.cgi' in self.navigation.scriptmap:
			self.name = self.navigation.scriptmap[self.name+'.cgi']
		elif self.name != '':
			self.name = "ERROR 404"
		self.print_self()
		
		
	def print_self(self):

		print self.headerp1 + self.name + self.headerp2
		self.navigation.print_self()
		print self.pageheaderp1 + self.name + self.pageheaderp2
		print "You are currently browsing the verified " + self.name + " page."
		print content
		print self.footer
		
		

class Navigation():
	scriptmap = {}
	navhtml = ""

	def __init__(self):
		self.navhtml = """
		<div class=\"navigation\">
		<div class="logo">
			<img src=\"./openstack.jpg\" /></br>
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
				self.navhtml += "<div class=\"entry\"><a href=\""+page['script'].split('.')[0]+"\">"+page['name']+"</a></div>"
				self.scriptmap[page['script']] = page['name']
			self.navhtml += "</div>"
				
		
		self.navhtml += "</div>"
	
	def print_self(self):
		print self.navhtml
