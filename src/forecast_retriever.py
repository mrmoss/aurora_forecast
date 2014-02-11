#!/usr/bin/python

#Glut Input Header
#	Created By:		Mike Moss and Ignacio Saez Lahidalga
#	Modified On:	02/10/2014

#Configuration Parser Library
import ConfigParser;

#Password Module
import getpass;

#Signal Library
import signal;

#SMTP Library
import smtplib;

#System Library
import sys;

#Thread Library
import thread;

#Time Library
import time;

#URL Library
import urllib2;

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

#File to String Function
def file_to_string(filename):
	try:
		with open(filename,"r") as opened_file:
			return opened_file.read();
	except:
		return "";

#Get URL Function (Makes a GET request, returns bytes on success, returns "" on failure.)
def get_url(link):
	try:
		request=urllib2.urlopen(time.strftime(link));
		return request.read();

	except:
		return "";

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

#Send Email Function (Sends an email through Gmail.)
def send_email(subject,message,address_from,address_to,username,password):
	try:
		#Connect to Gmail
		smtp_server=smtplib.SMTP("smtp.gmail.com:587");
		smtp_server.ehlo();
		smtp_server.starttls();
		smtp_server.ehlo();
		smtp_server.login(username,password);

		#Send Message
		header="From: "+address_from+"\r\nTo: "+address_to+"\r\nSubject: "+subject+"\r\n";
		smtp_server.sendmail(address_from,address_to,header+message);

		#All Done
		smtp_server.quit();

		#Success
		return True;

	except:
		#Failure
		return False;

#Send Email Threaded Function (Spawns off a new thread that sends an email, non-blocking for main thread.)
def send_email_threaded(subject,message,address_from,address_to,username,password):
	thread.start_new(send_email_thread_function,([subject,message,address_from,address_to,username,password],));

#Send Email Thread Function (Thread function spawned off by the send_email_threaded function.)
def send_email_thread_function(data):
	send_email(data[0],data[1],data[2],data[3],data[4],data[5]);

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
	#password=file_to_string("private_key");

	#Send Email Test
	#send_email_threaded("Aurora Forecaster Error!!!","The now forecast failed to download!\r\n\r\nAurora Forecaster",
		#sender_email,receiver_email,sender_account,password);

	#Exit Main Thread
	break;