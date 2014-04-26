#!/usr/bin/python

import cgi
import cr_retriever

request=cgi.FieldStorage().getvalue("r")

print "Content-type: application/json\n\n"

try:
	print cr_retriever.get(request)
except:
	print "{'error:'Invalid request.'}"
