#!/usr/bin/python

#Kp Utiltiy Source
#	Created By:		Mike Moss
#	Modified On:	03/01/2014

#Valid Kp Function (Tests a kp, returns tuple containing [0](bool)passed, [1](str)error).
def valid_kp(kp,line):
	if(kp<-1 or kp>9):
		return (False,
			"Invalid Kp on line "+str(line)+
			" (expected a value between -1.0 to 9.0 and got "+str(kp)+").")

	#Good Kp
	return (True,"")