#!/usr/bin/python

#File Utility Library Source
#	Created By:		Mike Moss
#	Modified On:	02/15/2014

#File to String Function
def file_to_string(filename):
	try:
		with open(filename,"r") as opened_file:
			return opened_file.read();
	except:
		return "";