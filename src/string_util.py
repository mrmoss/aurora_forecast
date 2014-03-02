#!/usr/bin/python

#String Utiltiy Source
#	Created By:		Mike Moss
#	Modified On:	03/01/2014

#Returns a string with line numbers.
def line_numbered(string):

	#Return Value
	return_value="";

	#Separate Lines
	lines=string.splitlines(True);

	#Add Line Numbers
	for ii in range(0,len(lines)):
		return_value+=str(ii+1)+":\t"+lines[ii];

	#Return New String
	return return_value;