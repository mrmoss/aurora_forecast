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
		self.json_string = json_string;

		# Test if the given string is valid json
		try:
			json.loads(json_string);
		except ValueError as err:
			# Invalid JSON
			self.print_error("FAILED (Invalid json string) " + str(err));
			return;

		# Parse json string
		self.json_object = json.loads (json_string);

	
	def print_error (self, error_msg):
		print 60 * "-";
		print error_msg;
		Test.failed_tests += 1;

	# Test if square brackets are used correctly in json string
	def test_brackets (self):
		if self.json_string[0] != '[' or self.json_string[-1] != ']':
			self.print_error ("FAILED (First and last characters of the json string must be '[' and ']' respectively");

		number_of_sbrackets = 0; 
		for char in self.json_string:
			if char == '[' or char == ']':
				number_of_sbrackets += 1;
		if number_of_sbrackets > 2:
			self.print_error ("FAILED (Too many square brackets in json sring");

		
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
		print "FAILED (Cannot determine which prediction page)"
		print 60 * "-";
		return;

	
	test = Test(json_string);
	test.test_brackets();
	# Invalid json string can't run other tests because other tests are dependent on this one
	if(Test.failed_tests == 0):
		test.test_with_schema();
	
	
	if Test.failed_tests == 0:
		print 60 * "-";
		print "PASSED all tests"
	else:
		print 60 * "-";
		print "FAILED", Test.failed_tests, "tests"


	print 60 * "-";
	
def main():
	json_string = parse("2014 Feb 11    150		5	3\n2015 Feb 12	    111		5	2", "28d");
	test_parser (json_string);
	

	
if __name__ == "__main__":
	main();
	
