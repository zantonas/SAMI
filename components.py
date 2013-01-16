#!/usr/bin/env python
import json


class Page():
	name = "Dashboard"
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
	
	def __init__(self):
		self.navigation = Navigation()
		self.print_self()
		
		
	def print_self(self):
		print "Content-type: text/html\n\n"
		print self.headerp1 + self.name + self.headerp2
		self.navigation.print_self()
		print self.pageheaderp1 + self.name + self.pageheaderp2
		print "You are currently browsing the verified " + self.name + " page."
		print self.content
		print self.footer
		
		

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
