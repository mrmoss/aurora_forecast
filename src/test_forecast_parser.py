#!/usr/bin/python

# Forecast Parser Test
#	Created By:	Ruslan Kolesnik, Caleb Hellickson, Ignacio Saez Lahildalga, Mike Moss
#	Modified On:	02/21/2014

import json
import datetime
from forecast_parser import parse
from voluptuous import Schema, Required, All, Length, Range, MultipleInvalid, Invalid


	

class Test:
	# Keeps track of number of failed tests
	failed_tests = 0;

	def __init__ (self, json_string):
		# Test if the given string is valid json
		try:
			json.loads(json_string);
		except ValueError as err:
			# Invalid JSON
			self.print_error("FAILED (Invalid json string) " + str(err));
			return;

		# Parse json string
		self.json_object = json.loads (json_string);

		self.json_string = json_string;

	def print_error (self, error_msg):
		print 60 * "-";
		print "\033[1;31m" + error_msg + "\033[1;m";
		Test.failed_tests += 1;

	# Test if square brackets are used correctly in json string
	def test_brackets (self):
		if self.json_string[0] != '[' or self.json_string[-1] != ']':
			self.print_error ("\033[1;31mFAILED (First and last characters of the json string must be '[' and ']' respectively");

		number_of_sbrackets = 0; 
		for char in self.json_string:
			if char == '[' or char == ']':
				number_of_sbrackets += 1;
		if number_of_sbrackets > 2:
			self.print_error ("FAILED (Too many square brackets in json sring");


	# Test if json format matches the decided format
	def test_json_format (self):
		match = {"time_stamp" : {"year" : 2000, "month" : 1, "day" : 1, "hour" : 1, "minute" : 1}, "time_predicted" : {"year" : 2000, "month" : 1, "day" : 1, "hour" : 1, "minute" : 1}, "forecast" : "now", "kp" : 7};
		within_dic = {"year" : 2000, "month" : 1, "day" : 1, "hour" : 1, "minute" : 1};
		
		counter = 0;
		for dictionary in self.json_object:
			counter += 1;
			
			# Check if dictionary has the correct keys
			if dictionary.keys() != match.keys():
				self.print_error ("FAILED (Object " + str(counter) + " in json string has incorrect or missing key)");
				continue;
			
			if type(dictionary['time_stamp']) is not dict:
				self.print_error ("FAILED (Object " + str(counter) + " in json string must contain time_stamp as an object)"); 
			else:
				# Check if dictionary keys within time_stamp dictionary match
				if dictionary['time_stamp'].keys() != within_dic.keys():
					self.print_error ("FAILED (Object " + str(counter) + " in json string has incorrect or missing key with time_stamp object)");

			if type(dictionary['time_predicted']) is not dict:
				self.print_error ("FAILED (Object " + str(counter) + " in json string must contain time_predicted as an object)");
			else:	
				# Check if dictionary keys within time_predicted dictionary match
				if dictionary['time_predicted'].keys() != within_dic.keys():
					self.print_error ("FAILED (Object " + str(counter) + " in json string has incorrect or missing key within time predicted object)");

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
				self.print_error("FAILED (Object " + str(counter) + " in json string) " + str(exc));

			

def test_parser (json_string):
	print json_string;
	if json_string == "Cannot determine which prediction page":
		print 60 * "-";
		print "\033[1;31mFAILED (Cannot determine which prediction page)\033[1;m"
		print 60 * "-";
		return;

	
	test = Test(json_string);
	test.test_brackets();
	# Invalid json string can't run other tests because other tests are dependent on this one
	if(Test.failed_tests == 0):
		test.test_json_format();
		test.test_with_schema();
	
	
	if Test.failed_tests == 0:
		print 60 * "-";
		print "\033[1;32mPASSED all tests\033[1;m"
	else:
		print 60 * "-";
		print "\033[1;31mFAILED", Test.failed_tests, "tests\033[1;m"


	print 60 * "-";
	
def main():
	json_string = parse("2014 Feb 11    150		5	3\n2014 Feb 12	    111		5	2", "28d");
	json_string = '[{"time_stamp" : {"year" : 2000, "month" : 1, "day" : 1, "hour" : 1, "minute" : 1}, "time_predicted" : {"year" : 2000, "month" : 1, "day" : 1, "hour" : 1, "minute" : 1}, "forecast" : "now", "kp" : 7}]';
	test_parser (json_string);
	

	
if __name__ == "__main__":
	main();
	
