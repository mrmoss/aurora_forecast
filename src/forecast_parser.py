#!/usr/bin/python
import datetime
import time
from Timestamp import *

# For parse
def get_current_date():
    return time.strftime("%Y %b %d %H %M")

# For 3-day forecast
# String currently is ":Issued: YYYY MMM DD HHMM UTC"
# CHANGE ABOVE LINE IF THE LOGIC CHANGES
def get_issue_date(issue_date_string):
    return issue_date_string[9:20]

# For 3-day forecast
def get_next_date(current_day):
    time = Timestamp(current_day)
    now = datetime.date(time.year, time.month, time.day)
    delta = datetime.timedelta(days=1)
    next_date = now + delta
    return next_date.strftime('%Y %b %d')

# for 3-day forecast
def get_next_three_days(issue_date):
    upcoming_dates = [issue_date]
    for day in range(3):
        next_day = get_next_date(upcoming_dates[day])
        upcoming_dates.append(next_day)
    return upcoming_dates[1:]

# Issue date is the best way to get date. Lines that start with digits are times.
def parse_3_day(input_text, time_now):
    output_text = ''
    issued = ':Issued:' 
    for line in input_text:
        if issued in line:
            starting_from_today = get_issue_date(line)
            next_three_days =  get_next_three_days(starting_from_today)
        elif line[0:2].isdigit():
            kps = line[7:].split()
            for day in next_three_days:
                json = '{' + time_now + ', "time_predicted":'
                json += Timestamp(day + line[0:2]).json() 
                kp_value = kps[0]
                kps = kps[1:]
                json += ',"forecast":"3day","kp":' + str(kp_value) + '},'
                output_text += json
    # Remove the off-by-1 comma made by the loop.
    output_text = output_text[:-1]
    return output_text 


def parse_1_hour(input_text, time_now):
    output_text = ''
    important_line = "Planetary"
    forecast = ',"forecast:"3day","kp":'
    prediction_times = []
    
    for line in input_text:
        if len(line) == 0:
            continue
        elif line[0].isdigit():
            json = '{' + time_now + ', "time_predicted":'
            for hour in range(24):
                all_day = Timestamp(line + ' ' + str(hour)).json()
                prediction_times.append(json + all_day + forecast)
        elif important_line in line:
            kps = line.split()[-8:]
            index = 0
            for hour in range(24):
                prediction_times[hour] += str(kps[hour / 3]) + ' }'
                output_text += prediction_times[hour]
    return output_text

def parse_15_min(input_text, timestamp):
    return

# String currently starts with digit, so that's what we test for.
def parse_28_day(input_text, time_now):
    output_text = ''
    for line in input_text:
        if len(line) == 0:
            continue
	if line[0].isdigit():
            json = '{' + time_now + ', "time_predicted":'
            json += Timestamp(line[0:11]).json() 
	    kp_value = line[-1]	# kp is all we need, and it is at the end of line.
	    json += ',"forecast":"28day","kp":' + str(kp_value) + '},'
	    output_text += json
    # Remove the off-by-1 comma made by the loop.
    output_text = output_text[:-1]
    return output_text 

def parse(input_text, which_one):
    timestamp = '"time_stamp":' + Timestamp(get_current_date()).json()
    text = input_text.split('\n')
    json_array = '[ '

    if which_one == "28d":
	json_array += parse_28_day(text, timestamp)
    elif which_one == "3d":
	json_array += parse_3_day(text, timestamp)
    elif which_one == "1h":
	json_array += parse_1_hour(text, timestamp)
    elif which_one == "15m":
	json_array += parse_15_min(text, timestamp)
    else:
	return "Cannot determine which prediction page"

    return json_array + ' ]'

def main():
    #test_page = "2014 Feb 11    150		5	3\n2014 Feb 12	    111		5	2\n" 
    # test_page = ":Issued: 2013 Dec 31 2205 UTC\n\n00-03UT        5         6         9", "3d"
    test_page = "2014 Feb 27\n\n Planetary(estimated Ap)     24     1     1     1     1     3     4     6     5"
    #print parse(test_page, "28d")
    #print parse(test_page, "3d")
    print parse(test_page, "1h")
    


if __name__ == "__main__":
    main()
