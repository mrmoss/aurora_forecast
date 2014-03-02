#!/usr/bin/python

#Forecast Retriever Source
#	Created By:		Paul Gentemann, Caleb Hellickson, Ruslan Kolesnik, Ignacio Saez Lahidalga, and Mike Moss
#	Modified On:	03/01/2014

#Configuration Parser Library
import ConfigParser;

#Emailer Module
import emailer;

#File Utility Library
import file_util;

#Forecast Parser Library
import forecast_parser;

#JSON Test Library
import test_json;

#Signal Library
import signal;

#System Library
import sys;

#Time Library
import time;

#URL Utility Library
import url_util;

#Abort Signal Handler Function (Kills program.)
def abort_signal_handler(signal,frame):
	sys.exit(0);

#Globals
server_email="Soothsayer <soothsayer@soothsayer.com>";
receiver_email="Administrator Bob <admin.bob@gmail.com>";
now_forecast_link="http://www.example.com/now.txt";
h1_forecast_link="http://www.example.com/1hour.txt";
d3_forecast_link="http://www.example.com/3day.txt";
d28_forecast_link="http://www.example.com/28day.txt";
now_forecast_timer=5;
h1_forecast_timer=20;
d3_forecast_timer=24;
d28_forecast_timer=1440;
retry_timer=1;

#Read Configuration File Function
def read_config(filename):
	try:
		#Create Parser
		config_parser=ConfigParser.RawConfigParser();

		#Open File for Parsing
		config_parser.read(filename);

		#Read Data Values
		receiver_email_temp=config_parser.get("Contact Info","receiver_email");
		now_forecast_link_temp=config_parser.get("Data Resources","now_forecast_link");
		h1_forecast_link_temp=config_parser.get("Data Resources","h1_forecast_link");
		d3_forecast_link_temp=config_parser.get("Data Resources","d3_forecast_link");
		d28_forecast_link_temp=config_parser.get("Data Resources","d28_forecast_link");
		now_forecast_timer_temp=config_parser.get("Time Settings","now_forecast_timer");
		h1_forecast_timer_temp=config_parser.get("Time Settings","h1_forecast_timer");
		d3_forecast_timer_temp=config_parser.get("Time Settings","d3_forecast_timer");
		d28_forecast_timer_temp=config_parser.get("Time Settings","d28_forecast_timer");
		retry_timer_temp=config_parser.get("Time Settings","retry_timer");

		#Get Global Variables
		global receiver_email;
		global now_forecast_link;
		global h1_forecast_link;
		global d3_forecast_link;
		global d28_forecast_link;
		global now_forecast_timer;
		global h1_forecast_timer;
		global d3_forecast_timer;
		global d28_forecast_timer;

		#Assign Global Variables
		receiver_email=receiver_email_temp;
		now_forecast_link=now_forecast_link_temp;
		h1_forecast_link=h1_forecast_link_temp;
		d3_forecast_link=d3_forecast_link_temp;
		d28_forecast_link=d28_forecast_link_temp;
		now_forecast_timer=now_forecast_timer_temp;
		h1_forecast_timer=h1_forecast_timer_temp;
		d3_forecast_timer=d3_forecast_timer_temp;
		d28_forecast_timer=d28_forecast_timer_temp;
		retry_timer=retry_timer_temp;

		#Success
		return True;

	except:
		#Failure
		return False;

#Write Configuration File Function
def write_config(filename):
	try:
		#Create Parser
		config_parser=ConfigParser.RawConfigParser();

		#Add Section and Write Data Values
		config_parser.add_section("Contact Info");
		config_parser.set("Contact Info","receiver_email",receiver_email);
		config_parser.add_section("Data Resources");
		config_parser.set("Data Resources","now_forecast_link",now_forecast_link);
		config_parser.set("Data Resources","h1_forecast_link",h1_forecast_link);
		config_parser.set("Data Resources","d3_forecast_link",d3_forecast_link);
		config_parser.set("Data Resources","d28_forecast_link",d28_forecast_link);
		config_parser.add_section("Time Settings");
		config_parser.set("Time Settings","now_forecast_timer",now_forecast_timer);
		config_parser.set("Time Settings","h1_forecast_timer",h1_forecast_timer);
		config_parser.set("Time Settings","d3_forecast_timer",d3_forecast_timer);
		config_parser.set("Time Settings","d28_forecast_timer",d28_forecast_timer);
		config_parser.set("Time Settings","retry_timer",retry_timer);

		#Write File With Parser
		with open(filename,"wb") as config_file:
			config_parser.write(config_file);

		#Success
		return True;

	except:
		#Failure
		return False;

#Fake Functions...
def update_database(fake):
	print("updating database!");

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
	exit();

#Forecast Update Function
def get_forecast(link,parser,email_text):
	#Try to Download Data
	data_download=url_util.get_url(link);

	#Failed Data Download
	if(data_download==""):
		emailer.send_email_threaded("Aurora Forecaster Error!!!","The "+email_text+" forecast failed to download!\r\n\r\nDownload Link:\r\n"+link+"\r\n\r\nAurora Forecaster\r\n\r\n",server_email,receiver_email);

	#Successful Data Download
	else:
		#Convert Downloaded Data
		data_converted=forecast_parser.parse(data_download,parser);

		#Failed Conversion
		if(data_converted==""):
			emailer.send_email_threaded("Aurora Forecaster Error!!!","The "+email_text+" forecast conversion script is not working!\r\n\r\nDownloaded Data:\r\n<<<start>>>\r\n"+data_download+"<<end>>>\r\n\r\nAurora Forecaster\r\n\r\n",server_email,receiver_email);

		#Successful Conversion
		else:
			#Parse Converted Data
			data_json=test_json.test_json_string(data_converted);

			#Failed Parse
			if(data_json[0]==False):
				emailer.send_email_threaded("Aurora Forecaster Error!!!","The "+email_text+" forecast parser reported an error!\r\n\r\nError Message:\r\n"+data_json[1]+"\r\n\r\nParse Data:\r\n"+str(data_converted)+"\r\n\r\nAurora Forecaster\r\n\r\n",server_email,receiver_email);

			#Successful Parse
			else:
				update_database(data_json[1]);

#Get Resources...For Forever...
while True:

	#Assign Abort Signal Handler
	signal.signal(signal.SIGINT,abort_signal_handler);

	#Start Server
	print("forecast retriever startup routine");

	#Read Configuration File (On failure, write a default configuration file.)
	error_message_start("\tloading configuration file...");

	if(read_config("forecast_retriever.cfg")==False):
		error_message_end(False);
		error_message_start("\t\tcreating configuration file...");

		#Write Configuration on Read Fail
		if(write_config("forecast_retriever.cfg")):
			error_message_end(True);
		else:
			error_message_end(False);
			error_message_fatal_error();

	else:
		error_message_end(True);

	#Test Email Login
	error_message_start("\tsigning into email...");

	#Good Email Signin
	if(emailer.send_email("Aurora Forecaster","Server started!",server_email,receiver_email)):
		error_message_end(True);

	#Bad Email Signin
	else:
		error_message_end(False);
		error_message_fatal_error();

	#Server Started
	print("server started");

	#Be A Server (Forever...)
	while True:

		#TEST
		get_forecast(d28_forecast_link,"28d","28 day");

		while True:
			time.sleep(0);

	#Exit Main Thread
	break;
