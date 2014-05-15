#!/usr/bin/python

import ConfigParser

#Globals
server_email="Soothsayer <soothsayer@soothsayer.com>"
receiver_email="Administrator Bob <admin.bob@gmail.com>"
now_forecast_link="http://www.example.com/now.txt"
h1_forecast_link="http://www.example.com/1hour.txt"
d3_forecast_link="http://www.example.com/3day.txt"
d28_forecast_link="http://www.example.com/28day.txt"
cr_link="http://www.example.com/cr.txt"
database="forecast_db"
user="root"
password=""

#Read Configuration File Function
def read_config(filename):
	try:
		#Create Parser
		config_parser=ConfigParser.RawConfigParser()

		#Open File for Parsing
		config_parser.read(filename)

		#Read Data Values
		receiver_email_temp=config_parser.get("Contact Info","receiver_email")
		now_forecast_link_temp=config_parser.get("Data Resources","now_forecast_link")
		h1_forecast_link_temp=config_parser.get("Data Resources","h1_forecast_link")
		d3_forecast_link_temp=config_parser.get("Data Resources","d3_forecast_link")
		d28_forecast_link_temp=config_parser.get("Data Resources","d28_forecast_link")
		cr_link_temp=config_parser.get("Data Resources","cr_link")
		database_temp=config_parser.get("Database","forecast_database_name")
		user_temp=config_parser.get("Database","forecast_database_user")
		password_temp=config_parser.get("Database","forecast_database_password")

		#Get Global Variables
		global receiver_email
		global now_forecast_link
		global h1_forecast_link
		global d3_forecast_link
		global d28_forecast_link
		global cr_link
		global database
		global user
		global password

		#Assign Global Variables
		receiver_email=receiver_email_temp
		now_forecast_link=now_forecast_link_temp
		h1_forecast_link=h1_forecast_link_temp
		d3_forecast_link=d3_forecast_link_temp
		d28_forecast_link=d28_forecast_link_temp
		cr_link=cr_link_temp
		database=database_temp
		user=user_temp
		password=password_temp

		#Success
		return True

	except:

		#Failure
		return False
