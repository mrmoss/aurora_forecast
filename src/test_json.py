#!/usr/bin/python

# Forecast Parser Test
#	Created By:	Ruslan Kolesnik, Caleb Hellickson, Ignacio Saez Lahildalga, Mike Moss
#	Modified On:	02/27/2014

#Date and Time Library
import datetime

#Forecast Parser Library
from forecast_parser import parse

#JSON Library
import json

#Schema Library
from voluptuous import Schema, Required, All, Length, Range, MultipleInvalid, Invalid

#Tests Starting and Ending Brackets, returns tuple (success,error_message).
def test_square_brackets(json_string):
	return_value=(True,"");

	if(len(json_string)>0):
		if(json_string[0] != '[' or json_string[-1] != ']'):
			return_value=(False,"First and last characters of the json string must be '[' and ']' respectively.");

	return return_value;

#Tests Json Syntax, returns tuple (success,error_message).
def test_json_syntax(json_string):
	return_value=(True,"");

	try:
		json.loads(json_string);
	except ValueError as err:
		return_value=(False,str(err)+".");

	return return_value;

#Tests Aurora Syntax (for database entries), returns tuple (success,error_message).
def test_aurora_syntax(json_string):
	return_value=(True,"");
	json_object="";

	try:
		json_object=json.loads(json_string);
	except ValueError as err:
		return_value=(False,str(err)+".");

	if(return_value[0]==True):
		time = {
				Required("year") : All(int, Range(min=1970, max=datetime.datetime.now().year)),
				Required("month") : All(int, Range(min=1, max=12)),
				Required("day") : All(int, Range(min=1, max=31)),
				Required("hour") : All(int, Range(min=-1, max=24)),
				Required("minute") : All(int, Range(min=-1, max=60))
			};

		forecast = All(unicode, Length(min=3, max=5));

		kp = All(int, Range(min=0, max=9));

		schema = Schema({
			Required("time_stamp") : time,
			Required("time_predicted") : time,
			Required("forecast") : forecast,
			Required("kp") : kp
		});

		counter = 0;
		for dictionary in json_object:
			counter += 1;
			try:
				schema(dictionary);
			except MultipleInvalid as e:
				exc = e;
				return_value=(False,"Invalid object at position "+str(counter)+":  "+str(exc)+".");

			if(return_value[0]==False):
				break;

	return return_value;

#JSON Tester (tests all other tests), returns tuple (success,error_message).
def test_json_string (json_string):
	return_value=(True,"");

	if(return_value[0]==True):
		return_value=test_square_brackets(json_string);

	if(return_value[0]==True):
		return_value=test_json_syntax(json_string);

	if(return_value[0]==True):
		return_value=test_aurora_syntax(json_string);

	return return_value;




