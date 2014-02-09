#!/usr/bin/python

#Glut Input Header
#	Created By:		Mike Moss and Ignacio Saez Lahidalga
#	Modified On:	02/08/2014

#Configuration Parser Library
import ConfigParser;

#Signal Library
import signal;

#System Library
import sys;

#Time Library
import time;

#URL Library
import urllib2;

#Abort Signal Handler Function (Kills program.)
def abort_signal_handler(signal,frame):
	sys.exit(0);

#Assign Abort Signal Handler
signal.signal(signal.SIGINT,abort_signal_handler);

#Get URL Function (Makes a GET request, returns bytes on success, returns "" on failure.)
def get_url(link):
	try:
		request=urllib2.urlopen(time.strftime(link));
		return request.read();

	except:
		return "";

#Globals
now_forecast_link="";
d3_forecast_link=""
d28_forecast_link="";

#Read Configuration File Function
def read_config(filename):
	try:
		#Create Parser
		config_parser=ConfigParser.RawConfigParser();

		#Open File for Parsing
		config_parser.read(filename);

		#Read Data Values
		now_forecast_link_temp=config_parser.get("Data Resources","now_forecast");
		d3_forecast_link_temp=config_parser.get("Data Resources","d3_forecast");
		d28_forecast_link_temp=config_parser.get("Data Resources","d28_forecast");

		#Get Global Variables
		global now_forecast_link;
		global d3_forecast_link;
		global d28_forecast_link;

		#Assign Global Variables
		now_forecast_link=now_forecast_link_temp;
		d3_forecast_link=d3_forecast_link_temp;
		d28_forecast_link=d28_forecast_link_temp;

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
		config_parser.add_section("Data Resources");
		config_parser.set("Data Resources","now_forecast",now_forecast_link);
		config_parser.set("Data Resources","d3_forecast",d3_forecast_link);
		config_parser.set("Data Resources","d28_forecast",d28_forecast_link);

		#Write File With Parser
		with open(filename,"wb") as config_file:
			config_parser.write(config_file);

		#Success
		return True;

	except:
		#Failure
		return False;

#Get Resources...For Forever...
#while True:

	#Read Configuration File (If failure, write a default one.)
	if read_config("forecast_retriever.cfg")==False:
		write_config("forecast_retriever.cfg");

	#TESTING
	print(get_url(now_forecast_link));
	print(get_url(d3_forecast_link));
	print(get_url(d28_forecast_link));