#!/usr/bin/python

#Kp Retriever Source
#	Created By:		Ignacio Saez Lahidalga and Caleb Hellickson
#	Modified On:	05/04/2014

import config_util
import db_util
import json
import MySQLdb as mdb


def get(json_object):

	if(config_util.read_config("forecast_retriever.cfg")==True):
		try:
			obj=json.loads("["+json_object+"]")
		except:
			obj=json.loads("[]")

		request=db_util.retrieve_forecast(obj,"localhost",config_util.user,config_util.password,config_util.database)

		if(request[0]==True):
			return request[1]
		else:
			return '{"error":"'+request[1]+'"}'
	else:
		return '{"error":"Bad password."}'
