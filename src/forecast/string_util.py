#!/usr/bin/python

#String Utiltiy Source
#	Created By:		Mike Moss
#	Modified On:	03/02/2014

#Returns a string with line numbers.
def line_numbered(string):

	#Return Value
	return_value=""

	#Separate Lines
	lines=string.splitlines(True)

	#Add Line Numbers
	for ii in range(0,len(lines)):
		return_value+=str(ii+1)+":\t"+lines[ii]

	#Return New String
	return return_value

#Is Integer Function (Tests if a string is an integer).
def is_int(string):
	try:
		int(string)
		return True

	except ValueError:
		return False

#Is Float Function (Tests if a string is a float).
def is_float(string):
	try:
		float(string)
		return True

	except ValueError:
		return False