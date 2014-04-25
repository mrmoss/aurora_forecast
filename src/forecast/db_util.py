#!/usr/bin/python

#Database Utility Source
#	Created By:		Ignacio Saez Lahidalga and Mike Moss and Caleb Hellickson
#	Modified On:	04/19/2014

#Date Module
import datetime

#Date Utility Modile
import date_util

#MySQL Module
import MySQLdb

#System Module
import sys

#Convert JSON Date Object to String Date Function
def convert_json_date_to_string_date_or_interval(json_date):
	
	if json_date["year"] == -1:
		date_str = "'1970-01-01 00:00:00' and '" + str(datetime.datetime.today().year) + "-12-31 23:59:00'"
		return (date_str,True)

	#Create String Date
	date_str="'"+str(json_date["year"])
	
	if json_date["month"] == -1:
		date_str += "-01-01 00:00:00' and " +date_str+ "-12-31 23:59:00'"
		return (date_str,True)
		
	date_str+="-"+str(json_date["month"])
	
	if json_date["day"] == -1:
		date_str += "-01 00:00:00' and " +date_str+ "-31 23:59:00'"
		return (date_str,True)
		
	date_str+="-"+str(json_date["day"])
	
	if json_date["hour"] == -1:
		date_str += " 00:00:00' and " + date_str+ " 23:59:00'"
		return (date_str,True)
		
	date_str+=" "+str(json_date["hour"])
	
	if json_date["minute"] == -1:
		date_str += ":00:00' and " + date_str + ":59:00'"
		return (date_str,True)
		
	date_str+=":"+str(json_date["minute"])
	date_str+=":00'"

	#Return String Date
	return (date_str,False)

#Convert JSON Date Object to String Date Function
def convert_json_date_to_string_date(json_date):

	#Create String Date
	date_str=str(json_date["year"])
	date_str+="-"+str(json_date["month"])
	date_str+="-"+str(json_date["day"])
	date_str+=" "+str(json_date["hour"])
	date_str+=":"+str(json_date["minute"])
	date_str+=":00"
	return date_str

#Insert Forecast Function (Takes forecast information and inserts it into a given MySQL database,
#		returns tuple [0](bool)success and [1](string)error).
def insert_forecast(json_object,host,username,password,database):

	#Test for Errors
	try:
		#Connect to Database
		database=MySQLdb.connect(host,username,password,database)

		#Create cursor to use separate working environments for the same connection
		cursor=database.cursor()

		#Traverse JSON Object
		for ii in json_object:

			#Create Entry Values
			forecast=ii["forecast"]
			predicted_time=convert_json_date_to_string_date(ii["predicted_time"])
			download_time=convert_json_date_to_string_date(ii["download_time"])
			kp=str(ii["kp"])

			#Create Insertion Execute String
			execute_str="insert into "+forecast+" (predicted_time,download_time,kp) values (\""+predicted_time+"\",\""+download_time+"\","+kp+")"

			#Execute Insertion
			cursor.execute(execute_str)

			#Commit Changes
			database.commit()

		#Close Cursor
		cursor.close()

		#Close Database
		database.close()

		#Good Insertion
		return(True,"")

	#Bad Insertion
	except MySQLdb.Error as e:
		return (False,"MySQL error (\""+str(e[0])+"\") - "+e[1]+".")

	#Something Other Bad Thing Happened
	except Exception as e:
		return (False,str(e)[0:].capitalize()+".")
		
def get_json_date_from_database(json_object):
	#call function to get date string
	date_str = convert_json_date_to_string_date_or_interval(json_object)
	return date_str
	
def retrieve_forecast(json_object,host,username,password,database):
	err_str = ""
	try:
		for ii in json_object:

			#Create Entry Values
			forecast=ii["forecast"]
			
			predicted_time=get_json_date_from_database(ii["predicted_time"])[0]
			newCommand=get_json_date_from_database(ii["predicted_time"])[1]
			
			if newCommand:
				sql_command = "Select predicted_time,kp from " +forecast+ " where (predicted_time between " +predicted_time+")"
			else:
				#build mysql command returning a kp
				sql_command = "Select predicted_time,kp from " +forecast+ " where predicted_time="+predicted_time

			#connect to the MariaDB database
			db = MySQLdb.connect(host,username,password,database)

			cursor = db.cursor()
			
			#execute the MySQL command we built
			cursor.execute(sql_command)

			#datas is the tuple we got back from the database
			datas = cursor.fetchall()
			
			#disconnect from the server
			db.close
			#check if there is data or not
			if not datas:
				return (False,"No data exists.")
			
			auxillary = 0
			
			#iterate through datas tuple and get the kp value from our date string
			#for x in range(0,len(datas)):
			
			return_json_object=""
			
			for i in datas:
				temp=(str(i[0]),str(i[1]))
				date_json=date_util.database_date_to_json_date(temp[0])
				return_json_object+='{"predicted_time":'+date_json+',"kp":'+temp[1]+'},'

			return_json_object='{"values":['+return_json_object[0:-1]+']}'
			return (True,return_json_object)

	except Exception,e:
		return (False,"Invalid request."+str(e))

