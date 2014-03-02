#!/usr/bin/python

#Date Utiltiy Source
#	Created By:		Mike Moss
#	Modified On:	03/01/2014

#Date/Time Module
import datetime;

#Takes first three letters of a month, returns an integer (1-12) on success, -1 on error.
def month_to_int(month):
	months=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"];

	for ii in range(0,11):
		if(month.lower()==months[ii]):
			return ii+1;

	return -1;

#Takes HHMM formated string, return an integer of HH on success, -1 on error.
def hhmm_to_hour(hhmm):
	if(len(hhmm)==4):
		return int(hhmm[:2]);
	else:
		return -1;

#Takes HHMM formated string, return an integer of MM on success, -1 on error.
def hhmm_to_min(hhmm):
	if(len(hhmm)==4):
		return int(hhmm[-2:]);
	else:
		return -1;

#Takes HH-HHUT formated string, return a tuple containing hours [0](int)HH and [1](int)HH on success, -1 indicates error.
def hhdashhhut_to_hours(hhdashhhut):
	if(len(hhdashhhut)==7):
		return (int(hhdashhhut[0:2]),int(hhdashhhut[3:5]));
	else:
		return (-1,-1);

#Valid Date Function (Tests a date, returns tuple containing [0](bool)passed, [1](str)error).
def valid_date(year,month,day,hour,minute,line):

	#Force Types
	year=int(year);
	month=int(month);
	day=int(day);
	hour=int(hour);
	minute=int(minute);
	line=int(line);

	#Invalid Year Check
	if(year<1970):
		return_string="Invalid year ";
		if(line>0):
			return_string+="on line "+str(line)+" ";
		return_string+=" (expected a value greater than or equal to 1970 and got "+str(year)+").";
		return (False,return_string);

	#Invalid Month Check
	if(month<-1 or month==0 or month>12 or (month==-1 and (day!=-1 or hour!=-1 or minute!=-1))):
		return_string="Invalid month ";
		if(line>0):
			return_string+="on line "+str(line+1)+" ";
		return_string+=" (expected a value between 1 and 12 and got "+str(month)+").";
		return (False,return_string);

	#Invalid Day Check
	if(day<-1 or day==0 or day>31 or (day==-1 and (hour!=-1 or minute!=-1))):
		return_string="Invalid day ";
		if(line>0):
			return_string+="on line "+str(line)+" ";
		return_string+=" (expected a value between 1 and 31 and got "+str(day)+").";
		return (False,return_string);

	#Invalid Hour Check
	if(hour<-1 or hour>23 or (hour==-1 and minute!=-1)):
		return_string="Invalid hour ";
		if(line>0):
			return_string+="on line "+str(line)+" ";
		return_string+=" (expected a value between 0 and 23 and got "+str(hour)+").";
		return (False,return_string);

	#Invalid Minute Check
	if(minute<-1 or minute>59):
		return_string="Invalid minute ";
		if(line>0):
			return_string+="on line "+str(line)+" ";
		return_string+=" (expected a value between 0 and 59 and got "+str(minute)+").";
		return (False,return_string);

	#Good Date
	return (True,"");