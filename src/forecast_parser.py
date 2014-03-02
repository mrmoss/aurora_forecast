#!/usr/bin/python

#Forecast Retriever Source
#	Created By:		Paul Gentemann and Mike Moss
#	Modified On:	03/01/2014

#Date/Time Module
import datetime;

#Date Utility Module
import date_util;

#Kp Utility Module
import kp_util;

#Is Integer Function (Tests if a string is an integer).
def is_int(string):
	try:
		int(string);
		return True;

	except ValueError:
		return False;

#Whitespace Lexer (Returns lexemes that are separated by whitespace).
def lexer_whitespace(raw_data):

	#Separate Whitespace
	lines=raw_data.splitlines(True);

	#Split Data In Each Line
	lexemes=[];

	for ii in range(0,len(lines)):
		lexemes.append(lines[ii].split());

	#Return Lexemes
	return lexemes;

#Now Parser (Parses the now forecast).
def parse_now(lexemes):

	try:
		#JSON Return String
		return_json="";

		#Retrieve Downloaded Time
		downloaded_year=datetime.datetime.today().year;
		downloaded_month=datetime.datetime.today().month;
		downloaded_day=datetime.datetime.today().day;
		downloaded_hour=datetime.datetime.today().hour;
		downloaded_minute=datetime.datetime.today().minute;
		found_data=False;

		#Parse Lexemes
		for ii in range(0,len(lexemes)):

			#Ignore Comments
			if(len(lexemes[ii])>0 and lexemes[ii][0].startswith("#")==False and lexemes[ii][0].startswith(":")==False):

				#Valid Time Row
				if(len(lexemes[ii])==18):

					#Default Values
					predicted_year=1970;
					predicted_month=1;
					predicted_day=1;
					predicted_hour=1;
					predicted_min=1;
					kp=-1;

					#Extract Predicted Time
					predicted_year=int(lexemes[ii][0]);
					predicted_month=int(lexemes[ii][1]);
					predicted_day=int(lexemes[ii][2]);
					predicted_hour=date_util.hhmm_to_hour(lexemes[ii][3]);
					predicted_minute=date_util.hhmm_to_min(lexemes[ii][3]);

					#Extract Predicted Kp
					kp=float(lexemes[ii][17]);

					#Test Predicted Date
					date_test=date_util.date_util.valid_date(predicted_year,predicted_month,predicted_day,
						predicted_hour,predicted_minute,ii+1);

					if(date_test[0]==False):
						return date_test;

					#Invalid Kp
					kp_test=kp_util.valid_kp(kp,ii+1);

					if(kp_test[0]==False):
						return kp_test;

					#Only Add Good Data
					if(kp>=0):

						#Add JSON String
						return_json+="\t{\n";

						return_json+="\t\t\"predicted_time\":"
						return_json+="{";
						return_json+=	"\"year\":"+str(predicted_year)+",";
						return_json+=	"\"month\":"+str(predicted_month)+",";
						return_json+=	"\"day\":"+str(predicted_day)+",";
						return_json+=	"\"hour\":"+str(predicted_hour)+",";
						return_json+=	"\"minute\":"+str(predicted_minute);
						return_json+="}";
						return_json+=",\n";
						return_json+="\t\t\"download_time\":"
						return_json+="{";
						return_json+=	"\"year\":"+str(downloaded_year)+",";
						return_json+=	"\"month\":"+str(downloaded_month)+",";
						return_json+=	"\"day\":"+str(downloaded_day)+",";
						return_json+=	"\"hour\":"+str(downloaded_hour)+",";
						return_json+=	"\"minute\":"+str(downloaded_minute);
						return_json+="}";
						return_json+=",\n";
						return_json+="\t\t\"forecast\":\"now\",\n";
						return_json+="\t\t\"kp\":"+str(kp)+"\n";

						return_json+="\t}\n";

						if(ii<len(lexemes)-1):
							return_json+="\t,\n";

						#Data Found
						found_data=True;

					#Unknown Symbol
					else:
						return (False,"Unexpected symbol \""+str(lexemes[ii][0])+"\" on line "+str(ii+1)+".");

		#No Data Means Error
		if(found_data==False):
			return (False,"Did not find any data.");

		#Return Passed and the JSON Object
		return (True,return_json);

	except Exception as e:
		return (False,str(e)[0:].capitalize()+".");

#1 Hour Parser (Parses the 1 hour forecast).
def parse_h1(lexemes):

	try:
		#JSON Return String
		return_json="";

		#Retrieve Downloaded Time
		downloaded_year=datetime.datetime.today().year;
		downloaded_month=datetime.datetime.today().month;
		downloaded_day=datetime.datetime.today().day;
		downloaded_hour=datetime.datetime.today().hour;
		downloaded_minute=datetime.datetime.today().minute;

		#Default Predicted Time
		found_date=False;
		predicted_year=1970;
		predicted_month=1;
		predicted_day=1;
		found_data=False;

		#Parse Lexemes
		for ii in range(0,len(lexemes)):

			#Ignore Comments
			if(len(lexemes[ii])>0 and lexemes[ii][0].startswith("#")==False and lexemes[ii][0].startswith(":")==False):

				#Valid YMD Row
				if(len(lexemes[ii])==3 and is_int(lexemes[ii][0])):

					#Found a Date
					found_date=True;

					#Extract Predicted YMD
					predicted_year=int(lexemes[ii][0]);
					predicted_month=date_util.month_to_int(lexemes[ii][1]);
					predicted_day=int(lexemes[ii][2]);

				#Valid Planetary Estimated Ap Row
				elif(found_date==True and len(lexemes[ii])==11 and lexemes[ii][0].startswith("Planetary")):

					#Go Through The 8 Three Hour Segments
					for jj in range(0,8):

						#Create 3 Entries Per Three Hour Segment
						for kk in range(0,3):

							#Data Found
							found_data=True;

							#Extract Predicted Hour, Minute is -1
							predicted_hour=jj*3+kk;
							predicted_minute=-1;

							#Extract Predicted Kp
							kp=float(lexemes[ii][3+jj]);

							#Test Predicted Date
							date_test=date_util.valid_date(predicted_year,predicted_month,predicted_day,
								predicted_hour,predicted_minute,ii+1);

							if(date_test[0]==False):
								return date_test;

							#Invalid Kp
							kp_test=kp_util.valid_kp(kp,ii+1);

							if(kp_test[0]==False):
								return kp_test;

							#Only Add Good Data
							if(kp>=0):

								#Add JSON String
								return_json+="\t{\n";

								return_json+="\t\t\"predicted_time\":"
								return_json+="{";
								return_json+=	"\"year\":"+str(predicted_year)+",";
								return_json+=	"\"month\":"+str(predicted_month)+",";
								return_json+=	"\"day\":"+str(predicted_day)+",";
								return_json+=	"\"hour\":"+str(predicted_hour)+",";
								return_json+=	"\"minute\":"+str(predicted_minute);
								return_json+="}";
								return_json+=",\n";
								return_json+="\t\t\"download_time\":"
								return_json+="{";
								return_json+=	"\"year\":"+str(downloaded_year)+",";
								return_json+=	"\"month\":"+str(downloaded_month)+",";
								return_json+=	"\"day\":"+str(downloaded_day)+",";
								return_json+=	"\"hour\":"+str(downloaded_hour)+",";
								return_json+=	"\"minute\":"+str(downloaded_minute);
								return_json+="}";
								return_json+=",\n";
								return_json+="\t\t\"forecast\":\"h1\",\n";
								return_json+="\t\t\"kp\":"+str(kp)+"\n";

								return_json+="\t}\n";

								if(predicted_hour<23):
									return_json+="\t,\n";

		#No Data Means Error
		if(found_data==False):
			return (False,"Did not find any data.");

		#Return Passed and the JSON Object
		return (True,return_json);

	except Exception as e:
		return (False,str(e)[0:].capitalize()+".");

#3 Day Parser (Parses the 3 day forecast).
def parse_d3(lexemes):

	try:
		#JSON Return String
		return_json="";

		#Retrieve Downloaded Time
		downloaded_year=datetime.datetime.today().year;
		downloaded_month=datetime.datetime.today().month;
		downloaded_day=datetime.datetime.today().day;
		downloaded_hour=datetime.datetime.today().hour;
		downloaded_minute=datetime.datetime.today().minute;

		#Default Predicted Time
		found_date=False;
		date=[];
		predicted_year=downloaded_year;
		predicted_month=1;
		found_data=False;

		#Parse Lexemes
		for ii in range(0,len(lexemes)):

			#Ignore Comments
			if(len(lexemes[ii])>0 and lexemes[ii][0].startswith("#")==False and lexemes[ii][0].startswith(":")==False):

				#Valid MD Row
				if(len(lexemes[ii])==6 and date_util.month_to_int(lexemes[ii][0])>0 and is_int(lexemes[ii][1])):

					#Found a Date
					found_date=True;
					date=lexemes[ii];

				#Valid Time Row
				elif(len(lexemes[ii])==4 and found_date==True):

					#Convert Hours
					hours=date_util.hhdashhhut_to_hours(lexemes[ii][0]);

					#Extract Data
					if(hours[0]>=0 and hours[1]>=0):

						#3 Days Per Row
						for jj in range(0,3):


							#3 Hours Per Segment
							for kk in range(0,3):

								#Found Data
								found_data=True;

								#Extract Predicted Time, Minute is -1
								predicted_month=date_util.month_to_int(date[jj*2]);
								predicted_day=int(date[jj*2+1]);
								predicted_hour=hours[0]+kk;
								predicted_minute=-1;

								#Extract Predicted Kp
								kp=float(lexemes[ii][1+jj]);

								#Test Predicted Date
								date_test=date_util.valid_date(predicted_year,predicted_month,predicted_day,
									predicted_hour,predicted_minute,ii+1);

								if(date_test[0]==False):
									return date_test;

								#Invalid Kp
								kp_test=kp_util.valid_kp(kp,ii+1);

								if(kp_test[0]==False):
									return kp_test;

								#Only Add Good Data
								if(kp>=0):

									#Add JSON String
									return_json+="\t{\n";

									return_json+="\t\t\"predicted_time\":"
									return_json+="{";
									return_json+=	"\"year\":"+str(downloaded_year)+",";
									return_json+=	"\"month\":"+str(predicted_month)+",";
									return_json+=	"\"day\":"+str(predicted_day)+",";
									return_json+=	"\"hour\":"+str(predicted_hour)+",";
									return_json+=	"\"minute\":"+str(predicted_minute);
									return_json+="}";
									return_json+=",\n";
									return_json+="\t\t\"download_time\":"
									return_json+="{";
									return_json+=	"\"year\":"+str(downloaded_year)+",";
									return_json+=	"\"month\":"+str(downloaded_month)+",";
									return_json+=	"\"day\":"+str(downloaded_day)+",";
									return_json+=	"\"hour\":"+str(downloaded_hour)+",";
									return_json+=	"\"minute\":"+str(downloaded_minute);
									return_json+="}";
									return_json+=",\n";
									return_json+="\t\t\"forecast\":\"d3\",\n";
									return_json+="\t\t\"kp\":"+str(kp)+"\n";

									return_json+="\t}\n";

									if(predicted_day<int(date[5]) or predicted_hour<23):
										return_json+="\t,\n";

		#No Data Means Error
		if(found_data==False):
			return (False,"Did not find any data.");

		#Return Passed and the JSON Object
		return (True,return_json);

	except Exception as e:
		return (False,str(e)[0:].capitalize()+".");

#28 Day Parser (Parses the 28 day forecast).
def parse_d28(lexemes):

	try:
		#JSON Return String
		return_json="";

		#Retrieve Downloaded Time
		downloaded_year=datetime.datetime.today().year;
		downloaded_month=datetime.datetime.today().month;
		downloaded_day=datetime.datetime.today().day;
		downloaded_hour=datetime.datetime.today().hour;
		downloaded_minute=datetime.datetime.today().minute;
		found_data=False;

		#Parse Lexemes
		for ii in range(0,len(lexemes)):

			#Ignore Comments
			if(len(lexemes[ii])>0 and lexemes[ii][0].startswith("#")==False and lexemes[ii][0].startswith(":")==False):

				#Valid Time Row
				if(len(lexemes[ii])==6):

					#Default Values
					predicted_year=1970;
					predicted_month=1;
					predicted_day=1;
					predicted_hour=1;
					predicted_min=1;
					kp=-1;

					#Extract Predicted Time
					predicted_year=int(lexemes[ii][0]);
					predicted_month=date_util.month_to_int(lexemes[ii][1]);
					predicted_day=int(lexemes[ii][2]);
					predicted_hour=-1;
					predicted_minute=-1;

					#Extract Predicted Kp
					kp=float(lexemes[ii][5]);

					#Test Predicted Date
					date_test=date_util.valid_date(predicted_year,predicted_month,predicted_day,
						predicted_hour,predicted_minute,ii+1);

					if(date_test[0]==False):
						return date_test;

					#Invalid Kp
					kp_test=kp_util.valid_kp(kp,ii+1);

					if(kp_test[0]==False):
						return kp_test;

					#Only Add Good Data
					if(kp>=0):

						#Add JSON String
						return_json+="\t{\n";

						return_json+="\t\t\"predicted_time\":"
						return_json+="{";
						return_json+=	"\"year\":"+str(predicted_year)+",";
						return_json+=	"\"month\":"+str(predicted_month)+",";
						return_json+=	"\"day\":"+str(predicted_day)+",";
						return_json+=	"\"hour\":"+str(predicted_hour)+",";
						return_json+=	"\"minute\":"+str(predicted_minute);
						return_json+="}";
						return_json+=",\n";
						return_json+="\t\t\"download_time\":"
						return_json+="{";
						return_json+=	"\"year\":"+str(downloaded_year)+",";
						return_json+=	"\"month\":"+str(downloaded_month)+",";
						return_json+=	"\"day\":"+str(downloaded_day)+",";
						return_json+=	"\"hour\":"+str(downloaded_hour)+",";
						return_json+=	"\"minute\":"+str(downloaded_minute);
						return_json+="}";
						return_json+=",\n";
						return_json+="\t\t\"forecast\":\"now\",\n";
						return_json+="\t\t\"kp\":"+str(kp)+"\n";

						return_json+="\t}\n";

						if(ii<len(lexemes)-1):
							return_json+="\t,\n";

						#Data Found
						found_data=True;

					#Unknown Symbol
					else:
						return (False,"Unexpected symbol \""+str(lexemes[ii][0])+"\" on line "+str(ii+1)+".");

		#No Data Means Error
		if(found_data==False):
			return (False,"Did not find any data.");

		#Return Passed and the JSON Object
		return (True,return_json);

	except Exception as e:
		return (False,str(e)[0:].capitalize()+".");