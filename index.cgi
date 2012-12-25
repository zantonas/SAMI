#!/usr/bin/env python
from components import Page
import os

def get_page_url_name():
	return os.environ['REQUEST_URI'].split('/')[2].lower()



print "Content-type: text/html\n\n";


page = Page(get_page_url_name())

