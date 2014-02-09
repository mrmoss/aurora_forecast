#!/usr/bin/python

import urllib2;

now_cast_url="http://www.swpc.noaa.gov/ftpdir/lists/geomag/AK.txt";
h1_cast_url="http://www.swpc.noaa.gov/ftpdir/lists/geomag/AK.txt";
d3_cast_url="http://www.swpc.noaa.gov/ftpdir/forecasts/geomag_forecast/0120geomag_forecast.txt";
d28_cast_url="http://www.swpc.noaa.gov/ftpdir/weekly/27DO.txt";

now_cast_request=urllib2.urlopen(now_cast_url);
h1_cast_request=urllib2.urlopen(h1_cast_url);
d3_cast_request=urllib2.urlopen(d3_cast_url);
d28_cast_request=urllib2.urlopen(d28_cast_url);

now_cast_data=now_cast_request.read();
h1_cast_data=h1_cast_request.read();
d3_cast_data=d3_cast_request.read();
d28_cast_data=d28_cast_request.read();

print(now_cast_data);
print(h1_cast_data);
print(d3_cast_data);
print(d28_cast_data);

