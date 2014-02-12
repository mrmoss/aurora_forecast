#!/usr/bin/python

#Glut Input Header
#	Created By:		Mike Moss and Ignacio Saez Lahidalga
#	Modified On:	02/11/2014

#Configuration Parser Library
import ConfigParser;

#Emailer Module
import emailer;

#File Utility Library
import file_util;

#Password Module
#import getpass;

#Signal Library
import signal;

#System Library
import sys;

#URL Utility Library
import url_util;

#Abort Signal Handler Function (Kills program.)
def abort_signal_handler(signal,frame):
	sys.exit(0);

#Globals
password="";
sender_email="Aurora Forecast <aurora.forecast@gmail.com>";
sender_account="aurora.forecast";
receiver_email="Administrator Bob <admin.bob@gmail.com>";
now_forecast_link="http://www.example.com/now.txt";
d3_forecast_link="http://www.example.com/3day.txt";
d28_forecast_link="http://www.example.com/28day.txt";

#Read Configuration File Function
def read_config(filename):
	try:
		#Create Parser
		config_parser=ConfigParser.RawConfigParser();

		#Open File for Parsing
		config_parser.read(filename);

		#Read Data Values
		sender_email_temp=config_parser.get("Contact Info","sender_email");
		sender_account_temp=config_parser.get("Contact Info","sender_account");
		receiver_email_temp=config_parser.get("Contact Info","receiver_email");
		now_forecast_link_temp=config_parser.get("Data Resources","now_forecast");
		d3_forecast_link_temp=config_parser.get("Data Resources","d3_forecast");
		d28_forecast_link_temp=config_parser.get("Data Resources","d28_forecast");

		#Get Global Variables
		global sender_email;
		global sender_account;
		global receiver_email;
		global now_forecast_link;
		global d3_forecast_link;
		global d28_forecast_link;

		#Assign Global Variables
		sender_email=sender_email_temp;
		sender_account=sender_account_temp;
		receiver_email=receiver_email_temp;
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
		config_parser.add_section("Contact Info");
		config_parser.set("Contact Info","sender_email",sender_email);
		config_parser.set("Contact Info","sender_account",sender_account);
		config_parser.set("Contact Info","receiver_email",receiver_email);
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
while True:

	#Assign Abort Signal Handler
	signal.signal(signal.SIGINT,abort_signal_handler);

	#Read Configuration File (On failure, write a default configuration file.)
	if(read_config("forecast_retriever.cfg")==False):
		write_config("forecast_retriever.cfg");

	#Get Password for Email via command line.
	#password=getpass.getpass("password for forecast retriever: ");

	#Get Password for Email via local file.
	password=file_util.file_to_string("private_key");

	#Send Email Test
	emailer.send_email_threaded("Aurora Forecaster Error!!!","The now forecast failed to download!\r\n\r\nAurora Forecaster",
		sender_email,receiver_email,sender_account,password);

	while True:
		x=1;

	#Exit Main Thread
	break;