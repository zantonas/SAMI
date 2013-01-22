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
	<style type="text/css">
		html, body{
			padding: 0px;
			margin: 0px;
			font-family: Arial;
			font-weight:bold;
		}
		form {
			width:300px;
			padding: 20px;
			position: absolute;
			margin:-150px 0 0 -150px;
			text-align: center;
			top: 50%;
			left: 50%;
			border-style: solid;
			border-color: #888888;
			box-shadow: 10px 10px 5px #888888;
		}

		
	</style>
	</head>
	<body>
	"""

print """
	<form method="post" action="login.cgi">
		<table>
			<thead>Please Log in</thead>
			<tbody>
				<tr>
					<td>Username: </td><td><input id="user" name="user" type="textbox"></input></td>
				</tr>
				<tr>
					<td>Password: </td><td><input name="password" type="password"></input></td>
				</tr>
				<tr>
					<td></td>
					<td><input name="submit" type="submit" value="Login"/></td>
				</tr>
			</tbody>
		</table>
	</form>
	"""
	
print """
	</body>
	</html>
	"""