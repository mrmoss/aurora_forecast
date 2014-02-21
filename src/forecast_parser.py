import datetime
import time

def month_name_to_num(month):
    return time.strptime(month, '%b').tm_mon

def get_current_date():
    return time.strftime("%Y %b %d %H %M")

def date_to_json(year, month, day):
    output_text =  '"year":' + str(year) + ','
    output_text += '"month":' + str(month) + ','
    output_text += '"day":' + str(day) + ','
    return output_text

def time_to_json(hour, minute):
    output_text =  '"hour":' + str(hour) + ','
    output_text += '"minute":' + str(minute)
    return output_text

def datetime_to_json(date, time_obj_name):
    year = date[0:4]
    month = month_name_to_num(date[5:8])
    day = date[9:11]
    json = '"' + time_obj_name + '":{' + date_to_json(year, month, day)

    hour = date[12:14]
    minute = date[15:17]
    json += time_to_json(hour, minute) + '}'
    return json

def parse_28_day(input_text):
    timestamp = datetime_to_json(get_current_date(), 'time_stamp')
    time = " -1 -1" # to indicate all hours and minutes of the day.

    document = input_text.split("\n")
    # Build array of json objects
    output_text = '[ '
    for line in document:
	# As of the project creation, all lines in the file are either comments,
	# or they start with the year. So testing for isdigit() is sufficient
	if line[0:4].isdigit():
	    json = '{' + timestamp + ','
	    json += datetime_to_json(line[0:11] + time, 'time_predicted')
	    kp_value = line[-1]	# kp is all we need, and it is at the end of line.
	    json += ',"forecast":"28day","kp":' + str(kp_value) + '}, '

	    output_text += json
    # Remove the off-by-1 comma made by the loop.
    output_text = output_text[:-2]
    return output_text + ' ]'
	    
def parse_3_day(input_text):
    return

def parse_1_hour(input_text):
    return

def parse_15_min(input_text):

    return

def parse(input_text, which):
    if which == "28d":
	return parse_28_day(input_text)
    elif which == "3d":
	parse_3_day(input_text)
    elif which == "1h":
	parse_1_hour(input_text)
    elif which == "15m":
	parse_15_min(input_text)
    else:
	return "Cannot determine which prediction page"

    return

def main():
    print parse("2014 Feb 11    150		5	3\n2014 Feb 12	    111		5	2")


if __name__ == "__main__":
    main()
