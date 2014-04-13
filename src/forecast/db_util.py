#!/usr/bin/python

#Database Utility Source
#	Created By:		Ignacio Saez Lahidalga and Mike Moss and Caleb Hellickson
#	Modified On:	04/12/2014

#MySQL Module
import MySQLdb

#System Module
import sys

#Convert JSON Date Object to String Date Function
def convert_json_date_to_string_date(json_date):

	#Create String Date
	date_str=str(json_date["year"])
	date_str+="-"+str(json_date["month"])
	date_str+="-"+str(json_date["day"])
	date_str+=" "+str(json_date["hour"])
	date_str+=":"+str(json_date["minute"])
	date_str+=":00"

	#Return String Date
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
    date_str = convert_json_date_to_string_date(json_object)
    return date_str
	
def retreive_from_database(json_object,host,username,password,database):

    for ii in json_object:

        #Create Entry Values
        forecast=ii["forecast"]
        
    predicted_time=get_json_date_from_database(ii["predicted_time"])

	#build mysql command returning a kp
    sql_command = "Select kp from " +forecast+ " where predicted_time="+"'"+predicted_time+"'"

	#connect to the MariaDB database
    db = MySQLdb.connect(host,username,password,database)

    cursor = db.cursor()
	
	#execute the MySQL command we built
    cursor.execute(sql_command)

	#datas is the tuple we got back from the database
    datas = cursor.fetchall()
	
    #disconnect from the server
    db.close
	
	#iterate through datas tuple and get the kp value from our date string
    for i, var in enumerate(datas):
        if i == len(datas) - 1:
            kp = var
	
	#set parsed_kp to float for concatination
    parsed_kp = 0.0
    
    #parse KP	
    for ii in kp:
		
        if ii != "(" or ii !=")" or ii != ",":
			#set parsed kp value to what we want
            parsed_kp += ii	
		
    return parsed_kp
