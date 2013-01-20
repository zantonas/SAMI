#!/usr/bin/env python
import Cookie, datetime, random, os
import cgi, cgitb 

print "Content-type: text/html"
validated = False

if "HTTP_COOKIE" in os.environ:
	try:
		cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])["session"].value
		if cookie == "swiftpassword":
			validated = True
	except (Cookie.CookieError, KeyError):
		pass
		
if not validated:
	form = cgi.FieldStorage()
	user = form.getvalue('user')
	password = form.getvalue('password')
	if user == "swift" and password == "password":
		expiration = datetime.datetime.now() + datetime.timedelta(days=30)
		cookie = Cookie.SimpleCookie()
		cookie["session"] = user+password
		print cookie.output()
		validated = True

if validated:
	print "Location: index.cgi"

	
print """
	<html>
	<head>
	<title>Swift Interface: Login</title>
	</head>
	<body>
	"""

print "Please log in"
print """
	<form method="post" action="login.cgi">
	<input id="user" name="user" type="textbox"></input>
	<input name="password" type="textbox"></input>
	<input name="submit" type="submit" value="Login"/>
	</form>
	"""
	
print """
	</body>
	</html>
	"""