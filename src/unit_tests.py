#!/usr/bin/python

#Unit Testing Source
#	Created By:		Paul Gentemann, Caleb Hellickson, Ruslan Kolesnik, Ignacio Saez Lahidalga, and Mike Moss
#	Modified On:	03/04/2014

#Forecast Parser Module
import forecast_parser

#JSON Utility Module
import json_util

#Kp Utility Module
import kp_util

#String Utility Module
import string_util

#Unit Testing Module
import unittest

#JSON Utility Tests
class json_utility_test_suite(unittest.TestCase):

	#Testing Function
	def runTest(self):
		x=0
		#json_util.test_square_brackets
		#json_util.test_syntax
		#json_util.test_aurora_syntax
		#json_util.test_all

#Kp Utility Tests
class kp_utility_test_suite(unittest.TestCase):

	#Testing Function
	def runTest(self):

		#Test Good Data
		for ii in range(-1,10):
			self.assertEqual(kp_util.valid_kp(ii,1)[0],True,"good kp")

		#Test Bad Data
		for ii in range(-1000,-3):
			self.assertEqual(kp_util.valid_kp(ii,1)[0],False,"Bad kp")
		for ii in range(10,1001):
			self.assertEqual(kp_util.valid_kp(ii,1)[0],False,"Bad kp")

#Forecast Parser Tests
class forecast_parser_test_suite(unittest.TestCase):

	#Testing Function
	def runTest(self):

		#Test Now Cast Parser
		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="2014 02 24  0000   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1.00"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],True,"good data - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="1969 02 24  0000   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1.00"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],False,"invalid year - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="-1 02 24  0000   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1.00"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],False,"invalid year - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="2014 13 24  0000   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1.00"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],False,"invalid month - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="2014 00 24  0000   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1.00"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],False,"invalid month - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="2014 -1 24  0000   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1.00"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],False,"invalid month - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="2014 03 32  0000   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1.00"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],False,"invalid day - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="2014 03 00  0000   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1.00"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],False,"invalid day - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="2014 03 -1  0000   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1.00"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],False,"invalid day - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="2014 03 12  -100   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1.00"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],False,"invalid hour - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="2014 03 12  2400   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1.00"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],False,"invalid hour - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="2014 03 12  0060   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1.00"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],False,"invalid minute - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="2014 03 12  00-1   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1.00"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],True,"valid minute - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="2014 03 12  -1-1   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1.00"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],True,"-1 testing - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="2014 03 -1  -1-1   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1.00"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],True,"-1 testing - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="2014 03 -1  -1-1   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1.00"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],True,"-1 testing - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="2014 -1 -1  -1-1   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1.00"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],True,"-1 testing - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="2014 -1 -1  -1-1   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        10.0"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],False,"invalid kp testing - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="2015 03 01  0000   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        -1\n"
		data+="2015 03 01  0000   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],True,"valid kp testing - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="idojfosdijfosdijfso\n"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],False,"random crap testing - "+json[1])

		data="\n\n"
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------\n"
		data+="2015 03 01  0000   0   2014 02 24  0053     3.00       53.0     2014 02 24  0353      2.67     233.0        1"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],True,"empty line testing - "+json[1])

		data=""
		data+=":Data_list: wingkp_list.txt\n"
		data+="#                           1-hour         1-hour                    4-hour         4-hour\n"
		data+="# UT Date   Time         Predicted Time  Predicted  Lead-time     Predicted Time  Predicted  Lead-time   USAF Est.\n"
		data+="# YR MO DA  HHMM   S     YR MO DA  HHMM    Index    in Minutes    YR MO DA  HHMM    Index    in Minutes     Kp\n"
		data+="#-----------------------------------------------------------------------------------------------------------------"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_now(lexemes)
		self.assertEqual(json[0],False,"no data testing - "+json[1])

		#Test 1 Hour Cast Parser
		data=""
		data+=":Product: Geomagnetic Data                AK.txt\n"
		data+="#               Geomagnetic\n"
		data+="#                 Dipole     A   ------------- 3 Hourly K Indices --------------\n"
		data+="# Station        Lat Long  Index 00-03 03-06 06-09 09-12 12-15 15-18 18-21 21-24\n"
		data+="#-------------------------------------------------------------------------------\n"
		data+="\n"
		data+="2014 Mar 2\n"
		data+="\n"
		data+="Boulder          N49 W 42    4     2     1     0     0     2     2     1     1\n"
		data+="Planetary(estimated Ap)      5     3     2     1     1     1     0     1     1\n"
		data+="Wingst           N54 E 95   -1    -1    -1    -1    -1    -1    -1    -1    -1"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_h1(lexemes)
		self.assertEqual(json[0],True,"good data - "+json[1])

		data=""
		data+=":Product: Geomagnetic Data                AK.txt\n"
		data+="#               Geomagnetic\n"
		data+="#                 Dipole     A   ------------- 3 Hourly K Indices --------------\n"
		data+="# Station        Lat Long  Index 00-03 03-06 06-09 09-12 12-15 15-18 18-21 21-24\n"
		data+="#-------------------------------------------------------------------------------\n"
		data+="\n"
		data+="1969 Mar 2\n"
		data+="\n"
		data+="Boulder          N49 W 42    4     2     1     0     0     2     2     1     1\n"
		data+="Planetary(estimated Ap)      5     3     2     1     1     1     0     1     1\n"
		data+="Wingst           N54 E 95   -1    -1    -1    -1    -1    -1    -1    -1    -1"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_h1(lexemes)
		self.assertEqual(json[0],False,"invalid year - "+json[1])

		data=""
		data+=":Product: Geomagnetic Data                AK.txt\n"
		data+="#               Geomagnetic\n"
		data+="#                 Dipole     A   ------------- 3 Hourly K Indices --------------\n"
		data+="# Station        Lat Long  Index 00-03 03-06 06-09 09-12 12-15 15-18 18-21 21-24\n"
		data+="#-------------------------------------------------------------------------------\n"
		data+="\n"
		data+="-1 Mar 2\n"
		data+="\n"
		data+="Boulder          N49 W 42    4     2     1     0     0     2     2     1     1\n"
		data+="Planetary(estimated Ap)      5     3     2     1     1     1     0     1     1\n"
		data+="Wingst           N54 E 95   -1    -1    -1    -1    -1    -1    -1    -1    -1"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_h1(lexemes)
		self.assertEqual(json[0],False,"invalid year - "+json[1])

		data=""
		data+=":Product: Geomagnetic Data                AK.txt\n"
		data+="#               Geomagnetic\n"
		data+="#                 Dipole     A   ------------- 3 Hourly K Indices --------------\n"
		data+="# Station        Lat Long  Index 00-03 03-06 06-09 09-12 12-15 15-18 18-21 21-24\n"
		data+="#-------------------------------------------------------------------------------\n"
		data+="\n"
		data+="2014 sdf 2\n"
		data+="\n"
		data+="Boulder          N49 W 42    4     2     1     0     0     2     2     1     1\n"
		data+="Planetary(estimated Ap)      5     3     2     1     1     1     0     1     1\n"
		data+="Wingst           N54 E 95   -1    -1    -1    -1    -1    -1    -1    -1    -1"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_h1(lexemes)
		self.assertEqual(json[0],False,"invalid month - "+json[1])

		data=""
		data+=":Product: Geomagnetic Data                AK.txt\n"
		data+="#               Geomagnetic\n"
		data+="#                 Dipole     A   ------------- 3 Hourly K Indices --------------\n"
		data+="# Station        Lat Long  Index 00-03 03-06 06-09 09-12 12-15 15-18 18-21 21-24\n"
		data+="#-------------------------------------------------------------------------------\n"
		data+="\n"
		data+="2014 Mar 32\n"
		data+="\n"
		data+="Boulder          N49 W 42    4     2     1     0     0     2     2     1     1\n"
		data+="Planetary(estimated Ap)      5     3     2     1     1     1     0     1     1\n"
		data+="Wingst           N54 E 95   -1    -1    -1    -1    -1    -1    -1    -1    -1"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_h1(lexemes)
		self.assertEqual(json[0],False,"invalid day - "+json[1])

		data=""
		data+=":Product: Geomagnetic Data                AK.txt\n"
		data+="#               Geomagnetic\n"
		data+="#                 Dipole     A   ------------- 3 Hourly K Indices --------------\n"
		data+="# Station        Lat Long  Index 00-03 03-06 06-09 09-12 12-15 15-18 18-21 21-24\n"
		data+="#-------------------------------------------------------------------------------\n"
		data+="\n"
		data+="2014 Mar 0\n"
		data+="\n"
		data+="Boulder          N49 W 42    4     2     1     0     0     2     2     1     1\n"
		data+="Planetary(estimated Ap)      5     3     2     1     1     1     0     1     1\n"
		data+="Wingst           N54 E 95   -1    -1    -1    -1    -1    -1    -1    -1    -1"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_h1(lexemes)
		self.assertEqual(json[0],False,"invalid day - "+json[1])

		data=""
		data+=":Product: Geomagnetic Data                AK.txt\n"
		data+="#               Geomagnetic\n"
		data+="#                 Dipole     A   ------------- 3 Hourly K Indices --------------\n"
		data+="# Station        Lat Long  Index 00-03 03-06 06-09 09-12 12-15 15-18 18-21 21-24\n"
		data+="#-------------------------------------------------------------------------------\n"
		data+="\n"
		data+="2014 Mar -1\n"
		data+="\n"
		data+="Boulder          N49 W 42    4     2     1     0     0     2     2     1     1\n"
		data+="Planetary(estimated Ap)      5     3     2     1     1     1     0     1     1\n"
		data+="Wingst           N54 E 95   -1    -1    -1    -1    -1    -1    -1    -1    -1"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_h1(lexemes)
		self.assertEqual(json[0],False,"invalid day - "+json[1])

		data=""
		data+=":Product: Geomagnetic Data                AK.txt\n"
		data+="#               Geomagnetic\n"
		data+="#                 Dipole     A   ------------- 3 Hourly K Indices --------------\n"
		data+="# Station        Lat Long  Index 00-03 03-06 06-09 09-12 12-15 15-18 18-21 21-24\n"
		data+="#-------------------------------------------------------------------------------\n"
		data+="\n"
		data+="2014 Mar 2\n"
		data+="\n"
		data+="Boulder          N49 W 42    4     2     1     0     0     2     2     1     1\n"
		data+="Planetary(estimated Ap)      5     10     2     1     1     1     0     1     1\n"
		data+="Wingst           N54 E 95   -1    -1    -1    -1    -1    -1    -1    -1    -1"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_h1(lexemes)
		self.assertEqual(json[0],False,"invalid kp testing - "+json[1])

		data=""
		data+=":Product: Geomagnetic Data                AK.txt\n"
		data+="#               Geomagnetic\n"
		data+="#                 Dipole     A   ------------- 3 Hourly K Indices --------------\n"
		data+="# Station        Lat Long  Index 00-03 03-06 06-09 09-12 12-15 15-18 18-21 21-24\n"
		data+="#-------------------------------------------------------------------------------\n"
		data+="\n"
		data+="2014 Mar 2\n"
		data+="\n"
		data+="Boulder          N49 W 42    4     2     1     0     0     2     2     1     1\n"
		data+="Planetary(estimated Ap)     -1    -1    -1    -1    -1    -1    -1    -1    -1\n"
		data+="Wingst           N54 E 95   -1    -1    -1    -1    -1    -1    -1    -1    -1"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_h1(lexemes)
		self.assertEqual(json[0],False,"valid kp testing - "+json[1])

		data="\n\n"
		data+=":Product: Geomagnetic Data                AK.txt\n"
		data+="#               Geomagnetic\n"
		data+="#                 Dipole     A   ------------- 3 Hourly K Indices --------------\n"
		data+="# Station        Lat Long  Index 00-03 03-06 06-09 09-12 12-15 15-18 18-21 21-24\n"
		data+="#-------------------------------------------------------------------------------\n"
		data+="\n"
		data+="2014 Mar 2\n"
		data+="\n"
		data+="Boulder          N49 W 42    4     2     1     0     0     2     2     1     1\n"
		data+="Planetary(estimated Ap)     -1    -1    -1    -1    -1    -1    -1    -1    -1\n"
		data+="Wingst           N54 E 95   -1    -1    -1    -1    -1    -1    -1    -1    -1"
		self.assertEqual(json[0],False,"empty line testing - "+json[1])

		data=""
		data+=":Product: Geomagnetic Data                AK.txt\n"
		data+="#               Geomagnetic\n"
		data+="#                 Dipole     A   ------------- 3 Hourly K Indices --------------\n"
		data+="# Station        Lat Long  Index 00-03 03-06 06-09 09-12 12-15 15-18 18-21 21-24\n"
		data+="#-------------------------------------------------------------------------------\n"
		data+="\n"
		data+="2014 Mar 2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_h1(lexemes)
		self.assertEqual(json[0],False,"no data testing - "+json[1])

		#Test D3 Cast Parser
		data=""
		data+=":Product: 0302geomag_forecast.txt\n"
		data+=":Issued: 2014 Mar 02 2205 UTC\n"
		data+="# Prepared by the U.S. Dept. of Commerce, NOAA, Space Weather Prediction Center\n"
		data+="#\n"
		data+="NOAA Ap Index Forecast\n"
		data+="Observed Ap 01 Mar 007\n"
		data+="NOAA Kp index forecast 03 Mar - 05 Mar\n"
		data+="             Mar 03    Mar 04    Mar 05\n"
		data+="00-03UT        2         2         2\n"
		data+="03-06UT        1         1         1\n"
		data+="06-09UT        1         1         1\n"
		data+="09-12UT        1         1         1\n"
		data+="12-15UT        1         1         1\n"
		data+="15-18UT        1         1         1\n"
		data+="18-21UT        2         2         2\n"
		data+="21-00UT        2         2         2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d3(lexemes)
		self.assertEqual(json[0],True,"good data - "+json[1])

		data=""
		data+=":Product: 0302geomag_forecast.txt\n"
		data+=":Issued: 2014 Mar 02 2205 UTC\n"
		data+="# Prepared by the U.S. Dept. of Commerce, NOAA, Space Weather Prediction Center\n"
		data+="#\n"
		data+="NOAA Ap Index Forecast\n"
		data+="Observed Ap 01 Mar 007\n"
		data+="NOAA Kp index forecast 03 Mar - 05 Mar\n"
		data+="             abc 03    Mar 04    Mar 05\n"
		data+="00-03UT        2         2         2\n"
		data+="03-06UT        1         1         1\n"
		data+="06-09UT        1         1         1\n"
		data+="09-12UT        1         1         1\n"
		data+="12-15UT        1         1         1\n"
		data+="15-18UT        1         1         1\n"
		data+="18-21UT        2         2         2\n"
		data+="21-00UT        2         2         2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d3(lexemes)
		self.assertEqual(json[0],False,"invalid month - "+json[1])

		data=""
		data+=":Product: 0302geomag_forecast.txt\n"
		data+=":Issued: 2014 Mar 02 2205 UTC\n"
		data+="# Prepared by the U.S. Dept. of Commerce, NOAA, Space Weather Prediction Center\n"
		data+="#\n"
		data+="NOAA Ap Index Forecast\n"
		data+="Observed Ap 01 Mar 007\n"
		data+="NOAA Kp index forecast 03 Mar - 05 Mar\n"
		data+="             Mar 32    Mar 04    Mar 05\n"
		data+="00-03UT        2         2         2\n"
		data+="03-06UT        1         1         1\n"
		data+="06-09UT        1         1         1\n"
		data+="09-12UT        1         1         1\n"
		data+="12-15UT        1         1         1\n"
		data+="15-18UT        1         1         1\n"
		data+="18-21UT        2         2         2\n"
		data+="21-00UT        2         2         2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d3(lexemes)
		self.assertEqual(json[0],False,"invalid day - "+json[1])

		data=""
		data+=":Product: 0302geomag_forecast.txt\n"
		data+=":Issued: 2014 Mar 02 2205 UTC\n"
		data+="# Prepared by the U.S. Dept. of Commerce, NOAA, Space Weather Prediction Center\n"
		data+="#\n"
		data+="NOAA Ap Index Forecast\n"
		data+="Observed Ap 01 Mar 007\n"
		data+="NOAA Kp index forecast 03 Mar - 05 Mar\n"
		data+="             Mar 00    Mar 04    Mar 05\n"
		data+="00-03UT        2         2         2\n"
		data+="03-06UT        1         1         1\n"
		data+="06-09UT        1         1         1\n"
		data+="09-12UT        1         1         1\n"
		data+="12-15UT        1         1         1\n"
		data+="15-18UT        1         1         1\n"
		data+="18-21UT        2         2         2\n"
		data+="21-00UT        2         2         2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d3(lexemes)
		self.assertEqual(json[0],False,"invalid day - "+json[1])

		data=""
		data+=":Product: 0302geomag_forecast.txt\n"
		data+=":Issued: 2014 Mar 02 2205 UTC\n"
		data+="# Prepared by the U.S. Dept. of Commerce, NOAA, Space Weather Prediction Center\n"
		data+="#\n"
		data+="NOAA Ap Index Forecast\n"
		data+="Observed Ap 01 Mar 007\n"
		data+="NOAA Kp index forecast 03 Mar - 05 Mar\n"
		data+="             Mar -1    Mar 04    Mar 05\n"
		data+="00-03UT        2         2         2\n"
		data+="03-06UT        1         1         1\n"
		data+="06-09UT        1         1         1\n"
		data+="09-12UT        1         1         1\n"
		data+="12-15UT        1         1         1\n"
		data+="15-18UT        1         1         1\n"
		data+="18-21UT        2         2         2\n"
		data+="21-00UT        2         2         2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d3(lexemes)
		self.assertEqual(json[0],False,"invalid day - "+json[1])

		data=""
		data+=":Product: 0302geomag_forecast.txt\n"
		data+=":Issued: 2014 Mar 02 2205 UTC\n"
		data+="# Prepared by the U.S. Dept. of Commerce, NOAA, Space Weather Prediction Center\n"
		data+="#\n"
		data+="NOAA Ap Index Forecast\n"
		data+="Observed Ap 01 Mar 007\n"
		data+="NOAA Kp index forecast 03 Mar - 05 Mar\n"
		data+="             Mar 03    Mar 04    Mar 05\n"
		data+="00-03UT        2         10         2\n"
		data+="03-06UT        1         1         1\n"
		data+="06-09UT        1         1         1\n"
		data+="09-12UT        1         1         1\n"
		data+="12-15UT        1         1         1\n"
		data+="15-18UT        1         1         1\n"
		data+="18-21UT        2         2         2\n"
		data+="21-00UT        2         2         2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d3(lexemes)
		self.assertEqual(json[0],False,"invalid kp testing - "+json[1])

		data=""
		data+=":Product: 0302geomag_forecast.txt\n"
		data+=":Issued: 2014 Mar 02 2205 UTC\n"
		data+="# Prepared by the U.S. Dept. of Commerce, NOAA, Space Weather Prediction Center\n"
		data+="#\n"
		data+="NOAA Ap Index Forecast\n"
		data+="Observed Ap 01 Mar 007\n"
		data+="NOAA Kp index forecast 03 Mar - 05 Mar\n"
		data+="             Mar 03    Mar 04    Mar 05\n"
		data+="00-03UT        2         -1         2\n"
		data+="03-06UT        1         1         1\n"
		data+="06-09UT        1         1         1\n"
		data+="09-12UT        1         1         1\n"
		data+="12-15UT        1         1         1\n"
		data+="15-18UT        1         1         1\n"
		data+="18-21UT        2         2         2\n"
		data+="21-00UT        2         2         2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d3(lexemes)
		self.assertEqual(json[0],True,"valid kp testing - "+json[1])

		data="\n\n"
		data+=":Product: 0302geomag_forecast.txt\n"
		data+=":Issued: 2014 Mar 02 2205 UTC\n"
		data+="# Prepared by the U.S. Dept. of Commerce, NOAA, Space Weather Prediction Center\n"
		data+="#\n"
		data+="NOAA Ap Index Forecast\n"
		data+="Observed Ap 01 Mar 007\n"
		data+="NOAA Kp index forecast 03 Mar - 05 Mar\n"
		data+="             Mar 03    Mar 04    Mar 05\n"
		data+="00-03UT        2         2         2\n"
		data+="03-06UT        1         1         1\n"
		data+="06-09UT        1         1         1\n"
		data+="09-12UT        1         1         1\n"
		data+="12-15UT        1         1         1\n"
		data+="15-18UT        1         1         1\n"
		data+="18-21UT        2         2         2\n"
		data+="21-00UT        2         2         2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d3(lexemes)
		self.assertEqual(json[0],True,"empty line testing - "+json[1])

		data=""
		data+=":Product: 0302geomag_forecast.txt\n"
		data+=":Issued: 2014 Mar 02 2205 UTC\n"
		data+="# Prepared by the U.S. Dept. of Commerce, NOAA, Space Weather Prediction Center\n"
		data+="#\n"
		data+="NOAA Ap Index Forecast\n"
		data+="Observed Ap 01 Mar 007\n"
		data+="NOAA Kp index forecast 03 Mar - 05 Mar\n"
		data+="             Mar 03    Mar 04    Mar 05\n"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d3(lexemes)
		self.assertEqual(json[0],False,"no data testing - "+json[1])

		#Test 28 Day Cast Parser
		data=""
		data+=":Product: 27-day Space Weather Outlook Table 27DO.txt\n"
		data+=":Issued: 2014 Feb 24 0820 UTC\n"
		data+="#   UTC      Radio Flux   Planetary   Largest\n"
		data+="#  Date       10.7 cm      A Index    Kp Index\n"
		data+="2014 Feb 24     175          10          3\n"
		data+="2014 Feb 25     175           8          3\n"
		data+="2014 Feb 26     175           5          2\n"
		data+="2014 Feb 27     180           5          2\n"
		data+="2014 Feb 28     175          15          3\n"
		data+="2014 Mar 01     170          15          3\n"
		data+="2014 Mar 02     165           5          2\n"
		data+="2014 Mar 03     170           5          2\n"
		data+="2014 Mar 04     175           5          2\n"
		data+="2014 Mar 05     175           5          2\n"
		data+="2014 Mar 06     180           5          2\n"
		data+="2014 Mar 07     180           5          2\n"
		data+="2014 Mar 08     180           5          2\n"
		data+="2014 Mar 09     180          10          3\n"
		data+="2014 Mar 10     175           5          2\n"
		data+="2014 Mar 11     160           8          3\n"
		data+="2014 Mar 12     145           5          2\n"
		data+="2014 Mar 13     145           5          2\n"
		data+="2014 Mar 14     150           5          2\n"
		data+="2014 Mar 15     150           5          2\n"
		data+="2014 Mar 16     150           5          2\n"
		data+="2014 Mar 17     150           5          2\n"
		data+="2014 Mar 18     155           5          2\n"
		data+="2014 Mar 19     155           5          2\n"
		data+="2014 Mar 20     155           5          2\n"
		data+="2014 Mar 21     160           5          2\n"
		data+="2014 Mar 22     165           5          2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d28(lexemes)
		self.assertEqual(json[0],True,"good data - "+json[1])

		data=""
		data+=":Product: 27-day Space Weather Outlook Table 27DO.txt\n"
		data+=":Issued: 2014 Feb 24 0820 UTC\n"
		data+="#   UTC      Radio Flux   Planetary   Largest\n"
		data+="#  Date       10.7 cm      A Index    Kp Index\n"
		data+="1969 Feb 24     175          10          3\n"
		data+="2014 Feb 25     175           8          3\n"
		data+="2014 Feb 26     175           5          2\n"
		data+="2014 Feb 27     180           5          2\n"
		data+="2014 Feb 28     175          15          3\n"
		data+="2014 Mar 01     170          15          3\n"
		data+="2014 Mar 02     165           5          2\n"
		data+="2014 Mar 03     170           5          2\n"
		data+="2014 Mar 04     175           5          2\n"
		data+="2014 Mar 05     175           5          2\n"
		data+="2014 Mar 06     180           5          2\n"
		data+="2014 Mar 07     180           5          2\n"
		data+="2014 Mar 08     180           5          2\n"
		data+="2014 Mar 09     180          10          3\n"
		data+="2014 Mar 10     175           5          2\n"
		data+="2014 Mar 11     160           8          3\n"
		data+="2014 Mar 12     145           5          2\n"
		data+="2014 Mar 13     145           5          2\n"
		data+="2014 Mar 14     150           5          2\n"
		data+="2014 Mar 15     150           5          2\n"
		data+="2014 Mar 16     150           5          2\n"
		data+="2014 Mar 17     150           5          2\n"
		data+="2014 Mar 18     155           5          2\n"
		data+="2014 Mar 19     155           5          2\n"
		data+="2014 Mar 20     155           5          2\n"
		data+="2014 Mar 21     160           5          2\n"
		data+="2014 Mar 22     165           5          2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d28(lexemes)
		self.assertEqual(json[0],False,"invalid year - "+json[1])

		data=""
		data+=":Product: 27-day Space Weather Outlook Table 27DO.txt\n"
		data+=":Issued: 2014 Feb 24 0820 UTC\n"
		data+="#   UTC      Radio Flux   Planetary   Largest\n"
		data+="#  Date       10.7 cm      A Index    Kp Index\n"
		data+="-1 Feb 24     175          10          3\n"
		data+="2014 Feb 25     175           8          3\n"
		data+="2014 Feb 26     175           5          2\n"
		data+="2014 Feb 27     180           5          2\n"
		data+="2014 Feb 28     175          15          3\n"
		data+="2014 Mar 01     170          15          3\n"
		data+="2014 Mar 02     165           5          2\n"
		data+="2014 Mar 03     170           5          2\n"
		data+="2014 Mar 04     175           5          2\n"
		data+="2014 Mar 05     175           5          2\n"
		data+="2014 Mar 06     180           5          2\n"
		data+="2014 Mar 07     180           5          2\n"
		data+="2014 Mar 08     180           5          2\n"
		data+="2014 Mar 09     180          10          3\n"
		data+="2014 Mar 10     175           5          2\n"
		data+="2014 Mar 11     160           8          3\n"
		data+="2014 Mar 12     145           5          2\n"
		data+="2014 Mar 13     145           5          2\n"
		data+="2014 Mar 14     150           5          2\n"
		data+="2014 Mar 15     150           5          2\n"
		data+="2014 Mar 16     150           5          2\n"
		data+="2014 Mar 17     150           5          2\n"
		data+="2014 Mar 18     155           5          2\n"
		data+="2014 Mar 19     155           5          2\n"
		data+="2014 Mar 20     155           5          2\n"
		data+="2014 Mar 21     160           5          2\n"
		data+="2014 Mar 22     165           5          2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d28(lexemes)
		self.assertEqual(json[0],False,"invalid year - "+json[1])

		data=""
		data+=":Product: 27-day Space Weather Outlook Table 27DO.txt\n"
		data+=":Issued: 2014 Feb 24 0820 UTC\n"
		data+="#   UTC      Radio Flux   Planetary   Largest\n"
		data+="#  Date       10.7 cm      A Index    Kp Index\n"
		data+="2014 abc 24     175          10          3\n"
		data+="2014 Feb 25     175           8          3\n"
		data+="2014 Feb 26     175           5          2\n"
		data+="2014 Feb 27     180           5          2\n"
		data+="2014 Feb 28     175          15          3\n"
		data+="2014 Mar 01     170          15          3\n"
		data+="2014 Mar 02     165           5          2\n"
		data+="2014 Mar 03     170           5          2\n"
		data+="2014 Mar 04     175           5          2\n"
		data+="2014 Mar 05     175           5          2\n"
		data+="2014 Mar 06     180           5          2\n"
		data+="2014 Mar 07     180           5          2\n"
		data+="2014 Mar 08     180           5          2\n"
		data+="2014 Mar 09     180          10          3\n"
		data+="2014 Mar 10     175           5          2\n"
		data+="2014 Mar 11     160           8          3\n"
		data+="2014 Mar 12     145           5          2\n"
		data+="2014 Mar 13     145           5          2\n"
		data+="2014 Mar 14     150           5          2\n"
		data+="2014 Mar 15     150           5          2\n"
		data+="2014 Mar 16     150           5          2\n"
		data+="2014 Mar 17     150           5          2\n"
		data+="2014 Mar 18     155           5          2\n"
		data+="2014 Mar 19     155           5          2\n"
		data+="2014 Mar 20     155           5          2\n"
		data+="2014 Mar 21     160           5          2\n"
		data+="2014 Mar 22     165           5          2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d28(lexemes)
		self.assertEqual(json[0],False,"invalid month - "+json[1])

		data=""
		data+=":Product: 27-day Space Weather Outlook Table 27DO.txt\n"
		data+=":Issued: 2014 Feb 24 0820 UTC\n"
		data+="#   UTC      Radio Flux   Planetary   Largest\n"
		data+="#  Date       10.7 cm      A Index    Kp Index\n"
		data+="2014 Feb 32     175          10          3\n"
		data+="2014 Feb 25     175           8          3\n"
		data+="2014 Feb 26     175           5          2\n"
		data+="2014 Feb 27     180           5          2\n"
		data+="2014 Feb 28     175          15          3\n"
		data+="2014 Mar 01     170          15          3\n"
		data+="2014 Mar 02     165           5          2\n"
		data+="2014 Mar 03     170           5          2\n"
		data+="2014 Mar 04     175           5          2\n"
		data+="2014 Mar 05     175           5          2\n"
		data+="2014 Mar 06     180           5          2\n"
		data+="2014 Mar 07     180           5          2\n"
		data+="2014 Mar 08     180           5          2\n"
		data+="2014 Mar 09     180          10          3\n"
		data+="2014 Mar 10     175           5          2\n"
		data+="2014 Mar 11     160           8          3\n"
		data+="2014 Mar 12     145           5          2\n"
		data+="2014 Mar 13     145           5          2\n"
		data+="2014 Mar 14     150           5          2\n"
		data+="2014 Mar 15     150           5          2\n"
		data+="2014 Mar 16     150           5          2\n"
		data+="2014 Mar 17     150           5          2\n"
		data+="2014 Mar 18     155           5          2\n"
		data+="2014 Mar 19     155           5          2\n"
		data+="2014 Mar 20     155           5          2\n"
		data+="2014 Mar 21     160           5          2\n"
		data+="2014 Mar 22     165           5          2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d28(lexemes)
		self.assertEqual(json[0],False,"invalid day - "+json[1])

		data=""
		data+=":Product: 27-day Space Weather Outlook Table 27DO.txt\n"
		data+=":Issued: 2014 Feb 24 0820 UTC\n"
		data+="#   UTC      Radio Flux   Planetary   Largest\n"
		data+="#  Date       10.7 cm      A Index    Kp Index\n"
		data+="2014 Feb 00     175          10          3\n"
		data+="2014 Feb 25     175           8          3\n"
		data+="2014 Feb 26     175           5          2\n"
		data+="2014 Feb 27     180           5          2\n"
		data+="2014 Feb 28     175          15          3\n"
		data+="2014 Mar 01     170          15          3\n"
		data+="2014 Mar 02     165           5          2\n"
		data+="2014 Mar 03     170           5          2\n"
		data+="2014 Mar 04     175           5          2\n"
		data+="2014 Mar 05     175           5          2\n"
		data+="2014 Mar 06     180           5          2\n"
		data+="2014 Mar 07     180           5          2\n"
		data+="2014 Mar 08     180           5          2\n"
		data+="2014 Mar 09     180          10          3\n"
		data+="2014 Mar 10     175           5          2\n"
		data+="2014 Mar 11     160           8          3\n"
		data+="2014 Mar 12     145           5          2\n"
		data+="2014 Mar 13     145           5          2\n"
		data+="2014 Mar 14     150           5          2\n"
		data+="2014 Mar 15     150           5          2\n"
		data+="2014 Mar 16     150           5          2\n"
		data+="2014 Mar 17     150           5          2\n"
		data+="2014 Mar 18     155           5          2\n"
		data+="2014 Mar 19     155           5          2\n"
		data+="2014 Mar 20     155           5          2\n"
		data+="2014 Mar 21     160           5          2\n"
		data+="2014 Mar 22     165           5          2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d28(lexemes)
		self.assertEqual(json[0],False,"invalid day - "+json[1])

		data=""
		data+=":Product: 27-day Space Weather Outlook Table 27DO.txt\n"
		data+=":Issued: 2014 Feb 24 0820 UTC\n"
		data+="#   UTC      Radio Flux   Planetary   Largest\n"
		data+="#  Date       10.7 cm      A Index    Kp Index\n"
		data+="2014 Feb -1     175          10          3\n"
		data+="2014 Feb 25     175           8          3\n"
		data+="2014 Feb 26     175           5          2\n"
		data+="2014 Feb 27     180           5          2\n"
		data+="2014 Feb 28     175          15          3\n"
		data+="2014 Mar 01     170          15          3\n"
		data+="2014 Mar 02     165           5          2\n"
		data+="2014 Mar 03     170           5          2\n"
		data+="2014 Mar 04     175           5          2\n"
		data+="2014 Mar 05     175           5          2\n"
		data+="2014 Mar 06     180           5          2\n"
		data+="2014 Mar 07     180           5          2\n"
		data+="2014 Mar 08     180           5          2\n"
		data+="2014 Mar 09     180          10          3\n"
		data+="2014 Mar 10     175           5          2\n"
		data+="2014 Mar 11     160           8          3\n"
		data+="2014 Mar 12     145           5          2\n"
		data+="2014 Mar 13     145           5          2\n"
		data+="2014 Mar 14     150           5          2\n"
		data+="2014 Mar 15     150           5          2\n"
		data+="2014 Mar 16     150           5          2\n"
		data+="2014 Mar 17     150           5          2\n"
		data+="2014 Mar 18     155           5          2\n"
		data+="2014 Mar 19     155           5          2\n"
		data+="2014 Mar 20     155           5          2\n"
		data+="2014 Mar 21     160           5          2\n"
		data+="2014 Mar 22     165           5          2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d28(lexemes)
		self.assertEqual(json[0],True,"valid day - "+json[1])

		data=""
		data+=":Product: 27-day Space Weather Outlook Table 27DO.txt\n"
		data+=":Issued: 2014 Feb 24 0820 UTC\n"
		data+="#   UTC      Radio Flux   Planetary   Largest\n"
		data+="#  Date       10.7 cm      A Index    Kp Index\n"
		data+="2014 Feb 24     175          10          10\n"
		data+="2014 Feb 25     175           8          3\n"
		data+="2014 Feb 26     175           5          2\n"
		data+="2014 Feb 27     180           5          2\n"
		data+="2014 Feb 28     175          15          3\n"
		data+="2014 Mar 01     170          15          3\n"
		data+="2014 Mar 02     165           5          2\n"
		data+="2014 Mar 03     170           5          2\n"
		data+="2014 Mar 04     175           5          2\n"
		data+="2014 Mar 05     175           5          2\n"
		data+="2014 Mar 06     180           5          2\n"
		data+="2014 Mar 07     180           5          2\n"
		data+="2014 Mar 08     180           5          2\n"
		data+="2014 Mar 09     180          10          3\n"
		data+="2014 Mar 10     175           5          2\n"
		data+="2014 Mar 11     160           8          3\n"
		data+="2014 Mar 12     145           5          2\n"
		data+="2014 Mar 13     145           5          2\n"
		data+="2014 Mar 14     150           5          2\n"
		data+="2014 Mar 15     150           5          2\n"
		data+="2014 Mar 16     150           5          2\n"
		data+="2014 Mar 17     150           5          2\n"
		data+="2014 Mar 18     155           5          2\n"
		data+="2014 Mar 19     155           5          2\n"
		data+="2014 Mar 20     155           5          2\n"
		data+="2014 Mar 21     160           5          2\n"
		data+="2014 Mar 22     165           5          2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d28(lexemes)
		self.assertEqual(json[0],False,"invalid kp testing - "+json[1])

		data=""
		data+=":Product: 27-day Space Weather Outlook Table 27DO.txt\n"
		data+=":Issued: 2014 Feb 24 0820 UTC\n"
		data+="#   UTC      Radio Flux   Planetary   Largest\n"
		data+="#  Date       10.7 cm      A Index    Kp Index\n"
		data+="2014 Feb 24     175          10          -1\n"
		data+="2014 Feb 25     175           8          3\n"
		data+="2014 Feb 26     175           5          2\n"
		data+="2014 Feb 27     180           5          2\n"
		data+="2014 Feb 28     175          15          3\n"
		data+="2014 Mar 01     170          15          3\n"
		data+="2014 Mar 02     165           5          2\n"
		data+="2014 Mar 03     170           5          2\n"
		data+="2014 Mar 04     175           5          2\n"
		data+="2014 Mar 05     175           5          2\n"
		data+="2014 Mar 06     180           5          2\n"
		data+="2014 Mar 07     180           5          2\n"
		data+="2014 Mar 08     180           5          2\n"
		data+="2014 Mar 09     180          10          3\n"
		data+="2014 Mar 10     175           5          2\n"
		data+="2014 Mar 11     160           8          3\n"
		data+="2014 Mar 12     145           5          2\n"
		data+="2014 Mar 13     145           5          2\n"
		data+="2014 Mar 14     150           5          2\n"
		data+="2014 Mar 15     150           5          2\n"
		data+="2014 Mar 16     150           5          2\n"
		data+="2014 Mar 17     150           5          2\n"
		data+="2014 Mar 18     155           5          2\n"
		data+="2014 Mar 19     155           5          2\n"
		data+="2014 Mar 20     155           5          2\n"
		data+="2014 Mar 21     160           5          2\n"
		data+="2014 Mar 22     165           5          2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d28(lexemes)
		self.assertEqual(json[0],True,"valid kp testing - "+json[1])

		data=""
		data+=":Product: 27-day Space Weather Outlook Table 27DO.txt\n"
		data+=":Issued: 2014 Feb 24 0820 UTC\n"
		data+="#   UTC      Radio Flux   Planetary   Largest\n"
		data+="#  Date       10.7 cm      A Index    Kp Index\n"
		data+="sdiofjsodifj Feb 24     175          10          3\n"
		data+="2014 Feb 25     175           8          3\n"
		data+="2014 Feb 26     175           5          2\n"
		data+="2014 Feb 27     180           5          2\n"
		data+="2014 Feb 28     175          15          3\n"
		data+="2014 Mar 01     170          15          3\n"
		data+="2014 Mar 02     165           5          2\n"
		data+="2014 Mar 03     170           5          2\n"
		data+="2014 Mar 04     175           5          2\n"
		data+="2014 Mar 05     175           5          2\n"
		data+="2014 Mar 06     180           5          2\n"
		data+="2014 Mar 07     180           5          2\n"
		data+="2014 Mar 08     180           5          2\n"
		data+="2014 Mar 09     180          10          3\n"
		data+="2014 Mar 10     175           5          2\n"
		data+="2014 Mar 11     160           8          3\n"
		data+="2014 Mar 12     145           5          2\n"
		data+="2014 Mar 13     145           5          2\n"
		data+="2014 Mar 14     150           5          2\n"
		data+="2014 Mar 15     150           5          2\n"
		data+="2014 Mar 16     150           5          2\n"
		data+="2014 Mar 17     150           5          2\n"
		data+="2014 Mar 18     155           5          2\n"
		data+="2014 Mar 19     155           5          2\n"
		data+="2014 Mar 20     155           5          2\n"
		data+="2014 Mar 21     160           5          2\n"
		data+="2014 Mar 22     165           5          2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d28(lexemes)
		self.assertEqual(json[0],False,"random crap testing - "+json[1])

		data="\n\n"
		data+=":Product: 27-day Space Weather Outlook Table 27DO.txt\n"
		data+=":Issued: 2014 Feb 24 0820 UTC\n"
		data+="#   UTC      Radio Flux   Planetary   Largest\n"
		data+="#  Date       10.7 cm      A Index    Kp Index\n"
		data+="2014 Feb 24     175          10          3\n"
		data+="2014 Feb 25     175           8          3\n"
		data+="2014 Feb 26     175           5          2\n"
		data+="2014 Feb 27     180           5          2\n"
		data+="2014 Feb 28     175          15          3\n"
		data+="2014 Mar 01     170          15          3\n"
		data+="2014 Mar 02     165           5          2\n"
		data+="2014 Mar 03     170           5          2\n"
		data+="2014 Mar 04     175           5          2\n"
		data+="2014 Mar 05     175           5          2\n"
		data+="2014 Mar 06     180           5          2\n"
		data+="2014 Mar 07     180           5          2\n"
		data+="2014 Mar 08     180           5          2\n"
		data+="2014 Mar 09     180          10          3\n"
		data+="2014 Mar 10     175           5          2\n"
		data+="2014 Mar 11     160           8          3\n"
		data+="2014 Mar 12     145           5          2\n"
		data+="2014 Mar 13     145           5          2\n"
		data+="2014 Mar 14     150           5          2\n"
		data+="2014 Mar 15     150           5          2\n"
		data+="2014 Mar 16     150           5          2\n"
		data+="2014 Mar 17     150           5          2\n"
		data+="2014 Mar 18     155           5          2\n"
		data+="2014 Mar 19     155           5          2\n"
		data+="2014 Mar 20     155           5          2\n"
		data+="2014 Mar 21     160           5          2\n"
		data+="2014 Mar 22     165           5          2"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d28(lexemes)
		self.assertEqual(json[0],True,"empty line testing - "+json[1])

		data=""
		data+=":Product: 27-day Space Weather Outlook Table 27DO.txt\n"
		data+=":Issued: 2014 Feb 24 0820 UTC\n"
		data+="#   UTC      Radio Flux   Planetary   Largest\n"
		data+="#  Date       10.7 cm      A Index    Kp Index"
		lexemes=forecast_parser.lexer_whitespace(data)
		json=forecast_parser.parse_d28(lexemes)
		self.assertEqual(json[0],False,"no data testing - "+json[1])

#String Utility Tests
class string_utility_test_suite(unittest.TestCase):

	#Testing Function
	def runTest(self):

		#Test Is Int
		self.assertEqual(string_util.is_int("10"),True,"positive integer should be true")
		self.assertEqual(string_util.is_int("0"),True,"zero should be true")
		self.assertEqual(string_util.is_int("-10"),True,"negative integer should be true")
		self.assertEqual(string_util.is_int("10.10"),False,"float should be false")
		self.assertEqual(string_util.is_int("m"),False,"invalid string should be false")

		#Test Whitespace Lexer
		test0=[["abc","def"],["ghi","jkl"],["mno","pqr"]]
		test1=forecast_parser.lexer_whitespace("abc def\nghi\tjkl\rmno             pqr")
		self.assertEqual(test0==test1,True,"whitespaces not separated correctly")

#Unit Testing Main
if(__name__=="__main__"):
	unittest.main()