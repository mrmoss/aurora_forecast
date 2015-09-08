#!/usr/bin/python

#Database Utility Source
#	Created By:		Ignacio Saez Lahidalga and Mike Moss and Caleb Hellickson
#	Modified On:	04/25/2014

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

#Insert Carrington Rotation Function (Takes carrington rotation data and inserts it into a given MySQL database,
#		returns tuple [0](bool)success and [1](string)error).
def insert_carrington_rotation(json_object,host,username,password,database):

	#Test for Errors
	try:
		#Connect to Database
		database=MySQLdb.connect(host,username,password,database)

		#Create cursor to use separate working environments for the same connection
		cursor=database.cursor()

		#Traverse JSON Object
		for ii in json_object:

			#Create Entry Values
			year=str(ii["date"]["year"])
			month=str(ii["date"]["month"])
			day=str(ii["date"]["day"])
			rotation_index=str(ii["rotation_index"])

			#Create Insertion Execute String
			execute_str="insert ignore into cr (rotation_index,year,month,day) values (\""+rotation_index+"\",\""+year+"\",\""+month+"\",\""+day+"\")"

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
	try:
		for ii in json_object:

			#Create Entry Values
			forecast=ii["forecast"]

			if(forecast!="now" and forecast!="h1" and forecast!="d3" and forecast!="d28"):
				return (False,"Invalid request."+str(e))

			newest=False

			try:
				newest=ii["newest"]
			except:
				newest=False

			predicted_time=get_json_date_from_database(ii["predicted_time"])[0]
			newCommand=get_json_date_from_database(ii["predicted_time"])[1]

			if newest:
				if newCommand:
					sql_command = "select distinct download_time,predicted_time,kp from "+forecast+" where (predicted_time between " +predicted_time+")"
				else:
					sql_command = "select distinct download_time,predicted_time,kp from "+forecast+" where predicted_time="+predicted_time
			else:
				if newCommand:
					sql_command = "select download_time,predicted_time,kp from "+forecast+" where (predicted_time between " +predicted_time+")"
				else:
					sql_command = "select download_time,predicted_time,kp from "+forecast+" where predicted_time="+predicted_time

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

			#iterate through datas tuple and get the kp value from our date string
			return_json_object=""

			for i in datas:
				download_date_json=date_util.database_date_to_json_date(str(i[0]))
				predicted_date_json=date_util.database_date_to_json_date(str(i[1]))
				return_json_object+='{"download_time":'+download_date_json+','
				return_json_object+='"predicted_time":'+predicted_date_json+','
				return_json_object+='"kp":'+str(i[2])+'},'

			return_json_object='{"values":['+return_json_object[0:-1]+']}'
			return (True,return_json_object)

	except Exception,e:
		return (False,"Invalid request."+str(e))

def retrieve_carrington(json_object,host,username,password,database):
	try:
		for ii in json_object:

			#Create Entry Values
			rotation_index=-1
			year=-1

			rotation_index=-1

			try:
				rotation_index=ii["rotation_index"]
			except:
				rotation_index=-1

			if not isinstance(rotation_index,int) or rotation_index<-1 or rotation_index>9:
				return (False,"Invalid request."+str(e))

			year=-1

			try:
				year=ii["year"]
			except:
				year=-1

			sql_command="select rotation_index,year,month,day from cr where "

			if(not rotation_index==-1):
				sql_command+="rotation_index="+str(rotation_index)

			if(not rotation_index==-1 and not year==-1):
				sql_command+=" and "

			if(not year==-1):
				sql_command+="year="+str(year)

			sql_command+=";"

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

			#iterate through datas tuple
			return_json_object=""

			for i in datas:
				return_json_object+='{"rotation_index":'+str(i[0])+','
				return_json_object+='"year":'+str(i[1])+','
				return_json_object+='"month":'+str(i[2])+','
				return_json_object+='"day":'+str(i[3])+'},'

			return_json_object='{"values":['+return_json_object[0:-1]+']}'
			return (True,return_json_object)

	except Exception,e:
		return (False,"Invalid request."+str(e))

