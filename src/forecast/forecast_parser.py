#!/usr/bin/python

#Forecast Parser Source
#	Created By:		Paul Gentemann and Mike Moss
#	Modified On:	03/04/2014

#Date/Time Module
import datetime

#Date Utility Module
import date_util

#Kp Utility Module
import kp_util

#String Utility Module
import string_util

#Whitespace Lexer (Returns lexemes that are separated by whitespace).
def lexer_whitespace(raw_data):

	#Separate Lines
	lines=raw_data.splitlines(True)

	#Split Data In Each Line By Whitespace
	lexemes=[]

	for ii in range(0,len(lines)):
		lexemes.append(lines[ii].split())

	#Return Lexemes
	return lexemes

#Assemble Dictionary Current Time Function, returns string, takes ((int)year,
#	(int)month, (int)day, (int)hour, (int)minute)
def assemble_dict_current_time():
	time={};
	time["year"]=datetime.datetime.today().year
	time["month"]=datetime.datetime.today().month
	time["day"]=datetime.datetime.today().day
	time["hour"]=datetime.datetime.today().hour
	time["minute"]=datetime.datetime.today().minute

	return time;

#Assemble JSON Forecast Date Function, returns string, takes ((int)yearm (int)month,
#	(int)day, (int)hour, (int)minute).
def assemble_json_forecast_date(time):
	json_string="";
	json_string+="{"
	json_string+=	"\"year\":"+str(time["year"])+","
	json_string+=	"\"month\":"+str(time["month"])+","
	json_string+=	"\"day\":"+str(time["day"])+","
	json_string+=	"\"hour\":"+str(time["hour"])+","
	json_string+=	"\"minute\":"+str(time["minute"])
	json_string+="}"

	return json_string

#Assemble JSON Forecast Function, returns string, takes ((time dict)predicted time,
#	(time dict)download time, (string)forecast, (float)kp).
def assemble_json_forecast(predicted_time,download_time,forecast,kp):

	json_string="";
	json_string+="\t{\n"
	json_string+="\t\t\"predicted_time\":"
	json_string+=assemble_json_forecast_date(predicted_time)
	json_string+=",\n"
	json_string+="\t\t\"download_time\":"
	json_string+=assemble_json_forecast_date(download_time)
	json_string+=",\n"
	json_string+="\t\t\"forecast\":\""+forecast+"\",\n"
	json_string+="\t\t\"kp\":"+str(kp)+"\n"
	json_string+="\t}\n"

	return json_string;

#Now Parser (Parses the now forecast).
def parse_now(lexemes):

	try:
		#JSON Return String
		return_json=""

		#Retrieve Downloaded Time
		download_time=assemble_dict_current_time();
		found_data=False

		#Parse Lexemes
		for ii in range(0,len(lexemes)):

			#Ignore Comments
			if(len(lexemes[ii])>0 and lexemes[ii][0].startswith("#")==False and lexemes[ii][0].startswith(":")==False):

				#Valid Time Row
				if(len(lexemes[ii])==18):

					#Extract Predicted Time
					predicted_time={};
					predicted_time["year"]=int(lexemes[ii][0])
					predicted_time["month"]=int(lexemes[ii][1])
					predicted_time["day"]=int(lexemes[ii][2])
					predicted_time["hour"]=date_util.hhmm_to_hour(lexemes[ii][3])
					predicted_time["minute"]=date_util.hhmm_to_min(lexemes[ii][3])

					#Extract Predicted Kp
					kp=float(lexemes[ii][17])

					#Test Predicted Date
					date_test=date_util.valid_date(predicted_time,ii+1)

					if(date_test[0]==False):
						return date_test

					#Invalid Kp
					kp_test=kp_util.valid_kp(kp,ii+1)

					if(kp_test[0]==False):
						return kp_test

					#Only Add Good Data
					if(kp>=0):
						return_json+=assemble_json_forecast(predicted_time,download_time,"now",kp);
						return_json+="\t,\n"
						found_data=True

				#Unknown Symbol
				else:
					return (False,"Unexpected symbol \""+str(lexemes[ii][0])+"\" on line "+str(ii+1)+".")

		#No Data Means Error
		if(found_data==False):
			return (False,"Did not find any data.")

		#Return Passed and the JSON Object
		return (True,return_json[:-2]+"\n")

	except Exception as e:
		return (False,str(e)[0:].capitalize()+".")

#1 Hour Parser (Parses the 1 hour forecast).
def parse_h1(lexemes):

	try:
		#JSON Return String
		return_json=""

		#Retrieve Downloaded Time
		download_time=assemble_dict_current_time();

		#Default Predicted Time
		found_date=False
		found_data=False

		#Parse Lexemes
		for ii in range(0,len(lexemes)):

			#Ignore Comments
			if(len(lexemes[ii])>0 and lexemes[ii][0].startswith("#")==False and lexemes[ii][0].startswith(":")==False):

				#Valid YMD Row
				if(len(lexemes[ii])==3 and string_util.is_int(lexemes[ii][0])):

					#Found a Date
					found_date=True

					#Extract Predicted YMD
					predicted_time={};
					predicted_time["year"]=int(lexemes[ii][0])
					predicted_time["month"]=date_util.month_to_int(lexemes[ii][1])
					predicted_time["day"]=int(lexemes[ii][2])
					predicted_time["hour"]=0;
					predicted_time["minute"]=0;

				#Valid Planetary Estimated Ap Row
				elif(found_date==True and len(lexemes[ii])==11 and lexemes[ii][0].startswith("Planetary")):

					#Go Through The 8 Three Hour Segments
					for jj in range(0,8):

						#Create 3 Entries Per Three Hour Segment
						for kk in range(0,3):

							#Extract Predicted Hour, Minute is -1
							predicted_hour=jj*3+kk
							predicted_minute=-1

							#Extract Predicted Kp
							kp=float(lexemes[ii][3+jj])

							#Test Predicted Date
							date_test=date_util.valid_date(predicted_time,ii+1)

							if(date_test[0]==False):
								return date_test

							#Invalid Kp
							kp_test=kp_util.valid_kp(kp,ii+1)

							if(kp_test[0]==False):
								return kp_test

							#Only Add Good Data
							if(kp>=0):
								return_json+=assemble_json_forecast(predicted_time,download_time,"h1",kp);
								return_json+="\t,\n"
								found_data=True

		#No Data Means Error
		if(found_data==False):
			return (False,"Did not find any data.")

		#Return Passed and the JSON Object
		return (True,return_json[:-2]+"\n")

	except Exception as e:
		return (False,str(e)[0:].capitalize()+".")

#3 Day Parser (Parses the 3 day forecast).
def parse_d3(lexemes):

	try:
		#JSON Return String
		return_json=""

		#Retrieve Downloaded Time
		download_time=assemble_dict_current_time();

		#Default Predicted Time
		found_date=False
		found_data=False

		#Parse Lexemes
		for ii in range(0,len(lexemes)):

			#Ignore Comments
			if(len(lexemes[ii])>0 and lexemes[ii][0].startswith("#")==False and lexemes[ii][0].startswith(":")==False):

				#Valid MD Row
				if(len(lexemes[ii])==6 and date_util.month_to_int(lexemes[ii][0])>0 and string_util.is_int(lexemes[ii][1])):

					#Found a Date
					found_date=True
					date=lexemes[ii]

				#Valid Time Row
				elif(len(lexemes[ii])==4 and found_date==True):

					#Convert Hours
					hours=date_util.hhdashhhut_to_hours(lexemes[ii][0])

					#Extract Data
					if(hours[0]>=0 and hours[1]>=0):

						#3 Days Per Row
						for jj in range(0,3):


							#3 Hours Per Segment
							for kk in range(0,3):

								#Extract Predicted Time, Minute is -1
								predicted_time={};
								predicted_time["year"]=download_time["year"]
								predicted_time["month"]=date_util.month_to_int(date[jj*2])
								predicted_time["day"]=int(date[jj*2+1])
								predicted_time["hour"]=hours[0]+kk
								predicted_time["minute"]=-1

								#Extract Predicted Kp
								kp=float(lexemes[ii][1+jj])

								#Test Predicted Date
								date_test=date_util.valid_date(predicted_time,ii+1)

								if(date_test[0]==False):
									return date_test

								#Invalid Kp
								kp_test=kp_util.valid_kp(kp,ii+1)

								if(kp_test[0]==False):
									return kp_test

								#Only Add Good Data
								if(kp>=0):
									return_json+=assemble_json_forecast(predicted_time,download_time,"d3",kp);
									return_json+="\t,\n"
									found_data=True

		#No Data Means Error
		if(found_data==False):
			return (False,"Did not find any data.")

		#Return Passed and the JSON Object
		return (True,return_json[:-2]+"\n")

	except Exception as e:
		return (False,str(e)[0:].capitalize()+".")

#28 Day Parser (Parses the 28 day forecast).
def parse_d28(lexemes):

	try:
		#JSON Return String
		return_json=""

		#Retrieve Downloaded Time
		download_time=assemble_dict_current_time();
		found_data=False

		#Parse Lexemes
		for ii in range(0,len(lexemes)):

			#Ignore Comments
			if(len(lexemes[ii])>0 and lexemes[ii][0].startswith("#")==False and lexemes[ii][0].startswith(":")==False):

				#Valid Time Row
				if(len(lexemes[ii])==6):

					#Default Values
					predicted_year=1970
					predicted_month=1
					predicted_day=1
					predicted_hour=1
					predicted_min=1
					kp=-1

					#Extract Predicted Time
					predicted_time={};
					predicted_time["year"]=int(lexemes[ii][0])
					predicted_time["month"]=date_util.month_to_int(lexemes[ii][1])
					predicted_time["day"]=int(lexemes[ii][2])
					predicted_time["hour"]=-1
					predicted_time["minute"]=-1

					#Extract Predicted Kp
					kp=float(lexemes[ii][5])

					#Test Predicted Date
					date_test=date_util.valid_date(predicted_time,ii+1)

					if(date_test[0]==False):
						return date_test

					#Invalid Kp
					kp_test=kp_util.valid_kp(kp,ii+1)

					if(kp_test[0]==False):
						return kp_test

					#Only Add Good Data
					if(kp>=0):
						return_json+=assemble_json_forecast(predicted_time,download_time,"d28",kp);
						return_json+="\t,\n"

						#Data Found
						found_data=True

				#Unknown Symbol
				else:
					return (False,"Unexpected symbol \""+str(lexemes[ii][0])+"\" on line "+str(ii+1)+".")

		#No Data Means Error
		if(found_data==False):
			return (False,"Did not find any data.")

		#Return Passed and the JSON Object
		return (True,return_json[:-2]+"\n")

	except Exception as e:
		return (False,str(e)[0:].capitalize()+".")
