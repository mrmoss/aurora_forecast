#!/usr/bin/python

#Glut Input Header
#	Created By:		Mike Moss and Ignacio Saez Lahidalga
#	Modified On:	02/08/2014

#URL Library
import urllib2;

#Signal Library
import signal

#System Library
import sys;

#Time Library
import time;

#Abort Signal Handler Function (Kills program.)
def abort_signal_handler(signal,frame):
	sys.exit(0);

#Assign Abort Signal Handler
signal.signal(signal.SIGINT,abort_signal_handler)

#Get URL Function (Makes a GET request, returns bytes on success, returns "" on failure.)
def get_url(link):
	try:
		request=urllib2.urlopen(link);
		return request.read();
	except:
		return "";

#Get Resources...For Forever...
while True:

	#Data Source Links
	now_forecast_link="http://www.swpc.noaa.gov/ftpdir/lists/geomag/AK.txt";
	d3_forecast_link="http://www.swpc.noaa.gov/ftpdir/forecasts/geomag_forecast/"+time.strftime("%m%d")+"geomag_forecast.txt";
	d28_forecast_link="http://www.swpc.noaa.gov/ftpdir/weekly/27DO.txt";

	#Main program.
	print(get_url(d3_forecast_link));