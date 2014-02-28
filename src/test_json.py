#!/usr/bin/python

# Forecast Parser Test
#	Created By:	Ruslan Kolesnik, Caleb Hellickson, Ignacio Saez Lahildalga, Mike Moss
#	Modified On:	02/27/2014

import json
import datetime
from forecast_parser import parse
from voluptuous import Schema, Required, All, Length, Range, MultipleInvalid, Invalid

class Test_json:
	# Keeps track of number of failed tests
	failed_tests = 0;
	error_string = "";

	def __init__ (self, json_string):
		self.json_string = json_string;

		# Test if the given string is valid json
		try:
			json.loads(json_string);
		except ValueError as err:
			# Invalid JSON
			self.print_error("Invalid json string (" + str(err)+").");
			return;

		# Parse json string
		self.json_object = json.loads (json_string);


	def print_error (self, error_msg):
		Test_json.error_string += error_msg + "\n";
		Test_json.failed_tests += 1;


	# Test if square brackets are used correctly in json string
	def test_brackets (self):
		if self.json_string[0] != '[' or self.json_string[-1] != ']':
			self.print_error ("First and last characters of the json string must be '[' and ']' respectively.");

		number_of_sbrackets = 0;
		for char in self.json_string:
			if char == '[' or char == ']':
				number_of_sbrackets += 1;
		if number_of_sbrackets > 2:
			self.print_error ("Too many square brackets in json string.");


	# Test json string using schema
	def test_with_schema (self):

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
		for dictionary in self.json_object:
			counter += 1;
			try:
				schema(dictionary);
			except MultipleInvalid as e:
				exc = e;
				self.print_error("Object " + str(counter) + " in json string) " + str(exc)+".");

def test_json_string (json_string):
	if json_string == "Cannot determine which prediction page":
		Test_json.error_string += "Cannot determine which prediction page";
		return (False, Test_json.error_string);

	test = Test_json(json_string);
	test.test_brackets();

	# Invalid json string can't run other tests because other tests are dependent on this one
	if(Test_json.failed_tests == 0):
		test.test_with_schema();

	passed=True;
	Test_json.error_string="No errors.";

	if Test_json.failed_tests != 0:
		passed=False;
		Test_json.error_string = str(Test_json.failed_tests);


	return (True, Test_json.error_string);

