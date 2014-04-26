#!/usr/bin/python

#Kp Retriever Source
#	Created By:		Ignacio Saez Lahidalga and Caleb Hellickson
#	Modified On:	04/24/2014

import db_util
import json
import MySQLdb as mdb


def get(json_object):

	try:
		obj=json.loads("["+json_object+"]")
	except:
		obj=json.loads("[]")

	request=db_util.retrieve_forecast(obj,"localhost","root","NOPE","forecast_db")

	if(request[0]==True):
		return request[1]
	else:
		return '{"error":"'+request[1]+'"}'
