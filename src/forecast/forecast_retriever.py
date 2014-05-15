#!/usr/bin/python

#Forecast Retriever Source
#	Created By:		Paul Gentemann, Caleb Hellickson, Ruslan Kolesnik, Ignacio Saez Lahidalga, and Mike Moss
#	Modified On:	05/04/2014

import config_util
import db_util
import emailer
import file_util
import forecast_parser
import json
import json_util
import signal
import string_util
import sys
import time
import url_util

#Abort Signal Handler Function (Kills program.)
def abort_signal_handler(signal,frame):
	sys.exit(0)

#Error Check Prompt Functions
def error_message_start(message):
	print message,
def error_message_end(success):
	if(success):
		print ":)"
	else:
		print ":("
def error_message_fatal_error():
	print "fatal error - exiting"
	exit()

#Forecast Update Function (Downloads, converts, parses, and updates database returns success).
def get_forecast(link,parser,email_text):

	#Try to Download Data
	data_download=url_util.get_url(link)

	#Failed Data Download
	if(data_download==""):
		emailer.send_email_threaded("Aurora Forecaster Error!!!","The "+email_text+" forecast failed to download!\r\n\r\nDownload Link:\r\n"+time.strftime(link)+"\r\n\r\nAurora Forecaster\r\n\r\n",server_email,receiver_email)
		return (False,"Could not download resource.")

	#Successful Data Download
	else:
		#Convert Downloaded Data
		data_conversion=(False,"Invalid parser \""+parser+"\".")

		if(parser=="now"):
			data_conversion=forecast_parser.parse_now(forecast_parser.lexer_whitespace(data_download))
		elif(parser=="h1"):
			data_conversion=forecast_parser.parse_h1(forecast_parser.lexer_whitespace(data_download))
		elif(parser=="d3"):
			data_conversion=forecast_parser.parse_d3(forecast_parser.lexer_whitespace(data_download))
		elif(parser=="d28"):
			data_conversion=forecast_parser.parse_d28(forecast_parser.lexer_whitespace(data_download))
		elif(parser=="cr"):
			data_conversion=forecast_parser.parse_carrington_rotation(forecast_parser.lexer_whitespace(data_download))

		#Failed Conversion
		if(data_conversion[0]==False):
			emailer.send_email_threaded("Aurora Forecaster Error!!!","The "+email_text+" forecast "+parser+" converter reported an error!\r\n\r\nError Message:\r\n"+data_conversion[1]+"\r\n\r\nDownload Data:\r\n"+string_util.line_numbered(data_download)+"\r\n\r\nAurora Forecaster\r\n\r\n",server_email,receiver_email)
			return data_conversion

		#Successful Conversion
		else:

			#Create JSON String
			json_string="["+data_conversion[1]+"]"

			#Parse Converted Data
			data_json=json_util.test_all(json_string)

			#Carrington Rotation Can Have "Bad" Dates
			if(parser=="cr"):
				data_json=(True,json_string)

			#Failed Parse
			if(data_json[0]==False):
				emailer.send_email_threaded("Aurora Forecaster Error!!!","The "+email_text+" forecast parser reported an error!\r\n\r\nError Message:\r\n"+data_json[1]+"\r\n\r\nParse Data:\r\n"+string_util.line_numbered(json_string)+"\r\n\r\nAurora Forecaster\r\n\r\n",server_email,receiver_email)
				return data_json

			#Successful Parse
			else:

				#Create JSON Object
				json_object=json.loads(json_string)

				#Insert Data
				database_insertion=(False,"")

				if(parser=="cr"):
					database_insertion=db_util.insert_carrington_rotation(json_object,"127.0.0.1",config_util.user,config_util.password,config_util.database)
				else:
					database_insertion=db_util.insert_forecast(json_object,"127.0.0.1",config_util.user,config_util.password,config_util.database)

				#Failed Insertion
				if(database_insertion[0]==False):
					emailer.send_email_threaded("Aurora Forecaster Error!!!","The "+email_text+" forecast database reported an error!\r\n\r\nError Message:\r\n"+database_insertion[1]+"\r\n\r\nAurora Forecaster\r\n\r\n",server_email,receiver_email)

				#Return Result
				return database_insertion

	#This should never happen...
	return (False,"Unknown error occured.")

#Forecast Parser Main
if(__name__=="__main__"):

	#Assign Abort Signal Handler
	signal.signal(signal.SIGINT,abort_signal_handler)

	#Command Line Argument Variables
	error=False
	error_text=""
	show_help=False
	link=""
	forecast=""
	email_text=""
	retrieve_now_cast=False
	retrieve_h1_cast=False
	retrieve_d3_cast=False
	retrieve_d28_cast=False
	retrieve_cr=False

	#No Arguemnts, Show Help
	if(len(sys.argv)<=1):
		show_help=True

	#Go Through Arguments
	for ii in range(1,len(sys.argv)):

		#Help Flag
		if(sys.argv[ii]=="--help"):
			show_help=True
			break

		#Now Cast Flag
		elif(sys.argv[ii]=="--now"):
			retreive_now_cast=True

		#1 Hour Cast Flag
		elif(sys.argv[ii]=="--1-hour"):
			retreive_h1_cast=True

		#3 Day Cast Flag
		elif(sys.argv[ii]=="--3-day"):
			retreive_d3_cast=True

		#28 Day Cast Flag
		elif(sys.argv[ii]=="--28-day"):
			retreive_d28_cast=True

		#Carrington Rotation Flag
		elif(sys.argv[ii]=="--carrington"):
			retrieve_cr=True

		#Other Flags
		else:

			#Set Error Text to Argument
			error_text=sys.argv[ii]

			#If Empty or Just -, Error
			if(len(sys.argv[ii])<=1):
				error=True

			#If No Errors, Check Flag
			if(error==False and sys.argv[ii].startswith("-")):

				#Go Through Check Letters
				for jj in range(1,len(sys.argv[ii])):

					#Now Cast Flag
					if(sys.argv[ii][jj]=="n"):
						retrieve_now_cast=True

					#1 Hour Cast Flag
					elif(sys.argv[ii][jj]=="h"):
						retrieve_h1_cast=True

					#3 Day Cast Flag
					elif(sys.argv[ii][jj]=="d"):
						retrieve_d3_cast=True

					#28 Day Cast Flag
					elif(sys.argv[ii][jj]=="m"):
						retrieve_d28_cast=True

					#Carrington Rotation Flag
					elif(sys.argv[ii][jj]=="c"):
						retrieve_cr=True

					#Unknown Flag
					else:
						error_text="-"+sys.argv[ii][jj]
						error=True
						break

			#Error, Stop Looking Through Arguments
			if(error==True):
				break

	#Error Found
	if(error==True):
		print("Invalid argument \""+error_text+"\".  Use -h or --help for more information.")
		exit(0)

	#Help Flag Set
	if(show_help==True):
		print("Forecast Retreiver usage:")
		print("\t--help\t\t\t\tShow this dialog.")
		print("\t-n, --now\t\t\tSpecify now cast retrieval.")
		print("\t-h, --1-hour\t\t\tSpecify 1 hour cast retrieval.")
		print("\t-d, --3-day\t\t\tSpecify 3 day cast retrieval.")
		print("\t-m, --28-day\t\t\tSpecify 28 day cast retrieval.")
		print("\t-c, --carrington\t\tSpecify carrington rotation retrieval.")
		exit(0)

	#Start Server
	print("Forecast Retriever")

	#Read Configuration File (On failure, write a default configuration file.)
	error_message_start("\tLoading Configuration File\t")

	if(config_util.read_config("forecast_retriever.cfg")==False):
		error_message_end(False)
		exit(0)
	else:
		error_message_end(True)

	#Get Forecasts
	if(retrieve_now_cast==True):
		error_message_start("\tRetrieving Now Cast\t\t")
		error_message_end(get_forecast(config_util.now_forecast_link,"now","now")[0])
	if(retrieve_h1_cast==True):
		error_message_start("\tRetrieving 1 Hour Cast\t\t")
		error_message_end(get_forecast(config_util.h1_forecast_link,"h1","1 hour")[0])
	if(retrieve_d3_cast==True):
		error_message_start("\tRetrieving 3 Day Cast\t\t")
		error_message_end(get_forecast(config_util.d3_forecast_link,"d3","3 day")[0])
	if(retrieve_d28_cast==True):
		error_message_start("\tRetrieving 28 Day Cast\t\t")
		error_message_end(get_forecast(config_util.d28_forecast_link,"d28","28 day")[0])
	if(retrieve_cr==True):
		error_message_start("\tRetrieving Carrington Rotation\t")
		test=get_forecast(config_util.cr_link,"cr","carrington rotation")
		error_message_end(test[0])
		print(test[1])
