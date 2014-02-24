#!/usr/bin/python
import datetime
import time
from Timestamp import *


def get_current_date():
    return time.strftime("%Y %b %d %H %M")

# String currently is ":Issued: YYYY MMM DD HHMM UTC"#{{{
# CHANGE ABOVE LINE WHEN STRING CHANGES
def get_issue_date(issue_date_string):
    return issue_date_string[9:25]

def get_next_date(current_day):
    time = Timestamp(current_day)
    now = datetime.date(year, month, day)
    delta = datetime.timedelta(days=1)
    next_date = now + delta
    return next_date.strftime('%Y %m %d')
	    
def parse_3_day(input_text, timestamp):
    doc = input_text.split('\n')
    output_text = '[ '
    issued = ':Issued:' # The line that contains issue date.
    for line in doc:
	if issued in line:
	    issue_date = get_issue_date(line)
	    first_day = get_next_date(issue_date)

	elif line[0:3].isdigit():
	    print line[0:3]
    return#}}}


# String currently starts with digit
def parse_28_day(input_text, timestamp):
    document = input_text.split("\n")
    # Build array of json objects
    output_text = '[ '
    for line in document:
	if line[0].isdigit():
            json = '{' + timestamp + ', time_predicted:'
            json += Timestamp(line[0:11]).json() 
	    kp_value = line[-1]	# kp is all we need, and it is at the end of line.
	    json += ',"forecast":"28day","kp":' + str(kp_value) + '}, '

	    output_text += json
    # Remove the off-by-1 comma made by the loop.
    output_text = output_text[:-2]
    return output_text + ' ]'

def parse_1_hour(input_text, timestamp):
    return

def parse_15_min(input_text, timestamp):
    return

def parse(input_text, which_one):
    timestamp = "time_stamp:" + Timestamp(get_current_date()).json()

    if which_one == "28d":
	return parse_28_day(input_text, timestamp)
    elif which_one == "3d":
	return parse_3_day(input_text, timestamp)
    elif which_one == "1h":
	return parse_1_hour(input_text, timestamp)
    elif which_one == "15m":
	return parse_15_min(input_text, timestamp)
    else:
	return "Cannot determine which prediction page"

    return

def main():
    print parse("2014 Feb 11    150		5	3\n2014 Feb 12	    111		5	2", "28d")
    #print parse(":Issued: 2013 Dec 31 2205 UTC\n\n 00-03UT        2         3         3", "3d")

if __name__ == "__main__":
    main()
