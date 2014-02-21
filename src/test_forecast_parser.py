#!/usr/bin/python

# Forecast Parser Test
#	Created By:	Ruslan Kolesnik, Caleb Hellickson, Ignacio Saez Lahildalga, Mike Moss
#	Modified On:	02/16/2014

import unittest
import json
import datetime
from forecast_parser_28_day import parse28




class Test:
	# Keeps track of number of failed tests
	failed_tests = 0;

	def __init__ (self, json_string):
		# Test if the given string is valid json
		try:
			json.loads(json_string);
		except:
			# Invalid JSON
			self.print_error("FAILED (Invalid json string)");
			return;

		# Parse json string
		self.json_object = json.loads (json_string);

		self.json_string = json_string;

	def print_error (self, error_msg):
		print "----------------------------------------------------------------"
		print error_msg;
		Test.failed_tests += 1;

	# Test if square brackets are used correctly in json string
	def test_brackets (self):
		if self.json_string[0] != '[' or self.json_string[-1] != ']':
			print_error ("FAILED (First and last characters of the json string must be '[' and ']' respectively");

		number_of_sbrackets = 0; 
		for char in self.json_string:
			if char == '[' or char == ']':
				number_of_sbrackets += 1;
		if number_of_sbrackets > 2:
			self.print_error ("FAILED (Too many square brackets in json sring");
			

	
	# Test if the second and second to last characters of json string are curly braces
	#def test_curly_braces (self):
	#	if self.json_string[1] != '{' or self.json_string[-2] != '}':
	#		self.print_error ("FAILED (Second and second to last characters of json string must be '{' and '}' respectively");

	def test_json_format (self):
		dic1 = {"time_stamp" : {"year" : 2000, "month" : 1, "day" : 1, "hour" : 1, "minute" : 1}};
		dic2 = {"time_predicted" : {"year" : 2000, "month" : 1, "day" : 1, "hour" : 1, "minute" : 1}, "forecast" : "now", "kp" : 7};
		within_dic = {"year" : 2000, "month" : 1, "day" : 1, "hour" : 1, "minute" : 1};
		
		counter = 0;
		for dictionary in self.json_object:
			counter += 1;
			
			# Check if dictionary has the correct keys
			if dictionary.keys() != dic1.keys() and dictionary.keys() != dic2.keys():
				self.print_error ("FAILED (Object " + str(counter) + " in json string has incorrect key)");
				continue;

			# Check if dictionary keys within time_stamp dictionary match
			if dictionary.has_key('time_stamp'):
				if dictionary['time_stamp'].keys() != within_dic.keys():
					self.print_error ("FAILED (Object " + str(counter) + " in json string has incorrect key)");

			# Check if dictionary keys within time_predicted dictionary match
			if dictionary.has_key('time_predicted'):
				if dictionary['time_predicted'].keys() != within_dic.keys():
					self.print_error ("FAILED (Object " + str(counter) + " in json string has incorrect key)");


			


def main():
	json_string = parse28("2014 Feb 11    150		5	3\n2014 Feb 12	    111		5	2");
	print json_string;
	
	test = Test(json_string);
	
	# Invalid json string can't do other tests
	if(Test.failed_tests == 0):
		test.test_brackets();
		#test.test_curly_braces();
		test.test_json_format();

	if Test.failed_tests == 0:
		print "----------------------------------------------------------------";
		print "PASSED all tests"
	else:
		print "----------------------------------------------------------------";
		print "FAILED", Test.failed_tests, "tests"


	print "----------------------------------------------------------------";	

	

main();
	
