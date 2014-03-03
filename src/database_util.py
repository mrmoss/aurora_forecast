#!/usr/bin/python

#Database Utility Source
#	Created By:		Mike Moss and Ignacio Saez Lahidalga
#	Modified On:	03/03/2014

#MySQL Module
import MySQLdb;

#System Module
import sys;

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
			if(ii["forecast"]=="now"):

				#Create Entries
				download_time=str(ii["download_time"]["year"]);
				download_time+="-"+str(ii["download_time"]["month"]);
				download_time+="-"+str(ii["download_time"]["day"]);
				download_time+=" "+str(ii["download_time"]["hour"]);
				download_time+=":"+str(ii["download_time"]["minute"]);
				download_time+=":"+"00";

				predicted_time=str(ii["predicted_time"]["year"]);
				predicted_time+="-"+str(ii["predicted_time"]["month"]);
				predicted_time+="-"+str(ii["predicted_time"]["day"]);
				predicted_time+=" "+str(ii["predicted_time"]["hour"]);
				predicted_time+=":"+str(ii["predicted_time"]["minute"]);
				predicted_time+=":"+"00";

				kp=str(ii["kp"]);

				#Insert into Database
				cursor.execute("insert into nowCast (date_forecasted,when_was_it_forecasted,kp_value) VALUES("+download_time+", "+predicted_time+", "+kp+");");

			else:
				return (False,"Invalid forecast.");

		#Close Cursor
		cursor.close();

		#Close Database
		database.close();

		#Good Insertion
		return(True,"");

	#Bad Insertion
	except Exception as e:
		return (False,str(e));

















import forecast_parser;
import json;

data="2014 03 -1  -1-1   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1.00";
lexemes=forecast_parser.lexer_whitespace(data);
json_parse=forecast_parser.parse_now(lexemes);

if(json_parse[0]):
	json_obj=json.loads("["+json_parse[1]+"]");

	insert=insert_forecast(json_obj,"127.0.0.1","root","not_adding_to_git","forecast_db");

	if(insert[0]==False):
		print(insert[1]);
	else:
		print("Worked?!");
