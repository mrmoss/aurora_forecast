#!/usr/bin/python

#Date Utiltiy Source
#	Created By:		Mike Moss
#	Modified On:	03/04/2014

#Date/Time Module
import datetime

#Takes first three letters of a month, returns an integer (1-12) on success, -1 on error.
def month_to_int(month):
	months=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]

	for ii in range(0,11):
		if(month.lower()==months[ii]):
			return ii+1

	return -1

#Takes HHMM formated string, return an integer of HH on success, -1 on error.
def hhmm_to_hour(hhmm):
	if(len(hhmm)==4):
		return int(hhmm[:2])
	else:
		return -1

#Takes HHMM formated string, return an integer of MM on success, -1 on error.
def hhmm_to_min(hhmm):
	if(len(hhmm)==4):
		return int(hhmm[-2:])
	else:
		return -1

#Takes HH-HHUT formated string, return a tuple containing hours [0](int)HH and [1](int)HH on success, -1 indicates error.
def hhdashhhut_to_hours(hhdashhhut):
	if(len(hhdashhhut)==7):
		return (int(hhdashhhut[0:2]),int(hhdashhhut[3:5]))
	else:
		return (-1,-1)

#Valid Date Function (Tests a date, returns tuple containing [0](bool)passed, [1](str)error).
def valid_date(date,line):

	#Force Types
	date["year"]=int(date["year"])
	date["month"]=int(date["month"])
	date["day"]=int(date["day"])
	date["hour"]=int(date["hour"])
	date["hour"]=int(date["hour"])
	line=int(line)

	#Invalid date["year"] Check
	if(date["year"]<1970):
		return_string="Invalid year "
		if(line>0):
			return_string+="on line "+str(line)+" "
		return_string+=" (expected a value greater than or equal to 1970 and got "+str(date["year"])+")."
		return (False,return_string)

	#Invalid date["month"] Check
	if(date["month"]<-1 or date["month"]==0 or date["month"]>12 or (date["month"]==-1 and (date["day"]!=-1 or date["hour"]!=-1 or date["minute"]!=-1))):
		return_string="Invalid month "
		if(line>0):
			return_string+="on line "+str(line+1)+" "
		return_string+=" (expected a value between 1 and 12 and got "+str(date["month"])+")."
		return (False,return_string)

	#Invalid date["day"] Check
	if(date["day"]<-1 or date["day"]==0 or date["day"]>31 or (date["day"]==-1 and (date["hour"]!=-1 or date["minute"]!=-1))):
		return_string="Invalid day "
		if(line>0):
			return_string+="on line "+str(line)+" "
		return_string+=" (expected a value between 1 and 31 and got "+str(date["day"])+")."
		return (False,return_string)

	#Invalid date["hour"] Check
	if(date["hour"]<-1 or date["hour"]>23 or (date["hour"]==-1 and date["minute"]!=-1)):
		return_string="Invalid hour "
		if(line>0):
			return_string+="on line "+str(line)+" "
		return_string+=" (expected a value between 0 and 23 and got "+str(date["hour"])+")."
		return (False,return_string)

	#Invalid date["minute"] Check
	if(date["minute"]<-1 or date["minute"]>59):
		return_string="Invalid minute "
		if(line>0):
			return_string+="on line "+str(line)+" "
		return_string+=" (expected a value between 0 and 59 and got "+str(date["minute"])+")."
		return (False,return_string)

	#Good Date
	return (True,"")