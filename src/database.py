#!/usr/bin/python


#mysql python connector library
import MySQLdb as mdb
#system library
import sys
#json library
import json

def store_forecast(jsonObject,host,username,password,database):
	error_str = "";
	stored = False;
	try:
		#Connect to the database
		connect = mdb.connect(host,username,password,database);
		#Create cursor to use separate working environments for the same
		#connection
		cursor = connect.cursor();
		obj = json.loads(jsonObject);
		for ii in obj:
			#if it is a 28 day forecast insert in the 28 day
			if (ii["forecast"]=="28day"):
				when_f = ii["time_stamp"]["year"]+"-"+ii["time_stamp"]["month"]+"-"+ii["time_stamp"]["day"];
				date= ii["time_predicted"]["year"]+"-"+ii["time_predicted"]["month"]+"-"+ii["time_predicted"]["day"];
				kp = ii["kp"];
				cursor.execute("INSERT INTO 28_forecast (date_forecasted,when_was_it_forecasted,kp_value) VALUES("+when_f+", "+date+", "+kp+");");
				   
			#if it is a 3 day forecast insert in the 3 day
			if (ii["forecast"]=="3day"):
				when_f = ii["time_stamp"]["year"]+"-"+
				ii["time_stamp"]["month"]+"-"+ii["time_stamp"]["day"]+" "+ii["time_stamp"]["hour"]+":"+ii["time_stamp"]["minute"]+":"+"00";
				date= ii["time_predicted"]["year"]+"-"ii["time_predicted"]["month"]+"-"++ii["time_predicted"]["day"]+ii["time_stamp"]["day"]+" "+ii["time_stamp"]["hour"]+":"+ii["time_stamp"]["minute"]+":"+"00";
				kp = ii["kp"];
				cursor.execute("INSERT INTO 3_forecast (date_forecasted,when_was_it_forecasted,kp_value) VALUES("+when_f+", "+date+", "+kp+");");
			#if it is a 1 hour insert in the 1 hour
			if (ii["forecast"]=="1hour"):
				when_f = ii["time_stamp"]["year"]+"-"+ii["time_stamp"]["month"]+"-"+ii["time_stamp"]["day"]+" "+ii["time_stamp"]["hour"]+":"+ii["time_stamp"]["minute"]+":"+"00";
				date= ii["time_predicted"]["year"]+"-"ii["time_predicted"]["month"]+"-"+ii["time_predicted"]["day"]+ii["time_stamp"]["day"]+" "+ii["time_stamp"]["hour"]+":"+ii["time_stamp"]["minute"]+":"+"00";
				kp = ii["kp"];
				cursor.execute("INSERT INTO 1_forecast (date_forecasted,when_was_it_forecasted,kp_value) VALUES("+when_f+", "+date+", "+kp+");");
			#if it is a now cast insert in now cast
			if (ii["forecast"]=="now"):
				when_f = ii["time_stamp"]["year"]+"-"+ii["time_stamp"]["month"]+"-"+ii["time_stamp"]["day"]+" "+ii["time_stamp"]["hour"]+":"+ii["time_stamp"]["minute"]+":"+"00";
				date= ii["time_predicted"]["year"]+"-"ii["time_predicted"]["month"]+"-"++ii["time_predicted"]["day"]+ii["time_stamp"]["day"]+" "+ii["time_stamp"]["hour"]+":"+ii["time_stamp"]["minute"]+":"+"00";
				kp = ii["kp"];
				cursor.execute("INSERT INTO nowCast (date_forecasted,when_was_it_forecasted,kp_value) VALUES("+when_f+", "+date+", "+kp+");");
		stored = True;
		cursor.close();
		connect.close();
	except mdb.Error,e:
		error_str = "Error %d: %s" % (e.args[0],e.args[1]);
	return(stored,error_str);