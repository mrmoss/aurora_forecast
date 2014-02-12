#!/usr/bin/python

#Emailer Library Source
#	Created By:		Mike Moss
#	Modified On:	02/11/2014

#Thread Library
import thread;

#SMTP Library
import smtplib;

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