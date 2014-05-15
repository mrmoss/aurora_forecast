#!/usr/bin/python

#Carrington Rotation Retriever Source
#	Created By:		Mike Moss
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

		request=db_util.retrieve_carrington(obj,"localhost",config_util.user,config_util.password,config_util.database)

		if(request[0]==True):
			return request[1]
		else:
			return '{"error":"'+request[1]+'"}'
	else:
		return '{"error":"Bad password."}'
