#!/usr/bin/python

#Carrington Rotation Retriever Source
#	Created By:		Mike Moss
#	Modified On:	04/25/2014

import db_util
import json
import MySQLdb as mdb


def get(json_object):

	try:
		obj=json.loads("["+json_object+"]")
	except:
		obj=json.loads("[]")

	request=db_util.retrieve_carrington(obj,"localhost","root","NOPE","forecast_db")

	if(request[0]==True):
		return request[1]
	else:
		return '{"error":"'+request[1]+'"}'
