#!/usr/bin/python

#JSON Utility Source
#	Created By:		Caleb Hellickson, Ruslan Kolesnik, Ignacio Saez Lahidalga, and Mike Moss
#	Modified On:	03/01/2014

#Date/Time Module
import datetime

#Date Utility Modile
import date_util

#Forecast Parser Module
import forecast_parser

#JSON Module
import json

#Kp Utility Module
import kp_util

#Tests starting and Eending brackets, returns tuple [0](bool)success and [1](string)error_message.
def test_square_brackets(json_string):

	if(len(json_string)>0 and (json_string[0]!='[' or json_string[-1]!=']')):
		return (False,"First and last characters of the json string must be '[' and ']' respectively.")

	return (True,"")

#Tests JSON syntax, returns tuple [0](bool)success and [1](string)error_message.
def test_syntax(json_string):

	#Bad JSON Test
	try:
		json.loads(json_string)

	#Bad JSON
	except ValueError as v:
		 return (False,str(v)+".")

	#Good JSON
	return (True,"")

#Tests Aurora Syntax (for database entries), returns tuple [0](bool)success and [1](string)error_message.
def test_aurora_syntax(json_string):

	try:

		#Create JSON Object
		json_object=json.loads(json_string)

		#Go Through JSON Object
		for ii in range(0,len(json_object)):

			#Test Predicted Date
			predicated_date=json_object[ii]["predicted_time"]

			predicted_date_test=date_util.valid_date(predicated_date["year"],predicated_date["month"],predicated_date["day"],
				predicated_date["hour"],predicated_date["minute"],-1)

			if(predicted_date_test[0]==False):
				return predicted_date_test

			#Test Download Date
			predicated_date=json_object[ii]["download_time"]

			download_date_test=date_util.valid_date(predicated_date["year"],predicated_date["month"],predicated_date["day"],
				predicated_date["hour"],predicated_date["minute"],-1)

			if(download_date_test[0]==False):
				return download_date_test

			#Test Kp
			kp_test=kp_util.valid_kp(json_object[ii]["kp"],-1)

			if(kp_test[0]==False):
				return kp_test

			#Test Forecast
			forecast=json_object[ii]["forecast"]

			if(forecast!="now" and forecast!="h1" and forecast!="d3" and forecast!="d28"):
				return (False,"Invalid forecast \""+forecast+"\" (expected \"now\", \"h1\", \"d3\", or \"d28\").")

	except Exception as e:
		return (False,str(e)[0:].capitalize()+".")

	#Good String
	return (True,"")

#Tests all tests, returns tuple [0](bool)success and [1](string)error_message.
def test_all(json_string):
	return_value=(True,"")

	if(return_value[0]==True):
		return_value=test_square_brackets(json_string)

	if(return_value[0]==True):
		return_value=test_syntax(json_string)

	if(return_value[0]==True):
		return_value=test_aurora_syntax(json_string)

	return return_value