#!/usr/bin/python

import signal
import sys
def signal_handler(signal,frame):
	sys.exit(0)
signal.signal(signal.SIGINT,signal_handler)

import urllib2;

forecast_url=[];
forecast_url.append("http://www.swpc.noaa.gov/ftpdir/lists/geomag/AK.txt");
forecast_url.append("http://www.swpc.noaa.gov/ftpdir/lists/geomag/AK.txt");
forecast_url.append("http://www.swpc.noaa.gov/ftpdir/forecasts/geomag_forecast/0120geomag_forecast.txt");
forecast_url.append("http://www.swpc.noaa.gov/ftpdir/weekly/27DO.txt");

forecast_data=["","","",""];












import threading;

def get_url(forecast):
	while True:
		try:
			request=urllib2.urlopen(forecast_url[forecast]);
			forecast_data[forecast]=request.read();
			result[forecast]=True;
			print "worked";
		except:
			print "error";

for ii in range(0,4):
	t = threading.Thread(target=get_url,args=[ii])
	t.daemon = True
	t.start()

import time;

while True:
	time.sleep(0);