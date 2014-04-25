#!/usr/bin/python

import cgi
import kp_retriever

request=cgi.FieldStorage().getvalue("r")

print "Content-type: application/json\n\n"

#try:
print kp_retriever.get(request)
#except:
	#print "{'error:'Invalid request.'}"
