#!/usr/bin/python

#Date/Time Module
import datetime;

import time
from Timestamp import *

#JSON Module
import json;

# For parse
def get_current_date():
	return time.strftime("%Y %b %d %H %M")

# For 3-day forecast
# String currently is ":Issued: YYYY MMM DD HHMM UTC"
# CHANGE ABOVE LINE IF THE LOGIC CHANGES
def get_issue_date(issue_date_string):
	return issue_date_string[9:20]

# For 3-day forecast
def get_next_date(current_day):
	time = Timestamp(current_day)
	now = datetime.date(time.year, time.month, time.day)
	delta = datetime.timedelta(days=1)
	next_date = now + delta
	return next_date.strftime('%Y %b %d')

# for 3-day forecast
def get_next_three_days(issue_date):
	upcoming_dates = [issue_date]
	for day in range(3):
		next_day = get_next_date(upcoming_dates[day])
		upcoming_dates.append(next_day)
	return upcoming_dates[1:]

#Takes first three letters of a month, returns an integer (1-12) on success, -1 on error.
def month_to_int(month):
	months=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"];

	for ii in range(0,11):
		if(month.lower()==months[ii]):
			return ii+1;

	return -1;

#Takes HHMM formated string, return an integer of HH on success, -1 on error.
def hhmm_to_hour(hhmm):
	if(len(hhmm)==4):
		return int(hhmm[:2]);
	else:
		return -1;

#Takes HHMM formated string, return an integer of MM on success, -1 on error.
def hhmm_to_min(hhmm):
	if(len(hhmm)==4):
		return int(hhmm[-2:]);
	else:
		return -1;

#Whitespace Lexer (Returns lexemes that are separated by whitespace).
def lexer_whitespace(raw_data):

	#Separate Whitespace
	lines=raw_data.splitlines(True);

	#Split Data In Each Line
	lexemes=[];

	for ii in range(0,len(lines)):
		lexemes.append(lines[ii].split());

	#Return Lexemes
	return lexemes;

#Now Parser (Parses the now forecast).
def parser_now(lexemes):

	#Array of valid dates (current and future).
	return_json="[\n";

	#Retrieve Downloaded Time
	downloaded_year=datetime.datetime.today().year;
	downloaded_month=datetime.datetime.today().month;
	downloaded_day=datetime.datetime.today().day;
	downloaded_hour=datetime.datetime.today().hour;
	downloaded_min=datetime.datetime.today().minute;

	#Parse Lexemes
	for ii in range(0,len(lexemes)):

		#Valid Column Width
		if(len(lexemes[ii])==18):

			#Default Values
			predicted_year=1970;
			predicted_month=1;
			predicted_day=1;
			predicted_hour=1;
			predicted_min=1;
			downloaded_year=1970;
			downloaded_month=1;
			downloaded_day=1;
			downloaded_hour=1;
			downloaded_min=1;
			kp=-1;

			#Extract Predicted Time
			predicted_year=int(lexemes[ii][0]);
			predicted_month=int(lexemes[ii][1]);
			predicted_day=int(lexemes[ii][2]);
			predicted_hour=hhmm_to_hour(lexemes[ii][3]);
			predicted_min=hhmm_to_min(lexemes[ii][3]);

			#Extract Predicted Kp
			kp=float(lexemes[ii][17]);

			#Invalid Year
			if(predicted_year<1970):
				return (False,
					"Invalid year on line "+str(ii+1)+
					" (expected a value greater than or equal to 1970 and got "+str(predicted_year)+").");

			#Invalid Month
			if(predicted_month<1 or predicted_month>12):
				return (False,
					"Invalid month on line "+str(ii+1)+
					" (expected a value between 1 and 12 and got "+str(predicted_month)+").");

			#Invalid Day
			if(predicted_day<1 or predicted_day>31):
				return (False,
					"Invalid day on line "+str(ii+1)+
					" (expected a value between 1 and 31 and got "+str(predicted_day)+").");

			#Invalid Hour
			if(predicted_hour<0 or predicted_hour>23):
				return (False,
					"Invalid hour on line "+str(ii+1)+
					" (expected a value between 0 and 23 and got "+str(predicted_hour)+").");

			#Invalid Minute
			if(predicted_min<0 or predicted_min>59):
				return (False,
					"Invalid minute on line "+str(ii+1)+
					" (expected a value between 0 and 59 and got "+str(predicted_min)+").");

			#Invalid Kp
			if(kp<-1 or kp>9):
				return (False,
					"Invalid Kp on line "+str(ii+1)+
					" (expected a value between -1.0 to 9.0 and got "+str(kp)+").");

			#Add JSON String
			return_json+="\t{\n";

			return_json+="\t\t\"time_predicted\":"
			return_json+="{";
			return_json+=	"\"year\":"+str(predicted_year)+",";
			return_json+=	"\"month\":"+str(predicted_month)+",";
			return_json+=	"\"day\":"+str(predicted_day)+",";
			return_json+=	"\"hour\":"+str(predicted_hour)+",";
			return_json+=	"\"minute\":"+str(predicted_min);
			return_json+="}";
			return_json+=",\n";
			return_json+="\t\t\"time_stamp\":"
			return_json+="{";
			return_json+=	"\"year\":"+str(downloaded_year)+",";
			return_json+=	"\"month\":"+str(downloaded_month)+",";
			return_json+=	"\"day\":"+str(downloaded_day)+",";
			return_json+=	"\"hour\":"+str(downloaded_hour)+",";
			return_json+=	"\"minute\":"+str(downloaded_min);
			return_json+="}";
			return_json+=",\n";
			return_json+="\t\t\"forecast\":\"now\",\n";
			return_json+="\t\t\"kp\":"+str(kp)+"\n";

			return_json+="\t}\n";

			if(ii<len(lexemes)-1):
				return_json+="\t,\n";

		#Non-Comment, Error
		elif(len(lexemes[ii])>0 and not(lexemes[ii][0].startswith("#") or lexemes[ii][0].startswith(":"))):
				return (False,
					"Invalid number of elements on line "+str(ii+1)+
					" (expected 18 and got "+str(len(lexemes[ii]))+").");

	return_json+="]";

	#Return Passed and the JSON Object
	return (True,return_json);

# Issue date is the best way to get date. Lines that start with digits are times.
def parse_3_day(input_text, time_now):
	output_text = ''
	issued = ':Issued:'

	for line in input_text:
		if issued in line:
			starting_from_today = get_issue_date(line)
			next_three_days =  get_next_three_days(starting_from_today)
		elif line[0:2].isdigit():
			kps = line[7:].split()
			for day in next_three_days:
				json = '{' + time_now + ', "time_predicted":'
				json += Timestamp(day + line[0:2]).json()
				kp_value = kps[0]
				kps = kps[1:]
				json += ',"forecast":"3day","kp":' + str(kp_value) + '},'
				output_text += json
	# Remove the off-by-1 comma made by the loop.
	output_text = output_text[:-1]
	return output_text


def parse_1_hour(input_text, time_now):
	output_text = ''
	important_line = "Planetary"
	forecast = ',"forecast:"3day","kp":'
	prediction_times = []

	for line in input_text:
		if len(line) == 0:
			continue
		elif line[0].isdigit():
			json = '{' + time_now + ', "time_predicted":'
			for hour in range(24):
				all_day = Timestamp(line + ' ' + str(hour)).json()
				prediction_times.append(json + all_day + forecast)
		elif important_line in line:
			kps = line.split()[-8:]
			index = 0
			for hour in range(24):
				prediction_times[hour] += str(kps[hour / 3]) + ' }'
				output_text += prediction_times[hour]
	return output_text

def parse_15_min(input_text, timestamp):
	return

# String currently starts with digit, so that's what we test for.
def parse_28_day(input_text, time_now):
	output_text = ''
	for line in input_text:
		if len(line) == 0:
			continue
		if line[0].isdigit():
			json = '{' + time_now + ', "time_predicted":'
			json += Timestamp(line[0:11]).json()
			kp_value = line[-1]	# kp is all we need, and it is at the end of line.
			json += ',"forecast":"28day","kp":' + str(kp_value) + '},'
			output_text += json
	# Remove the off-by-1 comma made by the loop.
	output_text = output_text[:-1]
	return output_text

def parse(input_text, which_one):
	timestamp = '"time_stamp":' + Timestamp(get_current_date()).json()
	text = input_text.split('\n')
	json_array = '[ '

	if which_one == "28d":
		json_array += parse_28_day(text, timestamp)
	elif which_one == "3d":
		json_array += parse_3_day(text, timestamp)
	elif which_one == "1h":
		json_array += parse_1_hour(text, timestamp)
	elif which_one == "15m":
		json_array += parse_15_min(text, timestamp)
	else:
		return "Cannot determine which prediction page"

	return json_array + ' ]'

#Main Test (Remove for production code).
import file_util;

data=file_util.file_to_string("now_cast.dat");
lexemes=lexer_whitespace(data);
ret=parser_now(lexemes);

if(ret[0]==False):
	print("Error:  "+ret[1]);
else:
	print(ret[1]);
