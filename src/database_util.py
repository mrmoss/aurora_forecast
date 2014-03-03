#!/usr/bin/python

#Database Utility Source
#	Created By:		Ignacio Saez Lahidalga
#	Modified On:	03/02/2014

#MySQL Module
import MySQLdb;

#System Module
import sys;

#JSON Module
import json;

#Insert Forecast Function (Takes forecast information and inserts it into a given MySQL database,
#		returns tuple [0](bool)success and [1](string)error).
def insert_forecast(json_object,host,username,password,database):

	#Test for Errors
	try:
		#Connect to Database
		database=MySQLdb.connect(host,username,password,database);

		#Create cursor to use separate working environments for the same connection
		cursor=database.cursor();

		#Convert JSON Object
		obj=json.loads(json_object);

		#Traverse JSON Object
		for ii in obj:

			#28 Day Forecast
			if(ii["forecast"]=="d28"):

				#Create Entries
				download_time=ii["download_time"]["year"]+"-"+ii["download_time"]["month"]+"-"+ii["download_time"]["day"];
				predicted_time=ii["predicted_time"]["year"]+"-"+ii["predicted_time"]["month"]+"-"+ii["predicted_time"]["day"];
				kp=ii["kp"];

				#Insert into Database
				cursor.execute("INSERT INTO 28_forecast (date_forecasted,when_was_it_forecasted,kp_value) VALUES("+download_time+", "+predicted_time+", "+kp+");");

			#3 Day Forecast
			if(ii["forecast"]=="d3"):

				#Create Entries
				download_time=ii["download_time"]["year"]+"-"+ii["download_time"]["month"]+"-"+ii["download_time"]["day"]+" "+ii["download_time"]["hour"]+":"+ii["download_time"]["minute"]+":"+"00";
				predicted_time=ii["predicted_time"]["year"]+"-"+ii["predicted_time"]["month"]+"-"++ii["predicted_time"]["day"]+ii["download_time"]["day"]+" "+ii["download_time"]["hour"]+":"+ii["download_time"]["minute"]+":"+"00";
				kp=ii["kp"];

				#Insert into Database
				cursor.execute("INSERT INTO 3_forecast (date_forecasted,when_was_it_forecasted,kp_value) VALUES("+download_time+", "+predicted_time+", "+kp+");");

			#1 Hour Forecast
			if(ii["forecast"]=="h1"):

				#Create Entries
				download_time=ii["download_time"]["year"]+"-"+ii["download_time"]["month"]+"-"+ii["download_time"]["day"]+" "+ii["download_time"]["hour"]+":"+ii["download_time"]["minute"]+":"+"00";
				predicted_time=ii["predicted_time"]["year"]+"-"+ii["predicted_time"]["month"]+"-"+ii["predicted_time"]["day"]+ii["download_time"]["day"]+" "+ii["download_time"]["hour"]+":"+ii["download_time"]["minute"]+":"+"00";
				kp=ii["kp"];

				#Insert into Database
				cursor.execute("INSERT INTO 1_forecast (date_forecasted,when_was_it_forecasted,kp_value) VALUES("+download_time+", "+predicted_time+", "+kp+");");

			#Now Forecast
			if(ii["forecast"]=="now"):

				#Create Entries
				download_time=ii["download_time"]["year"]+"-"+ii["download_time"]["month"]+"-"+ii["download_time"]["day"]+" "+ii["download_time"]["hour"]+":"+ii["download_time"]["minute"]+":"+"00";
				predicted_time=ii["predicted_time"]["year"]+"-"+ii["predicted_time"]["month"]+"-"++ii["predicted_time"]["day"]+ii["download_time"]["day"]+" "+ii["download_time"]["hour"]+":"+ii["download_time"]["minute"]+":"+"00";
				kp=ii["kp"];

				#Insert into Database
				cursor.execute("INSERT INTO nowCast (date_forecasted,when_was_it_forecasted,kp_value) VALUES("+download_time+", "+predicted_time+", "+kp+");");

		#Close Cursor
		cursor.close();

		#Close Database
		database.close();

		#Good Insertion
		return(True,"");

	#Bad Insertion
	except Exception as e:
		return (False,str(e)[0:].capitalize()+".");