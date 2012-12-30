#!/usr/bin/env python
from components import Page
import os

def get_script_name():
	return os.environ['REQUEST_URI'].split('/')[2].lower()



print "Content-type: text/html\n\n";

#IMPORTANT TODO: MAKE SURE THIS CAN ONLY LOAD SCRIPTS WE WANT IT TO LOAD
script = get_script_name()

if script == '':
	page = Page()
else:
	try:
	   with open(script+".py") as f: pass # Check if script exists
	   __import__(script) # Load Script
	except IOError as e:
	   print '404.'

   

