#!/usr/bin/python

#Database Utility Source
#	Created By:		Ignacio Saez Lahidalga and Mike Moss
#	Modified On:	03/03/2014

#MySQL Module
import MySQLdb;

#System Module
import sys;

#Convert JSON Date Object to String Date Function
def convert_json_date_to_string_date(json_date):

	#Create String Date
	date_str=str(json_date["year"]);
	date_str+="-"+str(json_date["month"]);
	date_str+="-"+str(json_date["day"]);
	date_str+=" "+str(json_date["hour"]);
	date_str+=":"+str(json_date["minute"]);
	date_str+=":00";

	#Return String Date
	return date_str;

#Insert Forecast Function (Takes forecast information and inserts it into a given MySQL database,
#		returns tuple [0](bool)success and [1](string)error).
def insert_forecast(json_object,host,username,password,database):

	#Test for Errors
	try:
		#Connect to Database
		database=MySQLdb.connect(host,username,password,database);

		#Create cursor to use separate working environments for the same connection
		cursor=database.cursor();

		#Traverse JSON Object
		for ii in json_object:

			#Now Forecast
			if(ii["forecast"]=="now" or ii["forecast"]=="h1" or ii["forecast"]=="d1" or ii["forecast"]=="d28"):

				#Create Entry Values
				forecast=ii["forecast"];
				predicted_time=convert_json_date_to_string_date(ii["predicted_time"]);
				download_time=convert_json_date_to_string_date(ii["download_time"]);
				kp=str(ii["kp"]);

				#Create Insertion Execute String
				execute_str="replace into "+forecast+" values (\""+predicted_time+"\",\""+download_time+"\","+kp+");";

				#Execute Insertion
				cursor.execute(execute_str);

				#Commit Changes
				database.commit();

			#Invalid Forecast
			else:
				return (False,"Invalid forecast.");

		#Close Cursor
		cursor.close();

		#Close Database
		database.close();

		#Good Insertion
		return(True,"");

	#Bad Insertion
	except MySQLdb.Error as e:
		return (False,"MySQL error (\""+str(e[0])+"\") - "+e[1]+".");

	#Something Other Bad Thing Happened
	except Exception as e:
		return (False,str(e)[0:].capitalize()+".");
