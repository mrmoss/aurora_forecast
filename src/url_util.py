#!/usr/bin/python

#URL Utility Library Source
#	Created By:		Mike Moss
#	Modified On:	02/15/2014

#Time Library
import time;

#URL Library
import urllib2;

#Get URL Function (Makes a GET request, returns bytes on success, returns "" on failure.)
def get_url(link):
	try:
		request=urllib2.urlopen(time.strftime(link));
		return request.read();

	except:
		return "";