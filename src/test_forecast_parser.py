#!/usr/bin/python

# Forecast Parser Test
#	Created By:	Ruslan Kolesnik, Caleb Hellickson, Ignacio Saez Lahildalga, Mike Moss
#	Modified On:	02/16/2014

import unittest
import json
import datetime
from forecast_parser_28_day import parse28

all_tests_passed = True;


# Test is json string is valid
def test_json_format(json_string):
	try:
		json.loads(json_string);
	except:
		# Invalid JSON
		print "----------------------------------------------------------------";
		print "FAILED (Invalid Jason): in function test_json_object";
	return;

# Check if given value is within range. Print error if it's not within range.
def check_range(key, value, min_range, max_range, func_name):
	if(value < min_range or value > max_range):
		print "----------------------------------------------------------------";
		print "FAILED (", key, value, "out of range ): in function", func_name;
		global all_tests_passed;
		all_tests_passed = False;
	return;

# Check if value of the given key is valid
def check_value(key, min_range, max_range, func_name, dictionary):
	if 'Time_stamp' in dictionary:
		json_temp = dictionary['Time_stamp'];

		# Check if year is within range
		check_range(key, json_temp[key], min_range, max_range, func_name);

	if 'Time_predicted' in dictionary:
		json_temp = dictionary['Time_predicted'];

		# Check if year is within range
		check_range(key, json_temp[key], min_range, max_range, func_name);
	return;


# Test if the year is within range
def test_year(json_object):
	min_year = 1970;
	max_year = datetime.datetime.now().year;
	for dictionary in json_object:
		check_value('year', min_year, max_year, 'test_year', dictionary);
	return;

# Test if month is within range	
def test_month(json_object):
	min_month = 1;
	max_month = 12;
	for dictionary in json_object:
		check_value('month', min_month, max_month, 'test_month', dictionary);
	return;

# Test if day is within range
def test_day(json_object):
	min_day = -1;
	max_day = 31;
	for dictionary in json_object:
		check_value('day', min_day, max_day, 'test_day', dictionary);
	return;

# Test if hour is within range
def test_hour(json_object):
	min_hour = -1;
	max_hour = 24;
	for dictionary in json_object:
		check_value('hour', min_hour, max_hour, 'test_hour', dictionary);
	return;

# Test if minutes are within range
def test_minutes(json_object):
	min_minutes = -1;
	max_minutes = 60;
	for dictionary in json_object:
		check_value('min', min_minutes, max_minutes, 'test_minutes', dictionary);
	return;

# Test if specified forecast is valid
def test_forecast(json_object):
	global all_tests_passed;
	for dictionary in json_object:
		if 'Time_predicted' in dictionary:
			if 'forecast' not in dictionary:
				print "----------------------------------------------------------------";
				print "FAILED (forecast not found): in function test_forecast";
				all_tests_passed = False;
				return;
			forecast = dictionary['forecast'];
			if(forecast != 'now' and forecast != 'd28' and forecast != 'd3' and forecast != 'h1'):
				print "----------------------------------------------------------------";
				print "FAILED (", forecast, "is not a valid forecast): in function test_forecast";
				all_tests_passed = False;
				return;
	return;

# Test if specified kp is within range
def test_kp(json_object):
	global all_tests_passed;
	min_kp = -1;
	max_kp = 9;
	for dictionary in json_object:
		if 'Time_predicted' in dictionary:
			if 'kp' not in dictionary:
				print "----------------------------------------------------------------";
				print "FAILED (kp not found): in function test_kp";
				all_tests_passed = False;
				return;
			check_range('kp', dictionary['kp'], min_kp, max_kp, 'test_kp');  
	return;


		

def main():
	#json_string = '[{"Time_stamp":{"year":2000,"month":1,"day":1,"hour":-1,"min":-1}},{"Time_predicted":{"year":2009,"month":12,"day":30,"hour":10,"min":11},"forecast":"d28","kp":7}]';
	json_string = parse28(
	test_json_format(json_string);
	json_object = json.loads(json_string);

	test_year(json_object);
	test_month(json_object);
	test_day(json_object);
	test_hour(json_object);
	test_minutes(json_string);
	test_forecast(json_object);
	test_kp(json_object);
	
	global all_tests_passed;
	if(all_tests_passed):
		print "----------------------------------------------------------------";
		print "PASSED all tests"

	print "----------------------------------------------------------------";

main();
	
